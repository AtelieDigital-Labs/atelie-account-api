from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/addresses/", include("apps.addresses.api.urls")),
    path("api/v1/accounts/", include("apps.users.api.urls")),
    path("api/v1/accounts/", include("apps.authentication.api.urls")),
    path("api/v1/accounts/wallets/", include("apps.wallets.api.urls")),
    path("accounts/", include("allauth.urls")),
    # Optional UI:
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
