const keystone = require('../bma-betstone');
const BetReceiptBannerTabletModel = keystone.list('betReceiptBannerTablet').model;
const akamai = require('../bma-betstone/lib/akamai');
const Logger = require('../lib/logger');

const banners = [
  {
    "name": "Bet Receipt Tablet 1",
    "validityPeriodStart": "2016-12-29T10:21:51.000Z",
    "validityPeriodEnd": "2017-02-17T10:21:52.000Z"
  },
  {
    "name": "Bet Receipt Tablet 2",
    "validityPeriodStart": "2016-12-29T10:22:26.000Z",
    "validityPeriodEnd": "2066-12-29T10:22:26.000Z"
  }
]

function populateBanners() {
  return Promise.all(
    banners.map(item => {
      const m = new BetReceiptBannerTabletModel(item);
      return m.save();
    })
  )
}

function deleteBanners() {
  return new Promise((resolve, reject) => {
    akamai.delete('bma', 'api/bma/bet-receipt-banners', deleteErr => {
      akamai.forceCache('bma', ['api/bma/bet-receipt-banners'], cacheErr => {
        Logger.error('UPDATE-0.0.17456', 'cacheErr', cacheErr);
        if (!cacheErr) {
          resolve();
        } else {
          reject(cacheErr);
        }
      });
    });
  });
}


exports = module.exports = function(next) {
  deleteBanners()
    .then(populateBanners)
    .then(() => next(), next);
};

