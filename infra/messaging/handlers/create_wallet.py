from apps.wallets.dependencies import get_wallet_service
from ..broker import broker
from ..queues import create_wallet_queue
from ..exchanges import exchange_catalogs
from asgiref.sync import sync_to_async


@broker.subscriber(exchange=exchange_catalogs, queue=create_wallet_queue)
async def handler_create_wallet(data: dict):
    service = get_wallet_service()

    await sync_to_async(service.create_wallet)(data)
