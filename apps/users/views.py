from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import permissions, status, viewsets
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
        # Garante que o usuário só veja os endereços vinculados ao ID dele no Token
        user = self.request.user
        return models.UserAddress.objects.filter(user=user)
    
    def perform_create(self, serializer):
        # Garante que ao criar, o endereço seja vinculado ao usuário logado
        serializer.save(user=self.request.user)

class BecomeArtisanView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BecomeArtisanSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        user.is_artisan = True
        user.save() 
        
        return Response(
            {"message": "Agora você é um artesão!"}, 
            status=status.HTTP_200_OK
        )
    
