const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Static Blocks
   * Get list of all static blocks or one static block if uri provided
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getStaticBlock = function(brand, uri) {
    const deferred = Q.defer(),
      resultObj = {};

    keystone.list('staticBlock')
      .model.findOne()
      .where({ brand })
      .where({ enabled: true, uri })
      .exec()
      .then(blockHTML => {
        if (blockHTML !== null) {
          resultObj.title = blockHTML.title;
          resultObj.uri = blockHTML.uri;
          resultObj.htmlMarkup = blockHTML.htmlMarkup;
          resultObj.enabled = blockHTML.enabled;
          deferred.resolve(resultObj);
        } else {
          deferred.resolve({});
        }
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  };

  return getStaticBlock(options.brand, options.uri);
};
