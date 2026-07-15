from dj_rest_auth.views import LoginView, LogoutView
from drf_spectacular.utils import extend_schema
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from ..serializers.login import CustomLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

@extend_schema(tags=["Auth"])
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


@extend_schema(tags=["Auth"])
class CustomLogoutView(LogoutView):
    pass


@extend_schema(tags=["Auth"])
class CustomGoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GOOGLE_CALLBACK_URL
