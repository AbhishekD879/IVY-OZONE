const keystone = require('../bma-betstone');
const EDPMarketModel = keystone.list('edpMarket').model;
const markets = [
  {
    "name": "All Markets",
    "lastItem": false
  },
  {
    "name": "Main Markets",
    "lastItem": false
  },
  {
    "name": "Goal Markets",
    "lastItem": false
  },
  {
    "name": "YourCall",
    "lastItem": false
  },
  {
    "name": "Player Bets",
    "lastItem": false
  },
  {
    "name": "Goalscorer Markets",
    "lastItem": false
  },
  {
    "name": "Half Markets",
    "lastItem": false
  },
  {
    "name": "Score Markets",
    "lastItem": false
  },
  {
    "name": "Team Goals Markets",
    "lastItem": false
  },
  {
    "name": "Other Markets",
    "lastItem": true
  }
];

function populateMarkets() {
  return Promise.all(
    markets.map(item => {
      const m = new EDPMarketModel(item);
      return m.save();
    })
  )
}

module.exports = next => populateMarkets().then(_ => next(), next);

