'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  /**
   * Get Leagues
   *
   * @param {string} brand
   * @returns {Promise}
   */
  function getLeagues(brand) {
    return new Promise((resolve, reject) => {
      keystone.list('league')
        .model.find({ brand })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => ({
              name: item.name,
              typeId: item.typeId,
              categoryId: item.categoryId,
              ssCategoryCode: item.ssCategoryCode,
              banner: item.banner,
              tabletBanner: item.tabletBanner,
              betBuilderUrl: item.betBuilderUrl,
              leagueUrl: item.leagueUrl,
              redirectionUrl: item.redirectionUrl
            })));
          },
          reject
        );
    });
  }

  return getLeagues(options.brand);
};
