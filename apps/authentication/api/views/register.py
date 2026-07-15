from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from ..serializers.register import CustomRegisterSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    tags=["Auth"], 
    examples=[
        OpenApiExample(
            name="Exemplo de registro",
            value={
                "username": "string",
                "email": "user@example.com",
                "password1": "string",
                "password2": "string",
                "first_name": "string",
                "last_name": "string",
                "phone_number": "(00) 00000-0000",
                "cpf": "000.000.000-00",
                "date_of_birth": "2000-01-01"
            },
            request_only=True,
        )
    ],
)
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


@extend_schema(tags=["Auth"])
class CustomResendEmailVerificationView(ResendEmailVerificationView):
    pass


@extend_schema(tags=["Auth"])
class CustomVerifyEmailView(VerifyEmailView):
    pass
