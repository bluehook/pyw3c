const sdk = {
  getAccount: function() {
    return new Promise((resolve, reject) => {
      // Get the initial account balance so it can be displayed.
      web3.eth.getAccounts(function (err, accs) {
        if (err != null) {
          console.error('There was an error fetching your accounts.');
          reject(err);
        }

        if (accs.length === 0) {
          console.error("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.");
          reject("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.");
        }

        self.account = accs[0];
        resolve(self.account);
      });
    });
  },

  // get account balance, return ether
  getBalance: function(account) {
    return new Promise((resolve, reject) => {
      web3.eth.getBalance(self.account, (err, balance) => {
        if (err) {
          console.error("failed to get account blance: ", self.account, err);
          reject(err);
        }

        self.balance = balance;
        console.log("balance: ", self.balance);
        resolve(balance);
      });
    });
  },

  buyXid: function(affcode, team, amount) {
    return new Promise(function (resolve, reject) {
      let fomo;
      let gas;
      FoMo3Dlong.deployed().then(function (instance) {
        fomo = instance;
        console.log("buyxid2 instance");
        gas =  fomo.buyXid.estimateGas(affcode, team, {from: self.account, value: amount});
        console.log("estimate returned", gas);
        return gas;
      }).then(function (value) {
        console.log("buyxid2 esitmatedgas", value.valueOf());
        var trans = fomo.buyXid(affcode, team, {from: self.account, value: amount, gas: value.valueOf(), gasPrice: 1000000000});
        console.log("transaction buyxid has been subbmitted: ", trans);
        trans = trans;
        resolve(trans);
      }).catch((err) => {
        console.error("buyXid err: ", err);
        reject(err);
      });
    });
  },

  setup: function() {
    const self = this;
    return new Promise(function (resolve, reject) {
      FoMo3Dlong.setProvider(web3.currentProvider);
      //F3Devents.setProvider(web3.currentProvider);

      self.getAccount().then((account) => {
        self.getBalance(account).then( (balance)=> {
          resolve();
        }).catch((err) => {
          reject(err);
        });
      }).catch((err) => {
        reject(err);
      });
    });
  },

  getTimeLeft: function() {
    const self = this;
    return new Promise(function (resolve, reject) {
      FoMo3Dlong.deployed().then(instance => {
        return instance.getTimeLeft();
      }).then(value => {
        resolve(value.valueOf());
      }).catch(e => {
        console.error("getTimeLeft err: ", e);
        reject(e);
      });
    });
  },

  iWantXKeys: function(keys) {
    const self = this;
    return new Promise(function (resolve, reject) {
      FoMo3Dlong.deployed().then(instance => {
        return instance.iWantXKeys(web3.toWei(keys, 'ether'));
      }).then(value => {
        resolve(value.valueOf());
      }).catch(e => {
        console.log("iWantXKeys err:", e, keys);
        reject(e);
      });
    });
  },

  isActivated: function() {
    const self = this;
    return new Promise(function (resolve, reject) {
      let fomo;
      FoMo3Dlong.deployed().then(function (instance) {
        fomo = instance;
        return fomo.activated_.call();
      }).then(function (value) {
        resolve(value);
      }).catch(function (e) {
        console.error(e);
        reject(e);
      });
    });
  },

  getCurrentRoundInfo: function() {
    return new Promise(function (resolve, reject) {
      FoMo3Dlong.deployed().then(instance => {
        return instance.getCurrentRoundInfo.call();
      }).then(value => {

        let ret = {
          ico: Number(value[0].valueOf()),
          roundid: Number(value[1].valueOf()),
          keys: Number(value[2].valueOf()),
          end: Number(value[3].valueOf()),
          start: Number(value[4].valueOf()),
          pot: Number(value[5].valueOf()),
          teamId: Number(value[6].valueOf() % 10),
          playerId: Number((value[6].valueOf() - value[6].valueOf() % 10) / 10),
          playerAddr: value[7].valueOf(),
          playerName: web3.toAscii(value[8].valueOf()),
          whales: Number(value[9].valueOf()),
          bears: Number(value[10].valueOf()),
          sneks: Number(value[11].valueOf()),
          bulls: Number(value[12].valueOf()),
          airDropTracker: Number(value[13].valueOf() % 1000),
          airDropPot: Number((value[13].valueOf() - value[13].valueOf() % 1000) / 1000)
        };
        resolve(ret);
      }).catch(e => {
        console.log("getRoundInfo error: ", e);
        reject(e);
      });
    });
  },
};

window.sdk = sdk;

