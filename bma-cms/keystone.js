// Start newRelic
// Configuration of the newRelic located in newrelic.js file
require('newrelic');

// Simulate config options from your production environment by
// customising the .env file in your project's root folder.
require('dotenv').load();

// Require keystone
var keystone = require('./bma-betstone');

const pushService = require('./lib/pushService');

// Initialise Keystone with your project's configuration.
// See http://keystonejs.com/guide/config for available options
// and documentation.

keystone.init({

  'name': 'bma',
  'brand': 'bma',


  'less': 'public',
  'static': 'public',
  'favicon': 'public/favicon.ico',
  'views': 'templates/views',
  'view engine': 'jade',
  'auto update': true,
  'mongo': process.env.MONGODB,
  'session': true,
  'auth': true,
  'user model': 'User',
  'trust proxy': true,
  'wysiwyg images': true,
  'cookie secret': 'z)BF~TBeOzX;@_JzwTum2cIF3cq0naK;&5o[bvJ,Eu(y_~KiUL9Hy%9PMpTl$n2S'
});

// Load your project's Models

keystone.import('models');

// Setup common locals for your templates. The following are required for the
// bundled templates and layouts. Any runtime locals (that should be set uniquely
// for each request) should be added to ./routes/middleware.js

keystone.set('locals', {
  _: require('underscore'),
  env: keystone.get('env'),
  utils: keystone.utils,
  editable: keystone.content.editable
});

// Load your project's Routes

keystone.set('routes', require('./routes'));

// Setup common locals for your emails. The following are required by Keystone's
// default email templates, you may remove them if you're using your own.

// Configure the navigation bar in Keystone's Admin UI

keystone.set('nav', {
  'admin': ['users', 'brand', 'staticBlock'],
  'maintenance': 'maintenancePage',
  'banners': ['banners', 'football3DBanner', 'betReceiptBanner', 'betReceiptBannerTablet'],
  'promotions': 'promotions',
  'features': 'features',
  'dashboard': 'dashboard',
  'menus': ['headerMenu', 'connectMenu', 'rightMenu', 'userMenu', 'sportCategory', 'footerMenu', 'topGames', 'bottomMenu', 'Desktop QuickLink', 'quickLink', 'footerLogos'],
  'widgets': 'widgets',
  'ModuleRibbonTabs': ['ModuleRibbonTabs'],
  'Offers': ['offerModule', 'offer'],
  'SEO': 'seoPage',
  'olympicSports': 'sports',
  'Leagues': 'leagues',
  'YourCall': ['ycLeague', 'ycMarket', 'ycStaticBlock'],
  'EDPMarkets': 'edpMarket',
  'SSO': 'ssoPage'
});

// init pushService
if (process.env.PUBNUB_PUBLISH_KEY && process.env.PUBNUB_SUBSCRIBE_KEY) {
  pushService.init(process.env.PUBNUB_PUBLISH_KEY, process.env.PUBNUB_SUBSCRIBE_KEY);
}

// Start Keystone to connect to your database and initialise the web server
keystone.start();
