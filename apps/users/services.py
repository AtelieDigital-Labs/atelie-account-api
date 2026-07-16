from .models import User
from django.shortcuts import get_object_or_404
from django.db import transaction


class UserService:
    def list_all(self) -> list[User]:
        users = User.objects.all()

        return users

    def get_user_by_id(self, user_id: int) -> User:
        user = get_object_or_404(User, pk=user_id)

        return user

    @transaction.atomic
    def update(self, user, data):
        for field, value in data.items():
            setattr(user, field, value)

        user.save(update_fields=data.keys())

        return user

    def cpf_exists(self, cpf: str) -> bool:
        return User.objects.filter(cpf=cpf).exists()

    def email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @transaction.atomic
    def active_artisan(self, artisan_id: int) -> User:
        artisan = self.get_user_by_id(artisan_id)

        if artisan.is_artisan:
            print("Usuário é um artesão")

        artisan.is_artisan = True
        artisan.save(update_fields=["is_artisan"])
        return artisan


def get_user_service() -> UserService:
    service = UserService()

    return service
