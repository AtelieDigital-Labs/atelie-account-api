from .views.login import CustomLoginView, CustomLogoutView, CustomGoogleLogin
from .views.register import (
    CustomRegisterView,
    CustomVerifyEmailView,
    CustomResendEmailVerificationView,
)
from .views.token import CustomTokenRefreshView, CustomTokenVerifyView
from .views.password import (
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
)
from django.urls import path

urlpatterns = [
    path("resgister/", CustomRegisterView.as_view(), name="rest_register"),
    path("verify-email/", CustomVerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "resend-email/",
        CustomResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("logout/", CustomLogoutView.as_view(), name="rest_logout"),
    path(
        "password/change/",
        CustomPasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path(
        "password/reset/", CustomPasswordResetView.as_view(), name="rest_password_reset"
    ),
    path(
        "password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("login/google/", CustomGoogleLogin.as_view(), name="google_login"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
