from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")}
