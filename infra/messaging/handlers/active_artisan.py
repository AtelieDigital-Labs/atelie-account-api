from ..events.store_created import StoreCreatedEvent
from ..broker import broker
from ..queues import active_artisan_queue
from ..exchanges import exchange_catalogs
from apps.users.services import get_user_service
from asgiref.sync import sync_to_async


@broker.subscriber(exchange=exchange_catalogs, queue=active_artisan_queue)
async def handler_active_artisan(data: StoreCreatedEvent):
    service = get_user_service()
    artisan_id = int(data.artisan_id)
    await sync_to_async(service.active_artisan, thread_sensitive=True)(artisan_id)
