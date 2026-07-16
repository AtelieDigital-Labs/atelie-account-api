from storages.backends.s3 import S3Storage

class CustomMinioStorage(S3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        # 1. Gera a URL assinada padrão (apontando internamente para http://minio:9000)
        url = super().url(name, parameters, expire, http_method)
        
        # 2. Substitui o host interno pelo seu endereço público com HTTPS e a rota /media
        url = url.replace("http://minio:9000", "https://ateliedigital.dev.br/media")
        return url
