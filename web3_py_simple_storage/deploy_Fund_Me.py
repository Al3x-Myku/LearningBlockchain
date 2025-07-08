from web3 import Web3
import json
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
load_dotenv()

install_solc('0.8.17')
with open("./Fund_Me.sol", "r") as file:
    fund_me_file = file.read()

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Fund_Me.sol": {"content": fund_me_file}},
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
with open("compiled_fund_me.json", "w") as file:
    json.dump(compile_sol, file)
bytecode = compile_sol["contracts"]["Fund_Me.sol"]["FundMe"]["evm"]["bytecode"]["object"]
abi = compile_sol["contracts"]["Fund_Me.sol"]["FundMe"]["abi"]
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
chain_id = 11155111
my_address = os.getenv("ACCOUNT_ADDRESS")  # asta chiar e portofelul meu lmao
# nu da push la key in plain txt
private_key = os.getenv("PRIVATE_KEY")  # aici venea cheia sper ca nu am lasat-o in plain text
Fund_Me = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)
# build transaction
transaction = Fund_Me.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# semnezi
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# trimite transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

#interact with the contract
print(f"Deployed! {txn_hash.hex()}")

# Wait for the transaction to be mined
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# Get the contract address
contract_address = txn_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")

fund_me = w3.eth.contract(address=contract_address, abi=abi)
# Example interaction: call the getPrice function
price = fund_me.functions.getPrice().call()
print(f"Current price: {price}")
owner = fund_me.functions.owner().call()
print(f"Contract owner: {owner}")
Fund = fund_me.functions.Fund().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "value": w3.to_wei(0.03, "ether"),  # Fund with 0.8 ETH
        "nonce": w3.eth.get_transaction_count(my_address),
    }
)
signed_fund_txn = w3.eth.account.sign_transaction(Fund, private_key=private_key)
fund_txn_hash = w3.eth.send_raw_transaction(signed_fund_txn.raw_transaction)    
# Wait for the fund transaction to be mined
w3.eth.wait_for_transaction_receipt(fund_txn_hash)  
withdraw_txn = fund_me.functions.withdraw().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.get_transaction_count(my_address),
    }
)
signed_withdraw_txn = w3.eth.account.sign_transaction(withdraw_txn, private_key=private_key)
withdraw_txn_hash = w3.eth.send_raw_transaction(signed_withdraw_txn.raw_transaction)
# Wait for the withdraw transaction to be mined
w3.eth.wait_for_transaction_receipt(withdraw_txn_hash)
print("Funds withdrawn successfully!")

