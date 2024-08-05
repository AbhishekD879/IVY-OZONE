'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get 3D Football banners
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getBanners(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('football3DBanner')
        .model.find({ brand, disabled: false })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              name: item.name,
              uriMedium: item.uriMedium,
              displayDuration: item.displayDuration,
              validityPeriodStart: item.validityPeriodStart,
              validityPeriodEnd: item.validityPeriodEnd,
              shortDescription: item.shortDescription
            })));
          },
          reject
        );
    });
  }

  return getBanners(options.brand);
};
