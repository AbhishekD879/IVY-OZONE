'use strict';

var keystone = require('../bma-betstone'),
  Brands = keystone.mongoose.model('brand'),
  apiManager = require('../lib/api');

exports = module.exports = function(next) {

  Brands.find().exec()
    .then(brands => Promise.all(
      brands.map(brand => {
        return apiManager.run('sports', {
          brand: brand.brandCode
        })
      })
    ))
    .then(_ => next(), next);
};
