from apps.users.services import get_user_service
from .services import WalletService


def get_wallet_service() -> WalletService:
    user_service = get_user_service()
    wallet = WalletService(user_service)

    return wallet
