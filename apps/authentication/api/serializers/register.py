from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from datetime import date
from apps.users.services import get_user_service
from validate_docbr import CPF


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate_email(self, email):
        user_service = get_user_service()
        if user_service.email_exists(email):
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return email

    def validate_phone_number(self, value):
        phone_number = "".join(filter(str.isdigit, value))

        if len(phone_number) != 11:
            raise serializers.ValidationError(
                "O Número de telefone deve conter exatamente 11 dígitos."
            )

        return phone_number

    def validate_cpf(self, value):
        cpf = "".join(filter(str.isdigit, value))

        if len(cpf) != 11:
            raise serializers.ValidationError(
                "O CPF deve conter exatamente 11 dígitos."
            )

        cpf_validator = CPF()

        if not cpf_validator.validate(cpf):
            raise serializers.ValidationError("CPF inválido.")

        user_service = get_user_service()
        if user_service.cpf_exists(cpf):
            raise serializers.ValidationError("CPF em uso.")

        return cpf

    def validate_date_of_birth(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError(
                "A data de nascimento não pode ser no futuro."
            )

        AGE_OF_MAJORITY = 18
        try:
            limit_date = date(today.year - AGE_OF_MAJORITY, today.month, today.day)
        except ValueError:  # Tratamento para anos bissextos
            limit_date = date(today.year - AGE_OF_MAJORITY, today.month, today.day - 1)

        if value > limit_date:
            raise serializers.ValidationError("Você deve ter pelo menos 18 anos.")

        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),
                "last_name": self.validated_data.get("last_name", ""),
                "phone_number": self.validated_data.get("phone_number", ""),
                "cpf": self.validated_data.get("cpf", ""),
                "date_of_birth": self.validated_data.get("date_of_birth"),
            }
        )
        return data

    def save(self, request):
        user = super().save(request)

        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.phone_number = self.validated_data.get("phone_number")
        user.cpf = self.validated_data.get("cpf")
        user.date_of_birth = self.validated_data.get("date_of_birth")

        user.save(
            update_fields=[
                "first_name",
                "last_name",
                "phone_number",
                "cpf",
                "date_of_birth",
            ]
        )

        return user
