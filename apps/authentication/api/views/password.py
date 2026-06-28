from dj_rest_auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Auth"])
class CustomPasswordChangeView(PasswordChangeView):
    pass


@extend_schema(tags=["Auth"])
class CustomPasswordResetView(PasswordResetView):
    pass


@extend_schema(tags=["Auth"])
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass
