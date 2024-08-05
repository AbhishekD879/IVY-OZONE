const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Static Blocks URLs.
   * Get array of all URLs configured in SEO section
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getSEOPage = function(brand, id) {
    const deferred = Q.defer();
    keystone.list('seoPage')
      .model.findOne({ brand, _id: id }).exec()
      .then(page => {
        deferred.resolve({
          id: page._id,
          title: page.title,
          url: page.url,
          description: page.description,
          staticBlock: page.staticBlock
        });
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  };

  return getSEOPage(options.brand, options.id);
};
