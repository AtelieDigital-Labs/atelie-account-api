from rest_framework import serializers
from ...models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework.validators import UniqueValidator


class CustomUserDetailsSerializer(UserDetailsSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)
    cpf = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Este CPF já está em uso."
            )
        ],
    )
    date_of_birth = serializers.DateField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            "phone_number",
            "cpf",
            "date_of_birth",
        )
        read_only_fields = (
            "cpf",
            "date_of_birth",
        )
