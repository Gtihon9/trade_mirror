import base64
import json

from solders import message
import requests
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.solders import VersionedTransaction
from solders.transaction import Transaction
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts

class JupiterClient:
    BASE_URL = "https://quote-api.jup.ag/v6"

    def __init__(self, solana_client: Client):
        self.solana_client = solana_client

    def get_quote(
        self,
        input_mint: str,  # Например, "So11111111111111111111111111111111111111112" (SOL)
        output_mint: str,  # Например, "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" (USDC)
        amount: int,       # В минимальных единицах (lamports для SOL)
        slippage: float = 0.5,  # Допустимый slippage в %
    ) -> dict:
        url = f"{self.BASE_URL}/quote"
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": int(slippage * 100),
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def perform_swap(
        self,
        quote: dict,
        user_keypair: Keypair,
    ) -> str:
        # Получаем готовую транзакцию от Jupiter
        swap_url = f"{self.BASE_URL}/swap"
        payload = {
            "quoteResponse": quote,
            "userPublicKey": str(user_keypair.pubkey()),
            "wrapUnwrapSOL": True,
        }
        response = requests.post(swap_url, json=payload)
        response.raise_for_status()
        swap_transaction = response.json()["swapTransaction"]

        raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swap_transaction))
        signature = user_keypair.sign_message(message.to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)

        result = self.solana_client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
        transaction_id = json.loads(result.to_json())['result']

        return result