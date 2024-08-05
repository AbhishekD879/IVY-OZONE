'use strict';

var keystone = require('../bma-betstone');
var apiManager = require('../lib/api');

exports = module.exports = function(next) {
  keystone.list('brand').model.find({}, {brandCode: true, _id: false})
    .exec()
    .then(brands => Promise.all(brands.map(brand => regenCache(brand.brandCode))))
    .then(_ => next(), next);
};

/**
 * regen QuickLinks API cache for selected brand
 * @param {String} brand
 * @returns {Promise}
 */
function regenCache (brand) {
  return Promise.all(
    ['horseracing', 'greyhound'].map(
      raceType => apiManager.run('quickLinks', {
        brand: brand,
        raceType: raceType
      })
    )
  );
}
