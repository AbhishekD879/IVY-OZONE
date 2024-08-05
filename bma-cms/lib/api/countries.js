const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Countries
   * Get list of allowed countries
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getCountriesData = function(brand) {
    const responseData = [],
      deferred = Q.defer();
    keystone.mongoose.model('Countries').find({ brand })
      .exec()
      .then(countriesData => {
        if (!countriesData.length) {
          deferred.reject('no country found');
        } else {
          countriesData[0].countriesData.forEach(item => {
            if (item.allowed) {
              responseData.push({
                val: item.val,
                phoneAreaCode: item.phoneAreaCode,
                label: item.label
              });
            }
          });
          deferred.resolve(responseData);
        }
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getCountriesData(options.brand);
};
