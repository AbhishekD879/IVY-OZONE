'use strict';

const keystone = require('../bma-betstone');
const Brands = keystone.mongoose.model('brand');
const apiManager = require('../lib/api');


exports = module.exports = function(next) {
  Brands.find({}).select({ 'brandCode': 1, "_id": 0}).exec().then(callAPIs).then(() => next(), next);
};

function callAPIs(brands) {
  return Promise.all(brands.map(brand => {
    return apiManager.run('modularContent', {
      brand: brand.brandCode
    });
  }));
}