from django.db import transaction
from .models import Wallet, WalletTransaction


class WalletService:
    def __init__(self, user_service) -> None:
        self.user_service = user_service

    @transaction.atomic
    def transactions(self, data):
        order_id = data["order_id"]
        wallet = Wallet.objects.select_for_update().get(user=data["artisan_id"])
        amount = data["total_amount"]
        wallet.balance += amount
        wallet.save()

        WalletTransaction.objects.create(
            order_id=order_id,
            wallet=wallet,
            amount=amount,
        )

    @transaction.atomic
    def create_wallet(self, data):
        user = self.user_service.get_user_by_id(data.get("artisan_id"))

        if not user:
            print(
                f"[WARNING] Usuário {data.get('artisan_id')} não encontrado. Pulando criação de carteira."
            )
            return  # Aqui ele sai graciosamente, o consumer dá ACK e a mensagem some da fila

        wallet, created = Wallet.objects.get_or_create(
            user=user, defaults={"pix_key": data["pix_key"]}
        )

        if created:
            print(f"[SUCCESS] Carteira criada para o usuário {user.pk}")
        else:
            print(
                f"[INFO] Carteira já existia para o usuário {user.pk}. Ignorado para manter idempotência."
            )
