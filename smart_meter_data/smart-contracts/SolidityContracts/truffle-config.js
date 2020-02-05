module.exports = {

  networks: {
    ganache_1: {
      host: "127.0.0.1",
      port: "7545",
      network_id: "*", //match any network id
      gasPrice: 20000000000,
      gas: 100721975,
      from: "0x84bBBB7c6f6e5C0bE095a8158D0cbe47Fd06228D" // account 2
    },
    ganache_2: {
      host: "127.0.0.1",
      port: "7545",
      network_id: "*", //match any network id
      gasPrice: 20000000000,
      gas: 100721975,
      from: "0x512b3C5194200a46D635759BBc03C54C16C0460D" // account 3
    }
  },

  compilers: {
    solc: {
        version: "^0.5.5",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200
            }
        }
    }
}
}