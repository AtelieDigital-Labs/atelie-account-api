from rest_framework.routers import SimpleRouter
from .views.wallets import WalletView, WalletByArtisan
from django.urls import path
router = SimpleRouter()

router.register(r"wallets", WalletView, basename="wallets")

urlpatterns = [path("users/me/wallet/", WalletByArtisan.as_view(), name="wallet-by-artisan")] + router.urls
