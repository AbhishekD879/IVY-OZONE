const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Menu Items
   * Get list of top menu items
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getMenuItems = function(brand) {
    const resultArr = [],
      deferred = Q.defer();

    keystone.list('topMenu')
      .model.find()
      .where({ brand })
      .where({ disabled: false })
      .sort('sortOrder')
      .exec()
      .then(topMenuItems => {
        topMenuItems.forEach((item, key) => {
          resultArr[key] = {};
          resultArr[key].linkTitle = item.linkTitle;
          resultArr[key].targetUri = item.targetUri;
          resultArr[key].disabled = item.disabled;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getMenuItems(options.brand);
};
