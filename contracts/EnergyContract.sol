pragma solidity >=0.4.21 <0.7.0;

contract EnergyContract {

	struct matched_entry{
		address _address;
		int _value;
	}

	address payable public owner;
	uint request_counter;
	uint release_counter;
	address[100] pending_requests;
	address[100] pending_release;
	mapping (address => int) request;
	mapping (address => int) release;
	mapping(address => matched_entry) matching;

	constructor() public {
	    owner = msg.sender;
	}
	// producer putting energy to give on the blockchain
	function incomingRequest(address _address, int _value) public {
	   request[_address] += _value;
	   pending_requests[request_counter] = _address;
	   request_counter += 1;
	}

	// consumer putting energy requirement on blockchain
	function incomingRelease(address _address, int _value) public {
		release[_address] = _value;
		pending_release[release_counter] = _address;
		release_counter += 1;
	}

	// fetches the traget producer address for energy transfer by Smart Meter
	function outgoingRelease(address _address) public view returns(address){
		matched_entry memory tmp = matching[_address];
		return tmp._address;
	}

	// aggregator matching producer and consumer
	function doMatching(int _value) public{
	    request[pending_requests[request_counter-1]] -= _value;
	    release[pending_release[release_counter-1]] += _value;
	    matched_entry memory entry;
	    entry._address = pending_requests[request_counter-1];
	    entry._value = _value;
	    matching[pending_release[release_counter-1]] = entry;
	    request_counter -= 1;
	    release_counter -= 1;
	}

	// function called by consumer entity after checking get_mapping_data
	function consume(address sender_address, int _value) public {
	    matching[sender_address]._value = _value;
	}

	// fetching outstanding energy request, 0 means no producer
	function check_request_counter() public view returns (uint){
		return request_counter;
	}

	// fetching outstanding energy consumption request, 0 means no consumer
	function check_release_counter()public view returns (uint){
		return release_counter;
	}

	// fetch the value from the request queue
	function get_request_value() public view returns (int) {
		return request[pending_requests[request_counter-1]];
	}

	// fetch the value from release queue
	function get_release_value() public view returns (int) {
		return release[pending_release[release_counter-1]];
	}

	// get the data and address to give to consumer's meter
	function get_mapping_data(address my_address) public returns (address) {
		release[my_address] = matching[my_address]._value; 
		return matching[my_address]._address;
	}

	// 
	function get_matching_value(address _address) public view returns (int){
		matched_entry memory tmp = matching[_address];
		return tmp._value;
		}
}