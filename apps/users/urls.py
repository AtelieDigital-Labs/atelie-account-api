from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'addresses', views.AddressView, basename='addresses')

urlpatterns = [
    path(r'me/', views.UserView.as_view(), name='me'),
    path(r'become-artisan/', views.BecomeArtisanView.as_view(), name='become-artisan')
] + router.urls