const EnergyContract = artifacts.require("EnergyContract");

module.exports = function(deployer) {
  deployer.deploy(EnergyContract);
};
