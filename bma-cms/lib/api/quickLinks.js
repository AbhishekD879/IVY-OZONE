const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get quick links
   *
   * @param {string} brand
   * @param {String} raceType
   * @returns {*|promise}
     */
  function getQuickLinks(brand, raceType) {
    const deferred = Q.defer(),
      quickLinks = [],
      currentDate = new Date();

    keystone.list('quickLink')
      .model.find({ brand })
      .where({ disabled: false })
      .where('raceType')
      .equals(raceType)
      .where('validityPeriodEnd')
      .gt(currentDate)
      .sort('sortOrder')
      .exec((err, items) => {
        if (err) {
          deferred.reject(err);
        } else {
          items.forEach(item => {
            quickLinks.push({
              title: item.title,
              body: item.body,
              linkType: item.linkType,
              target: item.target,
              raceType: item.raceType,
              validityPeriodStart: item.validityPeriodStart,
              validityPeriodEnd: item.validityPeriodEnd,
              iconUrl: item.uriMedium,
              iconLargeUrl: item.uriLarge
            });
          });

          deferred.resolve(quickLinks);
        }
      });

    return deferred.promise;
  }

  return getQuickLinks(options.brand, options.raceType);
};
