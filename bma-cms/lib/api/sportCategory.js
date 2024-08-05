'use strict';

const keystone = require('../../bma-betstone');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Sport Categories
   * Get list of all sport categories
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getSportCategories = (brand, isNative) => {
    return new Promise((resolve, reject) => {
      keystone.list('sportCategory')
        .model.find()
        .where({ brand })
        .sort('sortOrder')
        .exec()
        .then(
          items => {
            resolve(items.map(item => {
              const responseItem = {
                alt: item.alt,
                imageTitle: item.imageTitle,
                categoryId: item.categoryId,
                ssCategoryCode: (item.ssCategoryCode !== undefined) ? item.ssCategoryCode : '',
                targetUri: item.targetUri,
                filename: item.filename.filename,
                uriMedium: (item.uriMedium !== undefined) ? item.uriMedium.substr(6) : '',
                uriLarge: (item.uriLarge !== undefined) ? item.uriLarge.substr(6) : '',
                widthMedium: item.widthMedium,
                heightLarge: item.heightMedium,
                widthLarge: item.widthMedium,
                heightMedium: item.heightMedium,
                uriSmall: (item.uriSmall !== undefined) ? item.uriSmall.substr(6) : '',
                widthSmall: item.widthSmall,
                heightSmall: item.heightSmall,
                disabled: item.disabled,
                showInPlay: item.showInPlay,
                showInHome: item.showInHome,
                showInAZ: item.showInAZ,
                uriSmallIcon: (item.uriSmallIcon !== undefined) ? item.uriSmallIcon.substr(6) : '',
                uriMediumIcon: (item.uriMediumIcon !== undefined) ? item.uriMediumIcon.substr(6) : '',
                uriLargeIcon: (item.uriLargeIcon !== undefined) ? item.uriLargeIcon.substr(6) : '',
                path: item.path,
                isTopSport: item.isTopSport,
                inApp: item.inApp,
                showScoreboard: item.showScoreboard,
                scoreBoardUrl: item.scoreBoardUrl
              };

              // Native client doesn't need svg icons
              if (!isNative) {
                responseItem.svg = item.svg;
                responseItem.svgId = item.svgId;
              }

              return responseItem;
            }));
          },
          reject
        );
    });
  };

  return getSportCategories(options.brand, options.isNative);
};
