const SmartMeterContract = artifacts.require("./SmartMeterContract.sol");

module.exports = function(deployer) {
  deployer.deploy(SmartMeterContract);
};
