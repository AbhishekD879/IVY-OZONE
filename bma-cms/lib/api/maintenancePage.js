'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get Maintenance page
   *
   * @param {string} brand
   * @param {string} deviceType
   * @returns {Promise} Resolves with {Object} or {Null}
   */
  function getMaintenancePage(brand, deviceType) {
    const deviceTypeWhereClause = {},
      isUnsupportedDevice = ['mobile', 'tablet', 'desktop'].indexOf(deviceType) === -1,
      deviceTypeFinal = isUnsupportedDevice ? 'mobile' : deviceType;

    deviceTypeWhereClause[deviceTypeFinal] = true;

    return new Promise((resolve, reject) => {
      keystone.list('maintenancePage')
        .model.find({ brand })
        .where(deviceTypeWhereClause)
        .where('validityPeriodEnd')
        .gt(new Date())
        .sort('validityPeriodStart')
        .exec()
        .then(
          items => {
            const result = items
                .map(item => ({
                  name: item.name,
                  uriMedium: item.uriMedium,
                  uriOriginal: item.uriOriginal,
                  targetUri: item.targetUri,
                  validityPeriodStart: item.validityPeriodStart,
                  validityPeriodEnd: item.validityPeriodEnd
                }));
            resolve(result);
          },
          reject
        );
    });
  }

  return getMaintenancePage(options.brand, options.deviceType);
};
