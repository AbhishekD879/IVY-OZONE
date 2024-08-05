const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get array of all URLs configured in SEO section
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getSEOPages = function(brand) {
    const deferred = Q.defer(),
      result = {};

    keystone.list('seoPage').model
      .find({
        brand,
        disabled: false
      }).exec()
      .then(seoPages => {
        seoPages.forEach(seoPage => {
          result[seoPage.url] = seoPage._id;
        });
        deferred.resolve(result);
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  };

  return getSEOPages(options.brand);
};
