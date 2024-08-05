const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Menu Items
   * Get list of left menu items
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getMenuItems = function(brand, deviceType) {
    const resultArr = [],
      deferred = Q.defer(),
      deviceTypeWhereClause = {},
      isUnsupportedDevice = ['mobile', 'tablet', 'desktop'].indexOf(deviceType) === -1,
      isDesktop = deviceType === 'desktop',
      deviceTypeFinal = isUnsupportedDevice ? 'mobile' : deviceType,
      itemsNumber = ['rcomb', 'connect'].includes(brand) ? 6 : 5;

    deviceTypeWhereClause[deviceTypeFinal] = true;

    keystone.list('footerMenu')
      .model.find()
      .where({ brand })
      .where({ disabled: false })
      .where(deviceTypeWhereClause)
      .sort('sortOrder')
      .exec()
      .then(footerMenuItems => {
        const menuList = isDesktop ? footerMenuItems : footerMenuItems.slice(0, itemsNumber);
        menuList.forEach((item, key) => {
          item.uriSmall = (item.uriSmall !== undefined && item.uriSmall === '') ? undefined : item.uriSmall;
          item.uriLarge = (item.uriLarge !== undefined && item.uriLarge === '') ? undefined : item.uriLarge;

          resultArr[key] = {};
          resultArr[key].targetUri = (item.targetUri !== undefined) ? item.targetUri : '';
          resultArr[key].linkTitle = item.linkTitle !== undefined ? item.linkTitle : '';
          resultArr[key].uriSmall = item.uriSmall !== undefined ? item.uriSmall.substr(6) : '';
          resultArr[key].uriLarge = item.uriLarge !== undefined ? item.uriLarge.substr(6) : '';
          resultArr[key].inApp = item.inApp;
          resultArr[key].showItemFor = item.showItemFor;
          resultArr[key].disabled = item.disabled;
          resultArr[key].svg = item.svg ? item.svg : undefined;
          resultArr[key].svgId = item.svgId ? item.svgId : undefined;
          resultArr[key].authRequired = item.authRequired;
          resultArr[key].systemID = item.systemID;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getMenuItems(options.brand, options.deviceType);
};
