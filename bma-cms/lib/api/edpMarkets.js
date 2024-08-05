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
  function getMarkets(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('edpMarket')
        .model.find({ brand })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              name: item.name,
              marketId: item.marketId,
              lastItem: item.lastItem
            })));
          },
          reject
        );
    });
  }

  return getMarkets(options.brand);
};
