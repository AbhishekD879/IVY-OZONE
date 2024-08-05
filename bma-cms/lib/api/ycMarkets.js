'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get Leagues
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getYCMarkets(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('ycMarket')
        .model.find({ brand })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              name: item.name,
              dsMarket: item.dsMarket
            })));
          },
          reject
        );
    });
  }

  return getYCMarkets(options.brand);
};
