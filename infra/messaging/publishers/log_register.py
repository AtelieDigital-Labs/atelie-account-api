from ..broker import broker
from ..exchanges import exchange_logs
from ..constants import RoutingKey


async def publisher_log_register(message: dict):
    await broker.publish(
        exchange=exchange_logs,
        routing_key=RoutingKey.LOG_REGISTER_ROUTING_KEY,
        message=message
    )

