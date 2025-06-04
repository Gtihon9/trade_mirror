from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    solana_wallet = models.CharField(
        max_length=44, # Длина Solana-адреса
        blank=True,
        null=True,
        unique=True,
        verbose_name="Solana Wallet Adress"
    )

    def __str__(self):
        return self.username


class SolanaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    tx_hash = models.CharField(max_length=64, unique=True)
    sender = models.CharField(max_length=44)  # Кошелек отправителя
    receiver = models.CharField(max_length=44)  # Кошелек получателя
    amount = models.DecimalField(max_digits=18, decimal_places=9)
    token = models.CharField(max_length=10)  # SOL/USDC/etc
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]