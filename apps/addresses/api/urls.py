from rest_framework.routers import SimpleRouter
from .views import AddressView


router = SimpleRouter()
router.register(r"", AddressView, basename="addresses")

urlpatterns = router.urls
