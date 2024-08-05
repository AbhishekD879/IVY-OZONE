'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get app quick links
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getDesktopQuickLinks(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('Desktop QuickLink')
        .model.find({ brand, disabled: false })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              title: item.title,
              target: item.target,
              uriMedium: item.uriMedium,
              uriLarge: item.uriLarge
            })));
          },
          reject
        );
    });
  }

  return getDesktopQuickLinks(options.brand);
};
