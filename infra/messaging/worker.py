import asyncio
from asgiref.sync import sync_to_async
from .publishers.log_register import publisher_log_register

from .broker import app, broker
from apps.audit.models import LogOutbox
from apps.audit.repository import process_outbox_batch
from config.logger import setup_trigger_logger

logger = setup_trigger_logger()

@sync_to_async
def mark_entries_as_processed(entry_ids: list[int]):
    LogOutbox.objects.filter(id__in=entry_ids).update(processed=True)

async def outbox_worker_loop():
    while True:
        try:
            entries = await sync_to_async(process_outbox_batch)()
            
            if not entries:
                await asyncio.sleep(5)
                continue

            processed_ids = []

            for entry in entries:
                await publisher_log_register(message=entry.payload)
                
                logger.info(f"Log {entry.log_id} enviado para a mensageria com sucesso")

                processed_ids.append(entry.id)
            
            if processed_ids:
                await mark_entries_as_processed(processed_ids)

        except Exception as e:
            logger.error("Erro no processamento do Outbox: %s", e, exc_info=True)
            await asyncio.sleep(5)


@app.on_startup
async def start_outbox_worker():
    logger.info("Iniciando o Worker de polling do Outbox...")

    asyncio.create_task(outbox_worker_loop())