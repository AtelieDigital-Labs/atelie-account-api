

from .services import create_outbox_entry


class AuditReadMixin:

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        instance = self.get_object()
        create_outbox_entry(
            action="SELECT",
            resource=instance._meta.db_table,
            resource_id=str(instance.pk),
            changes={},
            reason="Consulta individual de saldo/extrato.",
        )

        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset())
        for instance in queryset:
            create_outbox_entry(
                action="SELECT",
                resource=instance._meta.db_table,
                resource_id=str(instance.pk),
                changes={},
                reason="Consulta de listagem de saldo/extrato.",
            )

        return response
