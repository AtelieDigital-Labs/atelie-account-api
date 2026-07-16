from django.apps import AppConfig


class AuditConfig(AppConfig):
    name = "apps.audit"
    verbose_name = "Auditoria (Transactional Outbox)"

    def ready(self):
        import apps.audit.signals 
