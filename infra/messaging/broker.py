import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django.setup()

from faststream.rabbit import RabbitBroker
from faststream import FastStream

broker = RabbitBroker(django.conf.settings.RABBITMQ_URL)
app = FastStream(broker)


from .handlers.active_artisan import handler_active_artisan
from .handlers.create_wallet import handler_create_wallet
from .handlers.wallet_transaction import handler_wallet_transation
from .worker import start_outbox_worker