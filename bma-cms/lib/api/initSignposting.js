'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get Signposting Promotions
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getSignpostingPromotions(brand) {
    const currentDate = new Date();

    return new Promise((resolve, reject) => {
      keystone.list('promotions')
        .model.find({ brand })
        .where({ disabled: false })
        .where({ isSignpostingPromotion: true })
        .where('validityPeriodEnd')
        .gt(currentDate)
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              title: item.title,
              requestId: item.requestId,
              promoKey: item.promoKey,
              eventLevelFlag: item.eventLevelFlag,
              marketLevelFlag: item.marketLevelFlag,
              showToCustomer: item.showToCustomer !== 'both'
                ? [item.showToCustomer]
                : ['new', 'existing'],
              vipLevels: item.vipLevels,
              promotionText: item.promotionText
            })));
          },
          reject
        );
    });
  }

  return getSignpostingPromotions(options.brand);
};
