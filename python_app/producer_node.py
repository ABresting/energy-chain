import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
filee = json.load(open('/home/xx/IMDEA_HCKTON/energy-chain/build/contracts/EnergyContract.json'))

abi = filee['abi']
contract_address = '0x6f1b910Cea5Ce57cB4475f50409a55221B2d6c01'
contract = web3.eth.contract(address=contract_address, abi=abi)

my_account = '0xffb179D5936E11348abFc4226c1566C05481ef8c'
my_private_key = '85dbd469176616ca29ebe0aebaaf1ddbd0cdb858326588c3b918c1e67e733da4'

def sign_transaction(tx, private_key):
	
	signed_tx = web3.eth.account.signTransaction(tx, private_key)
	return signed_tx

# advertising excess energy for peers to consume
def put_energy_request(address, value):
	nonce = web3.eth.getTransactionCount(address)
	transaction = contract.functions.incomingRequest(address ,
    value ).buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('0.1', 'gwei'),
    'from': address,
    'nonce': nonce
    }) 
 
	signed_txn = sign_transaction(transaction, my_private_key) 
	
	web3.eth.sendRawTransaction(signed_txn.rawTransaction)