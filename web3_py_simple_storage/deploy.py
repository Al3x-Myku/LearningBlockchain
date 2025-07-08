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
chain_id = 5777
my_address = "0xCb22C032d64f92ae1aB0EE923EEA1Ad5a2b96d11"
private_key = "0xfa0ba31965d5c70039350bd3f90ec8a9ac153f98abb15e93ff8fff5b1a813aa5"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

