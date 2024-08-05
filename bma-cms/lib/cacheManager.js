'use strict';

const Q = require('q'),
  _ = require('underscore'),
  akamai = require('../bma-betstone/lib/akamai'),
  ReadWriteStream = require('./read-write-stream.js'),
  pushService = require('./pushService'),
  withoutForceCache = ['bannersV2', 'promotions', 'promotionsV2'],
  Logger = require('./logger');

/**
 * cacheManager constructor
 */
function CacheManager() {
  this.config = {
    path: 'caches',
    pathMapping: {
      bannersV2: '/api/v2/:brand/banners/:categoryUri',
      football3DBanners: '/api/:brand/3d-football-banners',
      betReceiptBanners: '/api/:brand/bet-receipt-banners/mobile',
      betReceiptBannersTablet: '/api/:brand/bet-receipt-banners/tablet',
      leagues: '/api/:brand/leagues',
      ycLeagues: '/api/:brand/yc-leagues',
      ycMarkets: '/api/:brand/yc-markets',
      ycStaticBlock: '/api/:brand/yc-static-block',
      edpMarkets: '/api/:brand/edp-markets',
      countries: '/api/:brand/countries-settings',
      headerMenu: '/api/:brand/header-menu',
      footerMenuV2: '/api/v2/:brand/footer-menu/:deviceType',
      footerMenuV3: '/api/v3/:brand/footer-menu',
      bottomMenu: '/api/:brand/bottom-menu',
      connectMenu: '/api/:brand/connect-menu',
      promotions: '/api/:brand/promotions',
      initSignposting: '/api/:brand/init-signposting',
      features: '/api/:brand/features',
      promotionsV2: '/api/v2/:brand/promotions/:categories',
      rightMenu: '/api/:brand/right-menu',
      sportCategory: '/api/:brand/sport-category',
      sportCategoryNative: '/api/:brand/sport-category-native',
      sports: '/api/:brand/sports',
      staticBlock: '/api/:brand/static-block/:uri',
      systemConfiguration: '/api/:brand/system-configuration',
      topGames: '/api/:brand/top-games',
      topMenu: '/api/:brand/top-menu',
      userMenu: '/api/:brand/user-menu',
      modularContent: '/api/:brand/modular-content',
      offersV2: '/api/v2/:brand/offers/:deviceType',
      seoPages: '/api/:brand/seo-pages',
      seoPage: '/api/:brand/seo-page/:id',
      seoSitemap: '/api/:brand/seo-sitemap',
      quickLinks: '/api/:brand/quick-links/:raceType',
      desktopQuickLinks: '/api/:brand/desktop-quick-links',
      widgets: '/api/:brand/widgets',
      ssoPage: '/api/:brand/sso-page/:osType',
      initialData: '/api/:brand/initial-data/:deviceType',
      maintenancePage: '/api/:brand/maintenance-page/:deviceType',
      footerLogosNative: '/api/:brand/footer-logos-native'
    }
  };
}

/**
 * Promise for caching JSON by key and options
 * useful for API Manager
 * this promise saves cache in 'deferred' mode (means in another thread) to prevent API slowdown
 * @param {string} key – pathMapping key
 * @param {object} options – options for route from pathMapping
 * @returns {*|promise}
 */
CacheManager.prototype.cacheJSONByKey = function(key, options) {
  const self = this;

  function cacheJSONPromise(json) {
    const deferred = Q.defer();

    deferred.resolve(json);

    process.nextTick(() => {
      const url = buildUrl(self.config.pathMapping[key], options);

      if (options.brand === 'bma' && key === 'modularContent') {
        // we need only Featured tab here
        pushService.push('featured', [_.findWhere(json, { directiveName: 'Featured' }), _.last(json)]);
      }

      self.cacheJSONbyUrl(options.brand, url, json, withoutForceCache.indexOf(key) !== -1);
    });

    return deferred.promise;
  }

  return cacheJSONPromise;
};

/**
 * Cache JSON to file depending on url
 * @param {String} url
 * @param {String} json
 * @returns {*|promise}
 */
CacheManager.prototype.cacheJSONbyUrl = function(brand, url, json, doNotForceCache) {
  const deferred = Q.defer(),
    filepath = url,
    stream = new ReadWriteStream();

  stream.write(JSON.stringify(json), 'utf-8');
  stream.end('');

  stream.on('finish', () => {
    Logger.info('CACHE', 'stream finished');
  });

  stream.on('error', err => {
    Logger.error('CACHE', 'stream errored', 'err');
    deferred.reject(err);
  });

  let transferredData = new Buffer('');
  stream.on('data', data => {
    transferredData = Buffer.concat(
      [transferredData, data],
      transferredData.length + data.length
    );
  });

  akamai.upload(brand, stream, filepath, uploadError => {
    if (doNotForceCache && !uploadError) {
      Logger.info('AKAMAI', filepath, transferredData.toString());
    } else if (!uploadError) {
      Logger.info('AKAMAI', filepath, transferredData.toString());
      akamai.forceCache(brand, [filepath], err => {
        if (!err) {
          deferred.resolve();
        } else {
          deferred.reject(err);
        }
      });
    } else {
      deferred.reject(uploadError);
    }
  });

  return deferred.promise;
};

/**
 * manually remove cache
 * @param {string} key – pathMapping key
 * @param {object} options – options for route from pathMapping
 * @returns {*|promise}
 */
CacheManager.prototype.removeCache = function(key, options) {
  const self = this,
    deferred = Q.defer(),
    filepath = buildUrl(self.config.pathMapping[key], options);

  akamai.delete(options.brand, filepath, deleteErr => {
    if (deleteErr) {
      deferred.reject(deleteErr);
    } else {
      akamai.forceCache(options.brand, [filepath], err => {
        if (!err) {
          deferred.resolve();
        } else {
          deferred.reject(err);
        }
      });
    }
  });

  return deferred.promise;
};

exports = module.exports = new CacheManager();

/**
 * Function for building url by route and options
 * @param {string} route
 * @param {object} options
 * @returns {string}
 */
function buildUrl(route, options) {
  let url = route;
  _.each(options, (value, key) => {
    url = url.replace(new RegExp(`:${key}`, 'g'), value);
  });

  return url;
}
