import json
from web3 import Web3


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
filee = json.load(open('/home/xx/IMDEA_HCKTON/energy-chain/build/contracts/EnergyContract.json'))

abi = filee['abi']
contract_address = '0x6f1b910Cea5Ce57cB4475f50409a55221B2d6c01'
contract = web3.eth.contract(address=contract_address, abi=abi)

my_account = '0xD1923f6c017Aa011f4479dC3eE267fe804C4CD86'
my_private_key = '046f82ef3e41b35506d2d8795bc698716678077df3ff85aff03448c06c98dda6'

def sign_transaction(tx, private_key):
	
	signed_tx = web3.eth.account.signTransaction(tx, private_key)
	return signed_tx

# requesting average energy requriement from peers
def put_energy_release(address, value):
	nonce = web3.eth.getTransactionCount(address)
	transaction = contract.functions.incomingRelease(address ,
    value ).buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('0.1', 'gwei'),
    'from': address,
    'nonce': nonce
    }) 
	signed_txn = sign_transaction(transaction, my_private_key) 
	
	web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# getting address of the target SmartMeter for energy transfer
def fetch_target_address(address):
	nonce = web3.eth.getTransactionCount(address)
	transaction = contract.functions.outgoingRelease(address ,
    value ).buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('0.1', 'gwei'),
    'from': address,
    'nonce': nonce
    }) 
	signed_txn = sign_transaction(transaction, my_private_key) 
	
	web3.eth.sendRawTransaction(signed_txn.rawTransaction)