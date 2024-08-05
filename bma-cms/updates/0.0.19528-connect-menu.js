const keystone = require('../bma-betstone');
const menuModel = keystone.list('connectMenu').model;
const connectMenu = [
  {
    "linkTitle": "Home",
    "targetUri": "/connect"
  },
  {
    "linkTitle": "Benefits",
    "targetUri": "/connect/benefits"
  },
  {
    "linkTitle": "Offers",
    "targetUri": "/connect/offers"
  },
  {
    "linkTitle": "Sign up",
    "targetUri": "/connect/signup"
  },
  {
    "linkTitle": "Shop Locator",
    "targetUri": "/connect/shop-locator"
  },
  {
    "linkTitle": "FAQ",
    "targetUri": "/connect/faq"
  }
];

function populateMenu() {
  return Promise.all(
    connectMenu.map(item => {
      const m = new menuModel(item);
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

module.exports = next => populateMenu().then(_ => next(), next);
