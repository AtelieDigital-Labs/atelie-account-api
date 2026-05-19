import pika
from django.conf import settings


def get_connection():

    credentials = pika.PlainCredentials(
        "guest",
        "guest"
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=5672,
        credentials=credentials,
    )

    return pika.BlockingConnection(parameters)