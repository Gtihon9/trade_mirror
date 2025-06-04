
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from django.conf import settings


class SolanaAPI:
    def __init__(self):
        self.client = Client(settings.SOLANA_RPC_URL)

    def get_transactions(self, wallet_address):
        """Получаем последние 10 транзакций кошелька"""
        try:
            # Конвертируем строку адреса в Pubkey
            pubkey = Pubkey.from_string(wallet_address)
            signatures = self.client.get_signatures_for_address(
                pubkey,
                limit=10
            )


            transactions = []
            for sig in signatures.value:
                if sig:
                    tx = self.client.get_transaction(sig.signature)
                    if tx:
                        transactions.append({
                            'signature': tx.value.transaction,
                            'timestamp': tx.value.block_time,
                            'details': tx  # Полные детали транзакции
                        })
            return transactions

        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []


    def get_balance(self, wallet_address):
        """Получаем баланс кошелька"""
        try:
            pubkey = Pubkey.from_string(wallet_address)
            response = self.client.get_balance(pubkey)
            balance_lamports = response.value  # Balance in lamports
            balance_sol = balance_lamports / 1e9  # Convert to SOL
            return balance_sol
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return