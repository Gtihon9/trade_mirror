from django.contrib.auth.models import AbstractUser
from django.db import models
from .jupiter_client import JupiterClient

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

class SwapRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_mint = models.CharField(max_length=100)
    output_mint = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    slippage = models.FloatField(default=0.5)
    tx_hash = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def execute_swap(self, user_keypair: Keypair):
        jupiter = JupiterClient(solana_client=Client("https://api.mainnet-beta.solana.com"))
        try:
            quote = jupiter.get_quote(
                self.input_mint,
                self.output_mint,
                self.amount,
                self.slippage,
            )
            tx_hash = jupiter.perform_swap(quote, user_keypair)
            self.tx_hash = tx_hash
            self.status = "success"
        except Exception as e:
            self.status = f"failed: {str(e)}"
        finally:
            self.save()