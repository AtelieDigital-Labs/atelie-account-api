from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = models.User
        fields = ["id", "username", "email"]
