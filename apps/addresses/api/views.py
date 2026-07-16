from rest_framework import viewsets
from ..models import Address
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressSerializer
from drf_spectacular.utils import extend_schema
from apps.users.services import get_user_service


@extend_schema(tags=["Addresses"])
class AddressView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Garante que ao criar, o endereço seja vinculado ao usuário logado
        serializer.save(user=self.request.user)


class A(viewsets.ViewSet):
    def list(self, request, pk):
        service = get_user_service()
        return service.get_user_by_id(pk)
