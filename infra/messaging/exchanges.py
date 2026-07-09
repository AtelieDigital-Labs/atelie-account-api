from faststream.rabbit import RabbitExchange, ExchangeType
from .constants import Exchange

exchange_accounts = RabbitExchange(
    name=Exchange.ACCOUNTS_EXCHANGE, type=ExchangeType.TOPIC, durable=True
)

exchange_catalogs = RabbitExchange(
    name=Exchange.CATALOG_EXCHANGE, type=ExchangeType.TOPIC, durable=True
)

exchange_orders = RabbitExchange(
    name=Exchange.ORDER_EXCHANGE, type=ExchangeType.TOPIC, durable=True
)

exchange_logs = RabbitExchange(
    name=Exchange.LOG_EXCHANGE, type=ExchangeType.TOPIC, durable=True
)