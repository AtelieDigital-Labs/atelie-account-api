from django.db import models
from django.conf import settings

class Wallet(models.Model):
    # Relação 1:1 garante que cada artesão tenha apenas uma carteira
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pix_key = models.CharField(max_length=100, blank=True, null=True)

class WalletTransaction(models.Model):
    # Relação 1:N (Uma carteira tem várias transações)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=50, null=True, blank=True) # Para rastrear de qual pedido veio
    created_at = models.DateTimeField(auto_now_add=True)

class Withdrawal(models.Model):
    # Relação 1:N (Uma carteira tem vários saques)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pendente'), ('COMPLETED', 'Concluído')])
    created_at = models.DateTimeField(auto_now_add=True)