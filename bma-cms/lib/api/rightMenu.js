const keystone = require('../../bma-betstone'),
  Q = require('q'),
  osFieldToKey = [
    { field: 'showOnlyOnIOS', key: 'ios' },
    { field: 'showOnlyOnAndroid', key: 'android' }
  ];

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
  const getMenuItems = function(brand) {
    brand = brand === 'retail' ? 'connect' : brand;
    const resultArr = [],
      deferred = Q.defer();

    function getUriLarge(item) {
      if (item.menuItemView === 'description') {
        return '';
      }
      return item.menuItemView !== 'description' && item.uriLarge !== undefined
          ? item.uriLarge.substr(6)
          : '/images/uploads/right_menu/default/default-156x156.png';
    }

    function getUriMedium(item) {
      if (item.menuItemView === 'description') {
        return '';
      }
      return item.menuItemView !== 'description' && item.uriMedium !== undefined
          ? item.uriMedium.substr(6)
          : '/images/uploads/right_menu/default/default-156x156.png';
    }

    function getUriSmall(item) {
      if (item.menuItemView === 'description') {
        return '';
      }
      return ((item.menuItemView !== 'description' && item.uriSmall !== undefined)
        ? item.uriSmall.substr(6)
        : '/images/uploads/right_menu/default/default-104x104.png');
    }

    keystone.list('rightMenu')
      .model.find({ $or: [ { brand: { $in: ['retail', 'connect'] } }, { showItemFor: { $ne: 'loggedOut' } } ] })
      .where({ brand })
      .where({ disabled: false })
      .sort('sortOrder')
      .exec()
      .then(rightMenuItems => {
        rightMenuItems.forEach((item, key) => {
          item.uriMedium = (item.uriMedium !== undefined && item.uriMedium === '') ? undefined : item.uriMedium;
          item.uriSmall = (item.uriSmall !== undefined && item.uriSmall === '') ? undefined : item.uriSmall;

          resultArr[key] = {};
          if (item.type === 'link') {
            resultArr[key].targetUri = (item.targetUri !== undefined) ? item.targetUri : '';
          } else {
            resultArr[key].buttonClass = (item.targetUri !== undefined) ? item.targetUri : '';
          }
          resultArr[key].linkTitle = (item.menuItemView !== 'icon' && item.linkTitle !== undefined)
            ? item.linkTitle
            : '';
          resultArr[key].uriLarge = getUriLarge(item);
          resultArr[key].uriMedium = getUriMedium(item);
          resultArr[key].uriSmall = getUriSmall(item);
          resultArr[key].section = item.section;
          resultArr[key].inApp = item.inApp;
          resultArr[key].type = item.type;
          resultArr[key].showItemFor = item.showItemFor;

          resultArr[key].showOnlyOnOS = osFieldToKey.reduce((prev, curr) => {
            return item[curr.field] ? prev.concat(curr.key) : prev;
          }, []);

          resultArr[key].qa = item.QA;
          resultArr[key].iconAligment = item.iconAligment;
          resultArr[key].disabled = item.disabled;
          resultArr[key].svg = item.svg;
          resultArr[key].svgId = item.svgId;
          resultArr[key].authRequired = item.authRequired;
          resultArr[key].systemID = item.systemID;
        });
        deferred.resolve(resultArr);
      }, err => {
        deferred.reject(err);
      });
    return deferred.promise;
  };

  return getMenuItems(options.brand);
};
