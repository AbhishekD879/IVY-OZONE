const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get top games
   * Get list of top game
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getTopGames = function(brand) {
    const resultArr = [],
      deferred = Q.defer();

    keystone.list('topGames')
      .model.find()
      .where({ brand })
      .sort('sortOrder')
      .exec()
      .then(topGamesItems => {
        topGamesItems.forEach((item, key) => {
          resultArr[key] = {};
          resultArr[key].alt = item.alt;
          resultArr[key].imageTitle = item.imageTitle;
          resultArr[key].targetUri = item.targetUri;
          resultArr[key].filename = item.filename.filename;
          resultArr[key].uriMedium = (item.uriMedium !== undefined) ? item.uriMedium.substr(6) : '';
          resultArr[key].widthMedium = item.widthMedium;
          resultArr[key].heightMedium = item.heightMedium;
          resultArr[key].uriLarge = (item.uriLarge !== undefined) ? item.uriLarge.substr(6) : '';
          resultArr[key].widthLarge = item.widthLarge;
          resultArr[key].heightLarge = item.heightLarge;
          resultArr[key].uriSmall = (item.uriSmall !== undefined) ? item.uriSmall.substr(6) : '';
          resultArr[key].widthSmall = item.widthSmall;
          resultArr[key].heightSmall = item.heightSmall;
          resultArr[key].disabled = item.disabled;
          resultArr[key].showItemOn = item.showItemOn;
          resultArr[key].uriSmallIcon = (item.uriSmallIcon !== undefined) ? item.uriSmallIcon.substr(6) : '';
          resultArr[key].uriMediumIcon = (item.uriMediumIcon !== undefined) ? item.uriMediumIcon.substr(6) : '';
          resultArr[key].uriLargeIcon = (item.uriLargeIcon !== undefined) ? item.uriLargeIcon.substr(6) : '';
          resultArr[key].path = item.path;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getTopGames(options.brand);
};
