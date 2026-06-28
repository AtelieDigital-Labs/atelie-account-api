from rest_framework.routers import SimpleRouter
from .views.wallets import WalletView

router = SimpleRouter()

router.register(r"", WalletView, basename="wallet")

urlpatterns = router.urls
