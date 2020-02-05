import json
from web3 import Web3


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
filee = json.load(open('/home/xx/IMDEA_HCKTON/energy-chain/build/contracts/EnergyContract.json'))

abi = filee['abi']
contract_address = '0x6f1b910Cea5Ce57cB4475f50409a55221B2d6c01'
contract = web3.eth.contract(address=contract_address, abi=abi)

my_account = '0x874f2b698744CC2b938AB17Ce385686CFe22878e'
my_private_key = "7a83ca12464c53e37ec7b0f30ff4dee712275a862bc2869bc228f3ddd17115d7"


def sign_transaction(tx, private_key):
	
	signed_tx = web3.eth.account.signTransaction(tx, private_key)
	return signed_tx

def chk_request_counter():
	return contract.functions.check_request_counter().call()

def chk_release_counter():
	return contract.functions.check_release_counter().call()

def fetch_request_value():
	return contract.functions.get_request_value().call()	

def fetch_release_value():
	return contract.functions.get_release_value().call()	

# Consumer chekcing if an incoming source assigned to it
def check_incoming_energy():
	
	if chk_request_counter():
		if chk_release_counter():
			request_value = fetch_request_value()
			release_value = fetch_release_value()

			if request_value >= release_value :
				nonce = web3.eth.getTransactionCount(my_account)
				transaction = contract.functions.doMatching(release_value).buildTransaction({
			    'gas': 2000000,
			    'gasPrice': web3.toWei('0.1', 'gwei'),
			    'from': my_account,
			    'nonce': nonce
			    }) 
				signed_txn = sign_transaction(transaction, my_private_key)
				web3.eth.sendRawTransaction(signed_txn.rawTransaction)