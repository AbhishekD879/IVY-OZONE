const keystone = require('../bma-betstone');
const apiManager = require('../lib/api');

exports = module.exports = function (next) {
  getBrandCodes()
    .then(brands => Promise.all(
      brands.map(brand => 
        apiManager.run('footerMenuV3', {
          brand: brand
        })
      )
    ))
    .then(() => next())
    .catch(next);
};

/**
 * Get brand codes
 * @returns {Promise}
 */
const getBrandCodes = () => {
  return new Promise((resolve, reject) => {
    keystone.list('brand').model.find({}, { brandCode: 1 }).exec()
      .then(brands => brands.map(brand => brand.brandCode))
      .then(resolve, reject);
  });
};
