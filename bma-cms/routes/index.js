/**
 * This file is where you define your application routes and controllers.
 *
 * Start by including the middleware you want to run for every request;
 * you can attach middleware to the pre('routes') and pre('render') events.
 *
 * For simplicity, the default setup for route controllers is for each to be
 * in its own file, and we import all the files in the /routes/api directory.
 *
 * Each of these files is a route controller, and is responsible for all the
 * processing that needs to happen for the route (e.g. loading data, handling
 * form submissions, rendering the view template, etc).
 *
 * Bind each route pattern your application should respond to in the function
 * that is exported from this module, following the examples below.
 *
 * See the Express application routing documentation for more information:
 * http://expressjs.com/api.html#app.VERB
 */

const keystone = require('../bma-betstone'),
  middleware = require('./middleware'),
  importRoutes = keystone.importer(__dirname),

  // Import Route Controllers
  routes = {
    api: importRoutes('./api'),
    apiV2: importRoutes('./apiV2'),
    apiV3: importRoutes('./apiV3'),
    ss: importRoutes('./ss'),
    views: importRoutes('./views')
  };

// Common Middleware
keystone.pre('routes', middleware.initLocals);
keystone.pre('render', middleware.flashMessages);

// Setup Route Bindings
exports = module.exports = function(app) {
  // Enabled CORS
  app.all('/api*', keystone.middleware.cors);

  app.get('/api/doc', routes.views.apiDoc);

  app.all('/api/purgeStatus/:progressUri', routes.api.purgeStatus);

  app.all('/api/set-config', routes.api.setConfig);
  app.all('/api/set-structure', routes.api.setStructure);

  app.all('/api/openbet-ssviewer/*', routes.api.openbetSSViewer);

  app.get('/api/status', routes.api.status);

  // Routs to support multi branding

  app.all('/api/v2/:brand/banners', routes.apiV2.banners);
  app.all('/api/v2/:brand/banners/:categoryUri', routes.apiV2.banners);

  app.all('/api/:brand/3d-football-banners/', routes.api.football3DBanners);

  app.all('/api/:brand/bet-receipt-banners/mobile', routes.api.betReceiptBanners);

  app.all('/api/:brand/bet-receipt-banners/tablet', routes.api.betReceiptBannersTablet);

  app.all('/api/:brand/leagues', routes.api.leagues);

  app.all('/api/:brand/yc-leagues', routes.api.ycLeagues);

  app.all('/api/:brand/yc-markets', routes.api.ycMarkets);

  app.all('/api/:brand/yc-static-block', routes.api.ycStaticBlock);

  app.all('/api/:brand/edp-markets', routes.api.edpMarkets);

  app.all('/api/:brand/seo-pages', routes.api.seoPages);
  app.all('/api/:brand/seo-page/:id', routes.api.seoPage);
  app.all('/api/:brand/seo-sitemap', routes.api.seoSitemap);

  app.all('/api/:brand/widgets', routes.api.widgets);

  app.all('/api/:brand/promotions', routes.api.promotions);
  app.all('/api/:brand/init-signposting', routes.api.initSignposting);

  app.all('/api/:brand/features', routes.api.features);

  app.all('/api/:brand/static-block/:uri', routes.api.staticBlock);

  app.all('/api/:brand/header-menu', routes.api.headerMenu);

  app.all('/api/:brand/connect-menu', routes.api.connectMenu);

  app.all('/api/v2/:brand/footer-menu/:deviceType', routes.apiV2.footerMenu);

  app.all('/api/:brand/bottom-menu', routes.api.bottomMenu);

  app.all('/api/:brand/right-menu', routes.api.rightMenu);

  app.all('/api/:brand/user-menu', routes.api.userMenu);

  app.all('/api/:brand/top-menu', routes.api.topMenu);

  app.all('/api/:brand/sport-category', routes.api.sportCategory);
  app.all('/api/:brand/sport-category-native', routes.api.sportCategoryNative);

  app.all('/api/:brand/sports', routes.api.sports);

  app.all('/api/:brand/top-games', routes.api.topGames);
  app.all('/api/:brand/system-configuration', routes.api.systemConfiguration);

  app.all('/api/:brand/set-config', routes.api.setConfig);
  app.all('/api/:brand/set-structure', routes.api.setStructure);

  app.all('/api/:brand/modular-content', routes.api.modularContent);
  app.all('/api/:brand/modular-content/:moduleId', routes.api.modularContent);

  app.post('/api/changeCountrySettings', routes.api.setCountries);
  app.all('/api/:brand/countries-settings', routes.api.countries);

  app.get('/api/ss/load-events/:selectionType/:selectionId/:from/:to', routes.ss.loadEvents);

  app.get('/api/v2/:brand/offers/:deviceType', routes.apiV2.offers);

  app.get('/api/:brand/quick-links/:raceType', routes.api.quickLinks);

  app.get('/api/:brand/desktop-quick-links', routes.api.desktopQuickLinks);

  app.get('/api/:brand/sso-page/:osType', routes.api.ssoPage);

  app.get('/api/:brand/initial-data/:deviceType', routes.api.initialData);

  app.get('/api/:brand/maintenance-page/:deviceType', routes.api.maintenancePage);

  app.get('/api/:brand/footer-logos-native', routes.api.footerLogosNative);

  // Routes used only on Retail
  app.all('/api/v2/:brand/promotions/:categories?', routes.apiV2.promotions);
  app.all('/api/v3/:brand/footer-menu', routes.apiV3.footerMenu);

  // NOTE: To protect a route so that only admins can see it, use the requireUser middleware:
  // app.get('/protected', middleware.requireUser, routes.api.protected);
};
