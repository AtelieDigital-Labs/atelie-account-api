from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from ..serializers.register import CustomRegisterSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Auth"])
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


@extend_schema(tags=["Auth"])
class CustomResendEmailVerificationView(ResendEmailVerificationView):
    pass


@extend_schema(tags=["Auth"])
class CustomVerifyEmailView(VerifyEmailView):
    pass
