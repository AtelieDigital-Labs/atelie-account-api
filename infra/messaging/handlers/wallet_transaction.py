from apps.wallets.dependencies import get_wallet_service
from ..broker import broker
from ..queues import wallet_transaction_queue
from ..exchanges import exchange_orders
from asgiref.sync import sync_to_async


@broker.subscriber(exchange=exchange_orders, queue=wallet_transaction_queue)
async def handler_wallet_transation(data: dict):
    service = get_wallet_service()

    await sync_to_async(service.transactions)(data)
