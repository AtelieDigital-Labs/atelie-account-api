from django.db import transaction
from apps.users.models import User
from ...models import Wallet 

@transaction.atomic
def callback_store_created(data):
    # .filter().first() evita a exceção e retorna None se o usuário não existir
    user = User.objects.filter(pk=data.get("artisan_id")).first()

    if not user:
        print(f"[WARNING] Usuário {data.get('artisan_id')} não encontrado. Pulando criação de carteira.")
        return  # Aqui ele sai graciosamente, o consumer dá ACK e a mensagem some da fila

    # get_or_create garante a idempotência: se já existir, ele não duplica e não quebra
    wallet, created = Wallet.objects.get_or_create(
        user=user,
        defaults=data['pix_key']
    )

    if created:
        print(f"[SUCCESS] Carteira criada para o usuário {user.pk}")
    else:
        print(f"[INFO] Carteira já existia para o usuário {user.pk}. Ignorado para manter idempotência.")

@transaction.atomic
def callback_become_atisan(data):
    user_id = data['artisan_id']

    user = User.objects.filter(pk=user_id).first()

    if not user:
        return  
    
    if user.is_artisan:
        return
    
    user.is_artisan = True
    user.save()