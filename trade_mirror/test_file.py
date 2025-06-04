import requests

# url = "http://127.0.0.1:8000/api/profile/"
# headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4OTcwMzU2LCJpYXQiOjE3NDg5NjY3NTYsImp0aSI6IjA5MmU2MDc0MDgyYTQ4YWNhODM2NTNlZTBmYjA2NWYzIiwidXNlcl9pZCI6Mn0.3iWKm57Fj3re74yL0_amu4bdsvuuhY_CYMwvarXQU2Q"}
# response = requests.get(url, headers=headers)
# print(response.json())


url = "http://127.0.0.1:8000/api/transactions/"
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4OTcwMzU2LCJpYXQiOjE3NDg5NjY3NTYsImp0aSI6IjA5MmU2MDc0MDgyYTQ4YWNhODM2NTNlZTBmYjA2NWYzIiwidXNlcl9pZCI6Mn0.3iWKm57Fj3re74yL0_amu4bdsvuuhY_CYMwvarXQU2Q"}
response = requests.get(url, headers=headers)

# import requests
#
# wallet_address = "EXCrDonPgYbBphkviAi9LT4WMCAHf8Z9N1waZVynBm3a"
# solana_rpc_url = "https://api.mainnet-beta.solana.com"
#
# payload = {
#     "jsonrpc": "2.0",
#     "id": 1,
#     "method": "getSignaturesForAddress",
#     "params": [wallet_address, {"limit": 10}]
# }
#
# response = requests.post(solana_rpc_url, json=payload)
# signatures = response.json().get("result", [])
#
# for sig in signatures:
#     payload = {
#         "jsonrpc": "2.0",
#         "id": 1,
#         "method": "getTransaction",
#         "params": [sig["signature"], {"encoding": "json"}]
#     }
#
#     response = requests.post(solana_rpc_url, json=payload)
#     transaction_details = response.json().get("result", {})
#
#     print(transaction_details)

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
WALLET_ADRESS = "EXCrDonPgYbBphkviAi9LT4WMCAHf8Z9N1waZVynBm3a"

from solana.rpc.api import Client
from solders.pubkey import Pubkey

client = Client(SOLANA_RPC_URL)

pubkey = Pubkey.from_string(WALLET_ADRESS)
signatures = client.get_signatures_for_address(pubkey,limit=10)
import json

transactions = []

for sig in signatures.value:
    if sig:
        tx = client.get_transaction(sig.signature)
        if tx:

            transactions.append({
                'signature': tx.value.transaction,
                'timestamp': tx.value.block_time,
                'details': tx  # Полные детали транзакции
            })
print(transactions)
# Convert to JSON
# transactions = [
#     {
#         "signature": tx.signature,
#         "slot": tx.slot,
#         "block_time": tx.block_time,
#         "confirmation_status": tx.confirmation_status,
#     }
#     for tx in signatures.value  # Используйте `.value`, если доступно
# ]
# print(transactions)