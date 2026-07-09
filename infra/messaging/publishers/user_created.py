from ..broker import broker
from ..exchanges import exchange_accounts
from ..constants import RoutingKey
from dataclasses import asdict
from ..events.user_created import UserCreatedEvent


async def publish_user_created(event: UserCreatedEvent):
    await broker.publish(
        exchange=exchange_accounts,
        routing_key=RoutingKey.USER_CREATED_ROUTING_KEY,
        message=asdict(event),
    )
