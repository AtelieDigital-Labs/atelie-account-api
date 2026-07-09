from rest_framework import viewsets
from ..serializers.wallets import WalletSerializer
from drf_spectacular.utils import extend_schema
from ...models import Wallet
from apps.audit.mixins import AuditReadMixin


@extend_schema(tags=["Wallets"])
class WalletView(AuditReadMixin, viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
