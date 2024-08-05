const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  const brand = options.brand === 'retail' ? 'connect' : options.brand;
  const subQuery = { brand };

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
   * Get Promotions
   * Get list of available promotions
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getPromotions() {
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
      const count = (config.structure.Promotions && config.structure.Promotions.expandedAmount)
        ? config.structure.Promotions.expandedAmount
        : 2;
      keystone.list('promotions')
        .model.find()
        .where(subQuery)
        .where({ disabled: false })
        .where('validityPeriodEnd')
        .gt(currentDate)
        .sort('sortOrder')
        .exec()
        .then(promotionsItems => {
          resultArr.expandedAmount = count;
          resultArr.promotions = [];
          promotionsItems.forEach((item, key) => {
            resultArr.promotions[key] = {};
            resultArr.promotions[key].title = item.title;
            resultArr.promotions[key].requestId = item.requestId;
            resultArr.promotions[key].promoKey = item.promoKey;
            resultArr.promotions[key].shortDescription = item.shortDescription;
            resultArr.promotions[key].description = item.description;
            resultArr.promotions[key].filename = item.filename.filename;
            resultArr.promotions[key].validityPeriodStart = item.validityPeriodStart;
            resultArr.promotions[key].validityPeriodEnd = item.validityPeriodEnd;
            resultArr.promotions[key].uriMedium = getUriMedium(item);
            resultArr.promotions[key].useDirectFileUrl = item.useDirectFileUrl;
            resultArr.promotions[key].directFileUrl = item.directFileUrl;
            resultArr.promotions[key].isSignpostingPromotion = item.isSignpostingPromotion;
            resultArr.promotions[key].eventLevelFlag = item.eventLevelFlag;
            resultArr.promotions[key].marketLevelFlag = item.marketLevelFlag;
            resultArr.promotions[key].overlayBetNowUrl = item.overlayBetNowUrl;
            resultArr.promotions[key].widthMedium = item.widthMedium;
            resultArr.promotions[key].heightMedium = item.heightMedium;
            resultArr.promotions[key].disabled = item.disabled;
            resultArr.promotions[key].showToCustomer = item.showToCustomer !== 'both'
              ? [item.showToCustomer]
              : ['new', 'existing'];
            resultArr.promotions[key].htmlMarkup = item.htmlMarkup;
            resultArr.promotions[key].promotionText = item.promotionText;
            resultArr.promotions[key].vipLevels = Array.isArray(item.vipLevels) ? item.vipLevels : [];
          });
          deferred.resolve(resultArr);
        }, err => {
          deferred.reject(err);
        });
      return deferred.promise;
    });
  }

  return getPromotions();
};
