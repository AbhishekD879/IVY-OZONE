'use strict';
const keystone = require('../../bma-betstone');

exports = module.exports = function(options) {
  /**
   * Get Menu Items
   * Get list of footer menu items
   * @returns {Promise}
   */
  const getMenuItems = brand => {
    function getItemTarget(item) {
      if (item.itemType === 'link') {
        return (item.targetUri !== undefined) ? item.targetUri : '';
      }
      return undefined;
    }

    return new Promise((resolve, reject) => {
      keystone.list('footerMenu')
        .model.find()
        .where({ brand, disabled: false })
        .sort('sortOrder')
        .exec()
        .then(
          footerMenuItems => {
            const result = footerMenuItems
              .reduce((prev, curr) => {
                if (
                  (prev.mobile < 5 && curr.mobile) ||
                  (prev.tablet < 5 && curr.tablet) ||
                  (prev.desktop < 5 && curr.desktop)
                ) {
                  prev.items.push(curr);

                  prev.mobile += curr.mobile ? 1 : 0;
                  prev.tablet += curr.tablet ? 1 : 0;
                  prev.desktop += curr.desktop ? 1 : 0;
                }

                return prev;
              }, { mobile: 0, tablet: 0, desktop: 0, items: [] })
              .items.map(item => {
                const device = [];

                if (item.mobile) {
                  device.push('m');
                }

                if (item.tablet) {
                  device.push('t');
                }

                if (item.desktop) {
                  device.push('d');
                }

                return {
                  target: getItemTarget(item),
                  title: item.linkTitle !== undefined ? item.linkTitle : '',
                  image: item.uriSmall !== undefined ? item.uriSmall.substr(6) : undefined,
                  imageLarge: item.uriLarge !== undefined ? item.uriLarge.substr(6) : undefined,
                  inApp: item.itemType === 'link' ? item.inApp : undefined,
                  showItemFor: item.showItemFor,
                  widget: item.itemType === 'widget' ? item.widgetName : undefined,
                  svg: item.svg ? item.svg : undefined,
                  svgId: item.svgId ? item.svgId : undefined,
                  authRequired: item.authRequired,
                  systemID: item.systemID,
                  device
                };
              });

            resolve(result);
          },
          reject
        );
    });
  };

  return getMenuItems(options.brand);
};
