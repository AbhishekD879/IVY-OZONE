'use strict';

const keystone = require('../../bma-betstone');
const _ = require('underscore');

/**
 * Get Footer Logos for Native app
 *
 * @param {string} brand
 * @returns {Promise}
 */
exports = module.exports = function getFooterLogosNative({ brand }) {
  return new Promise((resolve, reject) => {
    keystone.list('footerLogos')
      .model.find({ brand, disabled: false })
      .sort('sortOrder')
      .exec()
      .then(
        items => resolve(
          items.map(item => _.pick(item, ['title', 'target', 'uriMedium']))
        ),
        reject
      );
  });
};
