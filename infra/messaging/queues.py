from faststream.rabbit import RabbitQueue
from .constants import RoutingKey, Queue

active_artisan_queue = RabbitQueue(
    name=Queue.BECOME_ARTISAN_QUEUE,
    routing_key=RoutingKey.STORE_CREATED_ROUTING_KEY,
    durable=True,
)

create_wallet_queue = RabbitQueue(
    name=Queue.CREATE_WALLET_QUEUE,
    routing_key=RoutingKey.STORE_CREATED_ROUTING_KEY,
    durable=True,
)

wallet_transaction_queue = RabbitQueue(
    name=Queue.WALLET_TRANSACTION_QUEUE,
    routing_key=RoutingKey.ORDER_PAID_ROUTING_KEY,
    durable=True,
)
