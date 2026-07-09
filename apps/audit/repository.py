

import logging

from django.db import transaction

from .models import LogOutbox

logger = logging.getLogger(__name__)

# Limite máximo de registros por execução (batching)
BATCH_SIZE = 50


def process_outbox_batch() -> list[LogOutbox]:
    with transaction.atomic():
        entries = list(
            LogOutbox.objects
            .select_for_update(skip_locked=True)
            .filter(processed=False)
            .order_by("created_at")[:BATCH_SIZE]
        )

    count = len(entries)

    if count > 0:
        logger.info(
            "Outbox: %d registro(s) pendente(s) recuperado(s).",
            count,
        )
    else:
        logger.debug("Outbox: nenhum registro pendente.")

    return entries
