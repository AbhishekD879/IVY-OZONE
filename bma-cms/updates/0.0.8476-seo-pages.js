'use strict';

const keystone = require('../bma-betstone');
const SEOPages = keystone.mongoose.model('seoPage');
const Brands = keystone.mongoose.model('brand');
const apiManager = require('../lib/api');
const cacheManager = require('../lib/cacheManager');


exports = module.exports = function(next) {
  cacheSEOPages()
    .then(cacheSEOPage)
    .then(() => next(), next);
};

function cacheSEOPages() {
  return Brands.find({}, { brandCode: 1 }).exec()
    .then(brands => {
      return Promise.all(brands.map(brand => {
        return apiManager.run('seoPages', {
          brand: brand.brandCode
        });
      }))
    })
}

function cacheSEOPage() {
  return SEOPages.find({ disabled: false }, { brand: 1, _id: 1 }).exec()
    .then(pages => {
      return Promise.all(pages.map(page => {
        return apiManager.run('seoPage', {
          brand: page.brand,
          id: page._id
        });
      }));
    })
}
