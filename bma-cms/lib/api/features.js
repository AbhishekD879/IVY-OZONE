const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  const subQuery = { brand: options.brand };

  /**
   * Get System Configuration
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getSystemConfig() {
    const deferred = Q.defer();
    // Load the Module Structure Type model
    keystone.mongoose.model('Structure')
      .findOne()
      .where(subQuery)
      .exec()
      .then(model => {
        deferred.resolve(model);
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  }

  /**
   * Get Features
   * Get list of available features
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getFeatures() {
    const deferred = Q.defer(),
      resultArr = {},
      currentDate = new Date();

    function getUriMedium(item) {
      if (item.uriMedium !== undefined) {
        return item.uriMedium.indexOf('public') !== -1 ? item.uriMedium.substr(6) : item.uriMedium;
      }
      return '';
    }

    return getSystemConfig().then(config => {
      const count = (config.structure.Features && config.structure.Features.expandedAmount)
        ? config.structure.Features.expandedAmount
        : 2;
      keystone.list('features')
        .model.find()
        .where(subQuery)
        .where({ disabled: false })
        .where('validityPeriodEnd')
        .gt(currentDate)
        .sort('sortOrder')
        .exec()
        .then(featuresItems => {
          resultArr.expandedAmount = count;
          resultArr.features = [];
          featuresItems.forEach((item, key) => {
            resultArr.features[key] = {};
            resultArr.features[key].title = item.title;
            resultArr.features[key].shortDescription = item.shortDescription;
            resultArr.features[key].description = item.description;
            resultArr.features[key].filename = item.filename.filename;
            resultArr.features[key].validityPeriodStart = item.validityPeriodStart;
            resultArr.features[key].validityPeriodEnd = item.validityPeriodEnd;
            resultArr.features[key].uriMedium = getUriMedium(item);
            resultArr.features[key].widthMedium = item.widthMedium;
            resultArr.features[key].heightMedium = item.heightMedium;
            resultArr.features[key].disabled = item.disabled;
            resultArr.features[key].showToCustomer = item.showToCustomer !== 'both'
              ? [item.showToCustomer]
              : ['logged-in', 'logged-out'];
          });
          deferred.resolve(resultArr);
        }, err => {
          deferred.reject(err);
        });
      return deferred.promise;
    });
  }

  return getFeatures();
};
