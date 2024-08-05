'use strict';

const
  clone = require('underscore').clone,
  apiManager = require('./index'),
  cacheManager = require('../../lib/cacheManager'),
  timer = {},
  Logger = require('../logger');

function runApi(apiKey, options) {
  return apiManager.run(apiKey, options, true);
}

/**
 * @param brand
 * @param deviceType {String|null}
 * @returns {Promise<Object>}
 * Collect all responses from API endpoints
 */
function getInitialData(brand, deviceType) {
  return Promise.all([
    runApi('staticBlock', { uri: 'global-footer', brand }),
    runApi('staticBlock', { uri: 'footer-markup-top', brand }),
    runApi('staticBlock', { uri: 'footer-markup-bottom', brand }),
    runApi('staticBlock', { uri: 'freebet-msg-en-us', brand }),
    runApi('footerLogos', { brand }),
    runApi('sportCategory', { brand }),
    runApi('sports', { brand }),
    runApi('bottomMenu', { brand }),
    runApi('modularContent', { brand }),
    runApi('seoPages', { brand }),
    runApi('footerMenuV2', { brand, deviceType }),
    runApi('initSignposting', { brand }),
    runApi('systemConfiguration', { brand })
  ]).then(
    ([globalFooter, footerMarkupTop, footerMarkupBottom, freebetMsg, footerLogos,
      sportCategories, sports, bottomMenu, modularContent, seoPages, footerMenu, initSignposting, systemConfiguration]) => {

      modularContent.forEach(element => {
        if (element.modules) {
          delete element.modules;
        }
      });

      return Promise.resolve({
        globalFooter,
        footerMarkupTop: footerMarkupTop.htmlMarkup,
        footerMarkupBottom: footerMarkupBottom.htmlMarkup,
        freebetMsg: freebetMsg.htmlMarkup,
        footerLogos,
        sportCategories,
        sports,
        bottomMenu,
        modularContent,
        seoPages,
        footerMenu,
        initSignposting,
        systemConfiguration
      });
    }
  );
}

/*
  Throttle cache regeneration of initial data. Especially relevant in case of migrations,
  when regenCache can be triggered many times in a row.
 */
function regenCache(brand) {
  if (timer[brand]) {
    clearTimeout(timer[brand]);
  }
  timer[brand] = setTimeout(() => regenCacheByBrand(brand), 1000 * 5);
}

/**
 * Refresh cache for initialData. Should be used in models.
 * @param brand
 */
function regenCacheByBrand(brand) {
  getInitialData(brand, null)
    .then(initialData => {
      return Promise.all(
        ['mobile', 'tablet', 'desktop'].map(deviceType => {
          return runApi('footerMenuV2', { brand, deviceType })
            .then(footerMenu => {
              const initialDataCopy = clone(initialData);
              initialDataCopy.footerMenu = footerMenu;
              return cacheManager.cacheJSONByKey('initialData', { brand, deviceType })(initialDataCopy);
            });
        })
      );
    })
    .catch(error => {
      Logger.info('INITIAL_DATA_MANAGER', 'Cache generation error', error);
    });
}

exports = module.exports = {
  getInitialData,
  regenCache
};
