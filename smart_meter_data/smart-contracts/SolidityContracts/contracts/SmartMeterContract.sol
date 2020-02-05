pragma solidity >=0.4.21 <0.7.0;

 contract SmartMeterContract {

    address payable public owner;
    int[] public consumedValues;
    int[] public producedValues;

    constructor() public {
        owner = msg.sender;
    }

    function addConsumedValue(int value) public {
       consumedValues.push(value);
    }

    function addProducedValue(int value) public {
      producedValues.push(value);
    }

    function getProducedValue(uint index) public view returns (int){
        return producedValues[index];
    }

    function getConsumedValue(uint index) public view returns (int){
        return consumedValues[index];
    }
 }

