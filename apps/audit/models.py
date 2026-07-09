import uuid

from django.db import models


class LogOutbox(models.Model):

    id = models.BigAutoField(primary_key=True)
    log_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    aggregate_type = models.CharField(
        max_length=100,
    )
    aggregate_id = models.CharField(
        max_length=100,
    )
    payload = models.JSONField()
    processed = models.BooleanField(
        default=False,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "log_outbox"
        ordering = ["created_at"]
        verbose_name = "Log Outbox"
        verbose_name_plural = "Log Outbox"

    def __str__(self):
        return f"[{self.aggregate_type}] {self.aggregate_id} — {self.log_id}"
