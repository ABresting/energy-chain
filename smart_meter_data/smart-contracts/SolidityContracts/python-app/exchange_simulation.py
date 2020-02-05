import json
import datetime
from web3 import Web3
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

logging.getLogger('flask_cors').level = logging.DEBUG

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
compiledFile= json.load(open('../build/contracts/SmartMeterContract.json'))

abi = compiledFile['abi']

owner_1 = "0x84bBBB7c6f6e5C0bE095a8158D0cbe47Fd06228D"
owner_2 = "0x512b3C5194200a46D635759BBc03C54C16C0460D"

private_key_1 = "cdad5a87ec436246e1b6c2e88de3b1ff5d28b83414fd51bd97af74d4900ced7c"
private_key_2 = "58c66bcdbd84d9f423310227a03ea6a8319e2f693abe75bc09e6fb152dd6b78d"

contract_address_1 = '0xa4eF592A08d69E7549029BEc42da3CaB3161f2F8' 
contract_address_2 = '0x7956EBFFF235e14ffBb5E256a77135b6429C15F7'

contract_1 = web3.eth.contract(address=contract_address_1, abi=abi)
contract_2 = web3.eth.contract(address=contract_address_2, abi=abi)

production1 =  [15,18,21,30,23,45,56,42,10,42,60,115] # energy surplus
consumption1 = [10,14,15,16,17,18,20,40,5,39,40,100]
production2 =  [7,3,10,14,8,20,19,23,4,15,26,37] # energy defficit
consumption2 = [10,8,18,17,14,27,41,32,5,32,41,65] 

def check_contract_creation():
    owner_1 = contract_1.functions.owner().call()
    print(owner_1)
    owner_2 = contract_2.functions.owner().call()
    print(owner_2)

def simulateConsumption(contract,consumption,owner,private_key):
    for i in consumption:
     registerConsumptionValue(contract, i, owner, private_key)

def simulateProduction(contract,production,owner,private_key):
    for i in production:
     registerProductionValue(contract, i, owner, private_key)
    
def registerConsumptionValue(contract, value, owner, private_key):
    nonce = web3.eth.getTransactionCount(owner)
    transaction = contract.functions.addConsumedValue(value).buildTransaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('0.1', 'gwei'),
        'from': owner,
        'nonce': nonce
    }) 
    signed_txn = sign_transaction(transaction, private_key) 
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)

def registerProductionValue(contract, value, owner, private_key):
    nonce = web3.eth.getTransactionCount(owner)
    transaction = contract.functions.addProducedValue(value).buildTransaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('0.1', 'gwei'),
        'from': owner,
        'nonce': nonce
    }) 
    signed_txn = sign_transaction(transaction, private_key) 
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)

def sign_transaction(tx, private_key):
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    return signed_tx

def getTotalProductionPerRegion():
    value = 0
    for i in range(len(production1)):
         value += production1[i] + production2[i]
    return value

def getTotalConsumptionPerRegion():
    value = 0
    for i in range(len(consumption1)):
         value += consumption1[i] + consumption2[i]
    return value

def getHouseholdConsumption():
    value = 0
    for i in range(len(consumption1)):
         value += consumption1[i]
    return value

def getHouseholdProduction():
    value = 0
    for i in range(len(production1)):
         value += production1[i]
    return value
    
check_contract_creation()
#simulateConsumption(contract_1,consumption1,owner_1, private_key_1)
#simulateProduction(contract_1, production1, owner_1, private_key_1)
#simulateConsumption(contract_2,consumption2,owner_2, private_key_2)
#simulateProduction(contract_2, production2, owner_2, private_key_2)

@app.route('/lastUsage', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_usage():
    profile_usage = []
    for i in range(len(consumption1)):
        profile_dictionary = {'date': '','produced': '', 'consumed': '' }
        profile_dictionary['date'] = datetime.datetime.now()
        profile_dictionary['produced'] = production1[i]
        profile_dictionary['consumed'] = consumption1[i]
        profile_usage.append(profile_dictionary)
    return jsonify(profile_usage)

@app.route('/lastTransactions', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_transactions():
    transactions = []
    for i in range(len(consumption1)):
        transaction_dictionary = {'date': '','destination': '', 'amount': '' }
        transaction_dictionary['date'] = datetime.datetime.now()
        transaction_dictionary['destination'] = owner_2
        transaction_dictionary['amount'] = production1[i]-consumption1[i]
        transactions.append(transaction_dictionary)
    return jsonify(transactions)

@app.route('/info', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_info():
    household_production_total = getHouseholdConsumption()
    household_consumption_total = getHouseholdProduction()
    info_dictionary = {'totalProduced': household_production_total,'totalConsumed': household_consumption_total, 'coins': 99 }    
    return jsonify(info_dictionary)

@app.route('/region/info', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_region_info():
    total_production = getTotalProductionPerRegion()
    total_consumption = getTotalConsumptionPerRegion()
    info_dictionary = {'totalProduced': total_production,'totalConsumed': total_consumption, 'coins': 99 }    
    return jsonify(info_dictionary)

@app.route("/hello",  methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/region/usage', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_region_usage():
    profile_usage = []
    for i in range(len(consumption1)):
        profile_dictionary = {'date': '','produced': '', 'consumed': '' }
        profile_dictionary['date'] = datetime.datetime.now()
        profile_dictionary['produced'] = production1[i] + production2[i]
        profile_dictionary['consumed'] = consumption1[i] + consumption2[i]
        profile_usage.append(profile_dictionary)
    return jsonify(profile_usage)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')