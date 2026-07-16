
import logging
import uuid
from datetime import datetime, timezone

from .context import get_current_actor
from .models import LogOutbox

logger = logging.getLogger(__name__)


def create_outbox_entry(
    action: str,
    resource: str,
    resource_id: str,
    changes: dict,
    reason: str,
) -> LogOutbox:

    log_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "log_id": log_id,
        "timestamp": timestamp,
        "microservice": "Accounts",
        "actor": {
            "user_id": get_current_actor(),
        },
        "action": action,
        "resource": resource,
        "resource_id": str(resource_id),
        "changes": changes,
        "reason": reason,  # inserir justificativa
    }

    entry = LogOutbox.objects.create(
        log_id=log_id,
        aggregate_type=resource,
        aggregate_id=str(resource_id),
        payload=payload,
        processed=False,
    )

    logger.info(
        "[INFO] Log gerado: log_id=%s",
        log_id,
    )

    return entry
