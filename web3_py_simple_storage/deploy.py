import solcx
from solcx import compile_standard
import json
from web3 import Web3
# Connect to Ganache
solcx.install_solc('0.8.17')
with open("./SimpleStorgae.sol", "r") as file:
    simple_storage_file = file.read()
    

compile_sol = compile_standard(
{
    "language": "Solidity",
    "sources": {"SimpleStorgae.sol": {"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*" : {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    },
},
solc_version ="0.8.17",
)
with open("compiled_sol.json", "w") as file:
    json.dump(compile_sol, file)

bytecode = compile_sol["contracts"]["SimpleStorgae.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

abi = compile_sol["contracts"]["SimpleStorgae.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xCb22C032d64f92ae1aB0EE923EEA1Ad5a2b96d11"
#nu da push la key in plain txt
private_key = "0xfa0ba31965d5c70039350bd3f90ec8a9ac153f98abb15e93ff8fff5b1a813aa5"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)

#build transaction
# sign transaction
# send transaction
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

#acum semnezi
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# trimite transaction
# Look for where you send the raw transaction
# Change .rawTransaction to .raw_transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

#Good practice to wait for the transaction to be mined
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print("Deployed!")

#interactiune cu contractul
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
# print(simple_storage.functions.retrieve().call())
#Call -> returns a value
#Transact -> changes a value
# print(simple_storage.functions.store(15).call()) 15
# print(simple_storage.functions.retrieve().call()) 0

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.get_transaction_count(my_address),
    }
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.raw_transaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)

print(simple_storage.functions.retrieve().call())  # Should print 15