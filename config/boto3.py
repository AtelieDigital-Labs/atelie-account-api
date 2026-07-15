import boto3
from botocore.exceptions import ClientError

from django.conf import settings


def ensure_bucket_exists():
    client = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    bucket = settings.AWS_STORAGE_BUCKET_NAME

    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        client.create_bucket(Bucket=bucket)

from storages.backends.s3 import S3Storage

class LocalMinioStorage(S3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        # Gera a URL assinada padrão usando o endpoint interno (minio:9000)
        url = super().url(name, parameters, expire, http_method)
        
        # Substitui o host do Docker pelo host que o seu navegador/React entende
        if "http://minio:9000" in url:
            return url.replace("http://minio:9000", "http://localhost:9000")
        return url