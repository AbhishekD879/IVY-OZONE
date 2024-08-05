'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get Bet Receipt banner
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getBanners(params) {
    return new Promise((resolve, reject) => {
      keystone.list(params.modelName)
        .model.find({
          brand: params.brand,
          disabled: false,
          validityPeriodEnd: { $gt: new Date() },
          validityPeriodStart: { $lt: new Date() }
        })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              id: item._id,
              name: item.name,
              uriMedium: item.uriMedium,
              useDirectFileUrl: item.useDirectFileUrl,
              directFileUrl: item.directFileUrl,
              validityPeriodStart: item.validityPeriodStart,
              validityPeriodEnd: item.validityPeriodEnd
            })));
          },
          reject
        );
    });
  }

  return getBanners(options);
};
