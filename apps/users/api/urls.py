from django.urls import path
from .views.users import CustomUserDetailsView
from .views.profiles import ProfileView

urlpatterns = [
    path(r"me/", ProfileView.as_view(), name="me"),
    path(r"user/", CustomUserDetailsView.as_view(), name="rest_user_details"),
]
