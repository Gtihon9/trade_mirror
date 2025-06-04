from celery import shared_task
from .models import User, SolanaTransaction
from .solana_client import SolanaAPI


@shared_task
def check_new_transactions():
    users = User.objects.exclude(solana_wallet=None)
    solana = SolanaAPI()

    for user in users:
        txs = solana.get_transactions(user.solana_wallet)
        for tx in txs:
            SolanaTransaction.objects.get_or_create(
                user=user,
                tx_hash=tx['signature'],
                defaults={
                    'sender': tx['sender'],
                    'receiver': tx['receiver'],
                    'amount': tx['amount'],
                    'token': tx['token']
                }
            )
