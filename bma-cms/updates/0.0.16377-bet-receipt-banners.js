const keystone = require('../bma-betstone');
const BetReceiptBannerModel = keystone.list('betReceiptBanner').model;

const banners = [
  {
    "name": "Bet Receipt Banner1",
    "validityPeriodStart": "2016-12-29T10:21:51.000Z",
    "validityPeriodEnd": "2017-02-17T10:21:52.000Z"
  },
  {
    "name": "Bet receipt Banner 2",
    "validityPeriodStart": "2016-12-29T10:22:26.000Z",
    "validityPeriodEnd": "2066-12-29T10:22:26.000Z"
  }
]

function populateBanners() {
  return Promise.all(
    banners.map(item => {
      const m = new BetReceiptBannerModel(item);
      return new Promise((resolve, reject) => {
        m.save(err => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        })
      })
    })
  )
}

module.exports = next => populateBanners().then(_ => next(), next);

