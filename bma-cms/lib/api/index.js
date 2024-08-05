const cacheManager = require('../cacheManager');

/**
 * API Manager Constructor
 */
function ApiManager() {
  this.apis = {
    bannersV2: require('./bannersV2'),
    football3DBanners: require('./football3Dbanners'),
    betReceiptBanners: require('./betReceiptBanners'),
    betReceiptBannersTablet: require('./betReceiptBanners'),
    leagues: require('./leagues'),
    ycLeagues: require('./ycLeagues'),
    ycMarkets: require('./ycMarkets'),
    ycStaticBlock: require('./ycStaticBlock'),
    edpMarkets: require('./edpMarkets'),
    countries: require('./countries'),
    headerMenu: require('./headerMenu'),
    connectMenu: require('./connectMenu'),
    footerMenuV2: require('./footerMenuV2'),
    footerMenuV3: require('./footerMenuV3'),
    bottomMenu: require('./bottomMenu'),
    promotions: require('./promotions'),
    initSignposting: require('./initSignposting'),
    features: require('./features'),
    promotionsV2: require('./promotionsV2'),
    rightMenu: require('./rightMenu'),
    sportCategory: require('./sportCategory'),
    sportCategoryNative: require('./sportCategory'),
    sports: require('./sports'),
    staticBlock: require('./staticBlock'),
    systemConfiguration: require('./systemConfiguration'),
    topGames: require('./topGames'),
    topMenu: require('./topMenu'),
    userMenu: require('./userMenu'),
    modularContent: require('./modularContent'),
    offersV2: require('./offersV2'),
    seoPages: require('./seoPages'),
    seoPage: require('./seoPage'),
    seoSitemap: require('./seoSitemap'),
    quickLinks: require('./quickLinks'),
    desktopQuickLinks: require('./desktopQuickLinks'),
    widgets: require('./widgets'),
    ssoPage: require('./ssoPage'),
    maintenancePage: require('./maintenancePage'),
    footerLogos: require('./footerLogos'),
    footerLogosNative: require('./footerLogosNative')
  };
}

/**
 * Run selected API
 * @param {string} key – API name
 * @param {object} options – API options
 * @param {boolean} [noCache] - prevent uploading to akamai
 * @returns {*|promise}
 */
ApiManager.prototype.run = function(key, options, noCache) {
  let pr = this.apis[key](options);

  if (!noCache && !process.env.AKAMAI_DISABLED) {
    pr = pr.then(cacheManager.cacheJSONByKey(key, options));
  }

  return pr;
};

exports = module.exports = new ApiManager();
