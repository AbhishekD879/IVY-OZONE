'use strict';
const keystone = require('../../bma-betstone');

exports = module.exports = function(options) {
  /**
   * Get list of SSO items by brand and OS
   * @returns {Promise}
   */
  const getSSOItems = (brand, os) => {
    brand = brand === 'retail' ? 'connect' : brand;
    function osPredicate(resultIOS, resultAndroid) {
      if (os === 'ios') return resultIOS;
      if (os === 'android') return resultAndroid;
      return '';
    }

    return new Promise((resolve, reject) => {
      keystone.list('ssoPage')
        .model.find()
        .where(
          Object.assign(
            { brand, disabled: false },
            osPredicate({ showOnIOS: true }, { showOnAndroid: true })
          )
        )
        .sort('sortOrder')
        .exec()
        .then(
          ssoItems => {
            resolve(
              ssoItems.map(item => {
                return {
                  target: osPredicate(item.targetIOS, item.targetAndroid),
                  title: item.title,
                  uriMedium: item.uriMedium,
                  openLink: item.openLink
                };
              })
            );
          },
          reject
        );
    });
  };

  return getSSOItems(options.brand, options.osType);
};
