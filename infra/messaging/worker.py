import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.local"
)

django.setup()

from infra.messaging.base_consumer import RabbitMQConsumer


from infra.messaging.constants import *

from apps.wallets.messaging.handlers.order_paid import callback_wallet_transaction


from apps.wallets.messaging.handlers.store_created import (
    callback_store_created,
    callback_become_atisan
)


consumer = RabbitMQConsumer()

consumer.register(
    exchange=ORDER_EXCHANGE,
    queue=WALLET_TRANSACTION_QUEUE,
    routing_key=ORDER_PAID_ROUTING_KEY,
    callback=callback_wallet_transaction,
)

consumer.register(
    exchange=CATALOG_EXCHANGE,
    queue=CREATE_WALLET_QUEUE,
    routing_key=STORE_CREATED_ROUTING_KEY,
    callback=callback_store_created,
)

consumer.register(
    exchange=CATALOG_EXCHANGE,
    queue=BECOME_ARTISAN_QUEUE,
    routing_key=STORE_CREATED_ROUTING_KEY,
    callback=callback_become_atisan,
)

consumer.start()