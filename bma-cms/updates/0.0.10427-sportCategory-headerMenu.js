'use strict';

var keystone = require('../bma-betstone'),
  Brands = keystone.mongoose.model('brand'),
  apiManager = require('../lib/api');

exports = module.exports = function(next) {

  Brands.find().exec()
    .then(regenCache)
    .then(_ => next(), next);
  
  function regenCache(brands) {
    return Promise.all(
      brands.reduce((prev, curr) => {
        return prev.concat([
          apiManager.run('sportCategory', {
            brand: curr.brandCode
          }),
          apiManager.run('headerMenu', {
            brand: curr.brandCode
          })
        ]);
      }, [])
    );
  }
};
