const keystone = require('../../bma-betstone'),
  Q = require('q');

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
  const getSports = function(brand) {
    const resultArr = [],
      deferred = Q.defer();

    keystone.list('sport')
      .model.find()
      .where({ brand })
      .sort('sortOrder')
      .exec()
      .then(sportItems => {
        sportItems.forEach((item, key) => {
          resultArr[key] = {};
          resultArr[key].alt = item.alt;
          resultArr[key].imageTitle = item.imageTitle;
          resultArr[key].categoryId = item.categoryId;
          resultArr[key].typeIds = (item.typeIds !== undefined && item.typeIds !== '') ? item.typeIds.split(',') : [];
          resultArr[key].ssCategoryCode = (item.ssCategoryCode !== undefined) ? item.ssCategoryCode : '';
          resultArr[key].targetUri = item.targetUri;
          resultArr[key].dispSortName = item.dispSortName.split(',');
          resultArr[key].primaryMarkets = item.primaryMarkets;
          resultArr[key].viewByFilters = ['byCompetitions', 'byTime'];
          resultArr[key].oddsCardHeaderType =
          {
            outcomesTemplateType1: item.outcomesTemplateType1,
            outcomesTemplateType2: item.outcomesTemplateType1,
            outcomesTemplateType3: item.outcomesTemplateType1
          };
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
          resultArr[key].showInPlay = item.showInPlay;
          resultArr[key].isOutrightSport = item.isOutrightSport;
          resultArr[key].isMultiTemplateSport = item.isMultiTemplateSport;
          resultArr[key].tabs = {
            'tab-live': item.tabLive,
            'tab-matches': item.tabMatches,
            'tab-outrights': item.tabOutrights,
            'tab-specials': item.tabSpecials
          };
          resultArr[key].defaultTab = item.defaultTab;
          resultArr[key].uriSmallIcon = (item.uriSmallIcon !== undefined) ? item.uriSmallIcon.substr(6) : '';
          resultArr[key].uriMediumIcon = (item.uriMediumIcon !== undefined) ? item.uriMediumIcon.substr(6) : '';
          resultArr[key].uriLargeIcon = (item.uriLargeIcon !== undefined) ? item.uriLargeIcon.substr(6) : '';
          resultArr[key].svg = item.svg;
          resultArr[key].svgId = item.svgId;
          resultArr[key].inApp = item.inApp;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getSports(options.brand);
};
