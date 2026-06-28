from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Auth"])
class CustomTokenVerifyView(TokenVerifyView):
    pass


RefreshView = get_refresh_view()


@extend_schema(tags=["Auth"])
class CustomTokenRefreshView(RefreshView):
    pass
