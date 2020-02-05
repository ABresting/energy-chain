##################################################################

The code is divided into two parts:
1. Smart contract end to end PoC
2. Smart Meter Data generation code for visualization

# Smart contract end to end PoC:

Located in root directory /energy-chain/python-app

## It has 3 main components:

1. Producer Node:

file: producer_node.py

It simulates the application layer of the Smart Meter where it interacts with ethereum blockchain using the smart contract.

put_energy_request(address, value) - this function helps into making sure that the Smart Meter with the given address supplies a value which represents the amount of energy it has and willing to share with peers.

2. Consumer Node:

file: consumer_node.py

it simulates the application layer of the Smart Meter where it interacts with ethereum blockchain using the smart contract.

put_energy_release(address, value) - this function helps into making sure that the Smart Meter with the given address supplies a value which represents the amount of energy it requires from the peers.

fetch_target_address(address) - this function with it's given address, fetches the address of the target producer from which the energy transfer will be initiated.

3. Aggregator Node:

file: aggregator_node.py

the major functionality of this component is to connect the producers and consumers, and to make this process transparent and auditable blockchain based solution is perfect.

check_incoming_energy() - it crawls the pending requests from producers and consumers into making sure that the demand can be met. It checks if there is enough energy from producers that consumers can utilize.


## Smart Contract

EnergyContract - Energy chain smart contract running over ethereum ganache blockchain.

Structure - matched_entry - it stores the target address(\_address) of the Smart Meter from where the energy transfer will be done, along with the value(\_value) for auditing purpose.

Array - pending_requests and pending_release - these two arrays which keeps track of the outstanding pending request and release, it can be modified by the index counter explained below so that we don't have to perform the delete action on the blockchain, so instead overwrite it.

request_counter and release_counter : they track the index of the last request which isto be processed.

mapping (address => int) request - this keeps the track of Smart Meters which wants to give away the energy for the consumers on peer-to-peer model.

mapping (address => int) release - this keeps the track of Smart Meters which wants to receieve the energy from the peer producers.

mapping(address => matched_entry) matching - it stores the address which will receive the energy from the peers, information on the producer is stores in the matched_entry structure.