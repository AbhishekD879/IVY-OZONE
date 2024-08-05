const keystone = require('../../bma-betstone'),
  Q = require('q');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get Menu Items
   * Get list of user menu items
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getMenuItems(brand) {
    const resultArr = [],
      deferred = Q.defer();

    keystone.list('userMenu')
      .model.find()
      .where({ brand })
      .where({ disabled: false })
      .sort('sortOrder')
      .exec()
      .then(userMenuItems => {
        userMenuItems.forEach((item, key) => {
          item.uriMedium = (item.uriMedium !== undefined && item.uriMedium === '') ? undefined : item.uriMedium;
          item.uriSmall = (item.uriSmall !== undefined && item.uriSmall === '') ? undefined : item.uriSmall;

          resultArr[key] = {};
          resultArr[key].targetUri = item.targetUri ? item.targetUri : 'my-account';
          resultArr[key].linkTitle = (item.linkTitle !== undefined) ? item.linkTitle : '';
          resultArr[key].uriMedium = (item.uriMedium !== undefined)
            ? item.uriMedium.substr(6)
            : '/images/uploads/right_menu/default/default-156x156.png';
          resultArr[key].uriSmall = (item.uriSmall !== undefined)
            ? item.uriSmall.substr(6)
            : '/images/uploads/right_menu/default/default-104x104.png';
          resultArr[key].activeIfLogout = item.activeIfLogout;
          resultArr[key].qa = item.QA;
          resultArr[key].disabled = item.disabled;
          resultArr[key].showUserMenu = item.showUserMenu;
          resultArr[key].svg = item.svg;
          resultArr[key].svgId = item.svgId;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  }

  return getMenuItems(options.brand);
};
