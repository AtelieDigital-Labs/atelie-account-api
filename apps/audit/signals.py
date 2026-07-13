from apps.wallets.models import WalletTransaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.users.models import User
from apps.wallets.models import Wallet

from .models import LogOutbox
from .services import create_outbox_entry

_MONITORED_MODELS = (User, Wallet, WalletTransaction)


def _serialize_value(value) -> str:
    """Converte qualquer valor para string para padronização do payload."""
    if value is None:
        return "None"
    return str(value)


@receiver(pre_save, sender=User)
@receiver(pre_save, sender=Wallet)
@receiver(pre_save, sender=WalletTransaction)
def audit_pre_save(sender, instance, **kwargs):

    # Guard: não auditar o próprio LogOutbox
    if sender is LogOutbox:
        return

    if instance.pk is None:
        instance._audit_is_create = True
        instance._audit_changes = {}
        return

    # Busca o estado atual no banco antes do save
    try:
        old_instance = sender.objects.filter(pk=instance.pk).values().first()
    except sender.DoesNotExist:
        instance._audit_is_create = True
        instance._audit_changes = {}
        return

    if old_instance is None:
        instance._audit_is_create = True
        instance._audit_changes = {}
        return

    # Calcula o diff campo a campo
    changes = {}
    for field_name, old_value in old_instance.items():
        # Ignora a PK e campos internos
        if field_name in ("id", "password", "last_login"):
            continue

        new_value = getattr(instance, field_name, None)

        if hasattr(new_value, "pk"):
            new_value = new_value.pk

        if str(old_value) != str(new_value):
            changes[field_name] = {
                "old_value": _serialize_value(old_value),
                "new_value": _serialize_value(new_value),
            }

    instance._audit_is_create = False
    instance._audit_changes = changes



@receiver(post_save, sender=User)
@receiver(post_save, sender=Wallet)
@receiver(post_save, sender=WalletTransaction)
def audit_post_save(sender, instance, created, **kwargs):

    # Guard: não auditar o próprio LogOutbox (evita loop recursivo)
    if sender is LogOutbox:
        return

    resource = sender._meta.db_table
    resource_id = str(instance.pk)

    is_create = getattr(instance, "_audit_is_create", created)
    changes = getattr(instance, "_audit_changes", {})

    if is_create:
        create_outbox_entry(
            action="INSERT",
            resource=resource,
            resource_id=resource_id,
            changes={},
            reason=f"Criação de registro em {resource}.",
        )
    elif changes:
        create_outbox_entry(
            action="UPDATE",
            resource=resource,
            resource_id=resource_id,
            changes=changes,
            reason=f"Atualização de registro em {resource}.",
        )

    instance._audit_is_create = None
    instance._audit_changes = None
