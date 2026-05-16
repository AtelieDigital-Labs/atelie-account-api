from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from . import serializers
from . import models
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    
class UserView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = serializers.UserSerializer
    
    def get_object(self):
        # Retorna o usuário logado para o Serializer trabalhar
        return self.request.user

class AddressView(viewsets.ModelViewSet):
    queryset = None
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return models.UserAddress.objects.none()

        if not self.request.user.is_authenticated:
            return models.UserAddress.objects.none()

        return models.UserAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Garante que ao criar, o endereço seja vinculado ao usuário logado
        serializer.save(user=self.request.user)


class ActivateArtisanView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_artisan:
            return Response({"message": "Usuário já é artisan"})

        user.is_artisan = True
        user.save()

        return Response({"message": "Usuário ativado como artisan"})