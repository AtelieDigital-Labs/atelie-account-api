from django.db import transaction
from ...models import Wallet, WalletTransaction


def callback_wallet_transaction(data):

    order_id = data["order_id"]

    if WalletTransaction.objects.filter(order_id=order_id).exists():
        return

    with transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=data["artisan_id"]
        )

        amount = data["total_amount"]

        wallet.balance += amount
        wallet.save()

        WalletTransaction.objects.create(
            order_id=order_id,
            wallet=wallet,
            amount=amount,
        )