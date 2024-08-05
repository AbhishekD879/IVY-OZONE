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
  function getYCStaticBlock(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('ycStaticBlock')
        .model.find({ brand, enabled: true })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              title: item.title,
              htmlMarkup: item.htmlMarkup
            })));
          },
          reject
        );
    });
  }

  return getYCStaticBlock(options.brand);
};
