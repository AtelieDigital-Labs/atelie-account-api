from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Primeiro tenta Authorization: Bearer <token>
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth

        # Se não houver Bearer, tenta o cookie
        raw_token = request.COOKIES.get("access")
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return user, validated_token