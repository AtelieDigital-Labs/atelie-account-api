from ..serializers.users import CustomUserDetailsSerializer
from dj_rest_auth.views import UserDetailsView
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Users"])
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
