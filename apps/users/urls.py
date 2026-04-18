from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'me', views.UserView, basename='me')

urlpatterns = router.urls