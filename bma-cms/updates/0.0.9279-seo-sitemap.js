'use strict';

const keystone = require('../bma-betstone');
const Brands = keystone.mongoose.model('brand');
const apiManager = require('../lib/api');

exports = module.exports = (next) => {
  getBrands()
    .then(brands => Promise.all(
      brands.map(brand => apiManager.run('seoSitemap', { brand: brand.brandCode }))
    ))
    .then(() => next())
    .catch(next);
};

const getBrands = () => {
  return new Promise((resolve, reject) => {
    Brands.find({}, { brandCode: 1}).exec().then(resolve, reject);
  });
};
