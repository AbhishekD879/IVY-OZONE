'use strict';

const keystone = require('../../bma-betstone'),
  _ = require('underscore'),
  utils = require('../utils');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = options => {
  const subQuery = { brand: options.brand },
    pickFields = [
      'id',
      'alt',
      'imageTitle',
      'targetUri',
      'link',
      'validityPeriodStart',
      'validityPeriodEnd',
      'widthMedium',
      'heightMedium',
      'widthSmall',
      'heightSmall',
      'disabled',
      'inApp',
      'enabled',
      'desktop_enabled',
      'desktop_inApp',
      'desktop_targetUri',
      'desktop_widthMedium',
      'desktop_heightMedium',
      'desktop_widthSmall',
      'desktop_heightSmall',
      'signpostingEventLevel',
      'signpostingMarketLevel'
    ];

  function uriMapper(uri) {
    if (_.isString(uri)) {
      return uri.indexOf('public') !== -1 ? uri.substr(6) : uri;
    }
    return '';
  }

  /**
   * Get unique id for appropriate sportCategory
   *
   * @returns {*|promise}
   */
  function getId(targetUri) {
    return utils.promisify(
      keystone.list('sportCategory')
        .model.find()
        .where('targetUri')
        .in(['default', new RegExp(`^${targetUri}`, 'i')])
        .exec()
    );
  }

  function bannerMapper(item) {
    return {
      filename: item.filename.filename,
      desktop_filename: item.desktop_filename.filename,
      uriMedium: uriMapper(item.uriMedium),
      uriSmall: uriMapper(item.uriSmall),
      desktop_uriMedium: uriMapper(item.desktop_uriMedium),
      desktop_uriSmall: uriMapper(item.desktop_uriSmall),
      showToCustomer: item.showToCustomer !== 'both' ? [item.showToCustomer] : ['new', 'existing'],
      vipLevels: Array.isArray(item.vipLevels) ? item.vipLevels : [],
      signpostingEventLevel: item.signpostingEventLevel,
      signpostingMarketLevel: item.signpostingMarketLevel
    };
  }

  /**
   * Get Banners
   * Get list of available banners by category id
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getBanners(categories) {
    return _.isEmpty(categories)
      ? Promise.resolve([])
      : utils.promisify(
      keystone.list('banners')
        .model.find()
        .where(subQuery)
        .where({ disabled: false })
        .where('categoryId')
        .in(_.pluck(categories, 'id'))
        .where('validityPeriodEnd')
        .gt(new Date())
        .sort('sortOrder')
        .exec()
    ).then(utils.entitiesMapper(pickFields, bannerMapper));
  }
  return getId(options.categoryUri).then(getBanners);
};
