from django.apps import AppConfig

from config.boto3 import ensure_bucket_exists


class UsersConfig(AppConfig):
    name = "apps.users"

    # def ready(self):
    #     ensure_bucket_exists()