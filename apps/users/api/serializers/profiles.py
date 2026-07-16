from ...models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "email",
            "profile_image",
            'is_artisan',
            'phone_number',
            'cpf',
            'date_of_birth'
        ]

    def validate(self, attrs):
        for field, value in attrs.items():
            if isinstance(value, str):
                attrs[field] = value.strip()

        return attrs
