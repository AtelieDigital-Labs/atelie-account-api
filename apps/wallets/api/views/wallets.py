from rest_framework import viewsets
from ..serializers.wallets import WalletSerializer
from drf_spectacular.utils import extend_schema
from ...models import Wallet


@extend_schema(tags=["Wallets"])
class WalletView(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
