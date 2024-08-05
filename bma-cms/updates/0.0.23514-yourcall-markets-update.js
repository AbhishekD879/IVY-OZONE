const keystone = require('../bma-betstone');
const YCMarketModel = keystone.list('ycMarket').model;
const markets = [
  {
    "name": "Match Result",
    "dsMarket": "Outcome"
  },
  {
    "name": "Player Bets",
    "dsMarket": "Player Bets"
  },
  {
    "name": "Both Teams to Score",
    "dsMarket": "Both score"
  },
  {
    "name": "Over/Under Goals",
    "dsMarket": "Total goals"
  },
  {
    "name": "Over/Under Corners",
    "dsMarket": "Total corners"
  },
  {
    "name": "Over/Under Booking Points",
    "dsMarket": "Total booking points"
  },
  {
    "name": "Player to be carded",
    "dsMarket": "Cards"
  },
  {
    "name": "Anytime Goalscorer",
    "dsMarket": "Goals"
  }
];

function deleteMarkets() {
  return YCMarketModel.find()
    .exec()
    .then(items =>
      Promise.all(items.map(item => {
        return YCMarketModel.remove();
      })));
}

function populateMarkets() {
  return Promise.all(
    markets.map(item => {
      const m = new YCMarketModel(item);
      return m.save();
    })
  )
}

exports = module.exports = function(next) {
  deleteMarkets()
    .then(populateMarkets)
    .then(() => next(), next);
};
