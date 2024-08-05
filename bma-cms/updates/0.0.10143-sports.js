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
 * regen Sports API cache for selected brand
 * @param {String} brand
 * @returns {Promise}
 */
function regenCache (brand) {
  return apiManager.run('sports', {
    brand: brand
  })
}
