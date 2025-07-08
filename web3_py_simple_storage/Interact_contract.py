from web3 import Web3
import json
from solcx import compile_standard, install_solc
install_solc('0.8.17')
import os
from dotenv import load_dotenv
load_dotenv()

contract_address = "0x9f7DC768f4e4e56aD50B2D21dAb34261B57781dD"

my_address = os.getenv("ACCOUNT_ADDRESS")  # asta chiar e portofelul meu lmao
# nu da push la key in plain txt
private_key = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
w3.eth.default_account = my_address

# Compile the Solidity contract to generate ABI (only needed once, then save ABI to Fund_Me_abi.json)
with open("Fund_Me.sol", "r") as file:
    fundme_source_code = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Fund_Me.sol": {"content": fundme_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.17",
)

# Extract ABI and save to FundMe_abi.json
abi = compiled_sol["contracts"]["Fund_Me.sol"]["FundMe"]["abi"]
with open("FundMe_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)


# ABI for the contract (replace with the actual ABI of your contract)
with open("FundMe_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

nonce = w3.eth.get_transaction_count(my_address)

# # Build transaction to call fundMe (assuming the function is called 'fund' and is payable)
# transaction = contract.functions.Fund().build_transaction({
#     "from": my_address,
#     "value": w3.to_wei(0.01, "ether"),  # adjust the value as needed
#     "nonce": nonce,
#     "gas": 200000,
#     "gasPrice": w3.to_wei("10", "gwei"),
# })

# # Sign the transaction
# signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# # Send the transaction
# tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# print(f"Transaction sent! Hash: {tx_hash.hex()}")

# # Increment nonce for the next transaction
# nonce += 1

withdraw_transaction = contract.functions.withdraw().build_transaction({
    "from": my_address,
    "nonce": nonce,
    "gasPrice": w3.to_wei("10", "gwei"),
})

# Sign the transaction
signed_withdraw_txn = w3.eth.account.sign_transaction(withdraw_transaction, private_key=private_key)

# Send the transaction
withdraw_tx_hash = w3.eth.send_raw_transaction(signed_withdraw_txn.raw_transaction)

print(f"Withdraw transaction sent! Hash: {withdraw_tx_hash.hex()}")