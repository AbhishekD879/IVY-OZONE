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
  function getLeagues(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('ycLeague')
        .model.find({ brand })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              typeId: item.typeId,
              name: item.name,
              enabled: item.enabled
            })));
          },
          reject
        );
    });
  }

  return getLeagues(options.brand);
};
