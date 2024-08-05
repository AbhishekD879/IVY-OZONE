const keystone = require('../bma-betstone'),
  _ = require('underscore'),
  Brands = keystone.list('brand').model,
  Widget = keystone.list('widget').model;


const widgets = [{
  title: 'Cash Out',
  type: 'cashout'
}, {
  title: 'Next Races',
  type: 'next-races'
}, {
  title: 'In-Play',
  type: 'in-play'
}, {
  title: 'Favorites',
  type: 'favourites'
}, {
  title: 'LIVE Stream',
  type: 'stream'
}, {
  title: 'Mini Games',
  type: 'mini-games'
}, {
  title: 'Offer Modules',
  type: 'offers'
}, {
  title: 'Bet Slip',
  type: 'betslip'
}];

function buildWidgets(brands) {
  var result = brands.map(brand => {
    return widgets.map((widget, i) => {
      var newWidget = _.clone(widget);
      newWidget.brand = brand.brandCode;
      newWidget.sortOrder = i;
      return newWidget;
    })
  });
  return _.flatten(result);
}

module.exports = next => {
  return Brands.find({}).exec()
    .then(brands => {
      return Promise.all(
        buildWidgets(brands).map(widget => {
          var w = new Widget(widget);
          return new Promise((resolve, reject) => {
            w.save(err => {
              if (err) {
                reject(err);
              } else {
                resolve();
              }
            })
          })
        })
      )
    })
    .then(_ => next(), next);
};

