from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from ..serializers.wallets import WalletSerializer
from drf_spectacular.utils import extend_schema
from ...models import Wallet
from apps.audit.mixins import AuditReadMixin

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

@extend_schema(tags=["Wallets"])
class WalletView(AuditReadMixin, viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

@extend_schema(tags=["Wallets"])
class WalletByArtisan(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)