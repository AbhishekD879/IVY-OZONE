import { toteClasses } from '../configs/toteClasses';
import { lotteriesConfig } from '../configs/lotteriesConfig';
import { sportsConfig } from '../configs/sportsConfig';
declare var require: any;
const packageData = require('../../../../package.json');

/* tslint:disable */
export default {
  brand: 'bma',
  settingsApiIms: {}, // 6.3 Android wrapper is crashing when this prop is missing. Removed in 6.4 ver.
  version: packageData.version,
  production: true,
  ENVIRONMENT: 'prod',
  CURRENT_PLATFORM: 'mobile',
  DOMAIN: '.coral.co.uk',
  googleTagManagerID: 'GTM-KW37JJ9',
  BETRADAR_WIDGETLOADERURL: 'https://widgets.sir.sportradar.com/5470d3e774c61ce0fc7757a4e10d7fc2/widgetloader',
  IMG_ARENA_SCOREBOARD: 'https://unpkg.com/@img-arena/front-row-seat',
  IMG_ARENA_OPERATOR_ID: '26',
  IMG_ARENA_OPERATOR_SECRET_KEY: 'UYhUc4Wep2',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '151'],
  BPP_ENDPOINT: 'https://bp.coral.co.uk/Proxy',
  SITESERVER_BASE_URL: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer',
  SITESERVER_VERSION: '2.31',
  SITESERVER_DNS: 'https://ss-aka-ori.coral.co.uk',
  SITESERVER_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.prod.coral.co.uk/silks/racingpost',
  IMAGES_ENDPOINT: 'https://img.coral.co.uk/img',
  INT_TOTE_IMAGES_ENDPOINT: 'https://tote-silks.coral.co.uk',
  SURFACE_BETS_URL: 'https://surface-bets.coral.co.uk/cms/api',
  CMS_ENDPOINT: 'https://cms.coral.co.uk/cms/api',
  CMS_ROOT_URI: 'https://cms.coral.co.uk/cms',
  CMS_LINK: 'https://cms.coral.co.uk/cms/',
  PERFORM_GROUP_END_POINT: 'https://secure.mobile.coral.performgroup.com/streaming',
  PERFORM_GROUP_END_POINT_DESKTOP: 'https://secure.coral.performgroup.com/streaming',
  IMG_END_POINT: 'https://api.livestreaming.imgarena.com/api/v2/streaming',
  ATR_END_POINT: 'https://bw106.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/coralV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis.symphony-solutions.eu',
  QUANTUMLEAP_BOOKMAKER: 'Coral',
  VISUALIZATION_IFRAME_URL: 'https://vis-static.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coral',
  DIGITAL_SPORTS_SYSTEM_ID: 993,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.prod.coral.co.uk/api',
  OPT_IN_ENDPOINT: 'https://optin.prod.coral.co.uk',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-hlv0.coral.co.uk/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.prod.coral.co.uk/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.prod.coral.co.uk/api/video/igame',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player.igamemedia.com/lib/v1.0/streamservice.js',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-mobile-pro.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'index.php',
    CARD_ENDPOINT: 'https://one-api-retail.coral.co.uk/v4/customer-api/customers',
    API_KEY: 'CRfeeacf03c008454b82f0176b5b63beb3'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/coral/0/',
  BET_FILTER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/oxygen/',
  BET_TRACKER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/bettracker/',
  SHOP_LOCATOR_ENDPOINT:
    'https://www.blipstar.com/blipstarplus/viewer/map?uid=4566046&value=10&gui=true&type=nearest&width=auto&tag=&autolocate=true&nocss=true&search=NW1',
    NOTIFICATION_CENTER_ENDPOINT:
    'https://notification-center.prod.coral.co.uk',
  LIVESERV: {
    DOMAIN: 'coral.co.uk',
    PUSH_COMMON_SUBDOMAIN: 'coral.co.uk',
    PUSH_LOCATION_HANDLER: '',
    PUSH_URL: 'https://mob-push.coral.co.uk',
    PUSH_INSTANCE_URL: 'mob-push.coral.co.uk',
    PUSH_INSTANCE_PORT: '443',
    PUSH_INSTANCE_TYPE: 'AJAX',
    PUSH_IFRAME_ID: 'push_iframe',
    PUSH_VERSION: 'e8382d8b7866e9a11d3529d8fe438008'
  },
  BR_TYPE_ID: ['28977', '28975', '29346'],
  CATEGORIES_DATA: sportsConfig,
  LOTTERIES_CONFIG: lotteriesConfig.prod,
  TOTE_CLASSES: toteClasses.prod,
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards.coral.co.uk',
    ENV: 'prod'
  },
  COUPON_STATS_EXTERNAL_URL:'https://df-api-gw-com.ladbrokescoral.com/sdm-fe-scoreboards/coral/js/sdm-scoreboard-min.js',
  FIVEASIDE: {
    contestPath: 'https://showdown.prod.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown.prod.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown.prod.ladbrokes.com/showdown/api/mybets'
  },
  mobileWidth: 767,
  landTabletWidth: 1024,
  desktopWidth: 1025,
  FEATURED_SPORTS: 'wss://featured-publisher.prod.coral.co.uk',
  INPLAYMS: 'wss://inplay-publisher.prod.coral.co.uk',
  LIVESERVEMS: 'wss://liveserve-publisher.prod.coral.co.uk',
  REMOTEBETSLIPMS: 'wss://remotebetslip.prod.coral.co.uk',
  EDPMS: 'https://edp.prod.coral.co.uk/',
  BIG_COMPETITION_MS: 'https://bigcompetition.prod.coral.co.uk/competition',
  UPMS: 'https://upms.prod.coral.co.uk/oddsPreference',
  BET_GENIUS_SCOREBOARD: {
    scorecentre:
      'https://ladbrokescoral.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre',
    api: 'https://ladbrokescoral.betstream.betgenius.com/betstream-view/public/bg_api.js'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  AEM_CONFIG: {
    server: 'https://banners-cms.coral.co.uk',
    at_property: 'b637a0ef-3583-855d-e895-29b3eb3894e3',
    betslip_at_property: 'b7d701f3-01c8-23b7-2b1f-48b4423f6c8b'
  },
  HELP_SUPPORT_URL: 'https://myaccount.coral.co.uk/en/mobileportal/contact',
  HELP_LOTTO_RULES: 'https://help.coral.co.uk/en/general-information/legal-matters/lottorules',
  TIME_ENDPOINT: 'https://hydra.prod.coral.co.uk',
  TIMEFORM_ENDPOINT: 'https://timeform.prod.coral.co.uk',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.prod.coral.co.uk/promosandbox/api/user-rank',
  RACING_POST_API_ENDPOINT: 'https://sb-api.coral.co.uk/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api.coral.co.uk/v4/sportsbook-api',
  RACING_POST_API_KEY: 'CDb93052f939a44c96b78dcaa7528d2447',
  GAMING_URL: ['https://gaming.coral.co.uk'],
  VS_QUOLITY_MAP: {
    desktop: 'web',
    tablet: 'mobhi',
    mobile: 'moblo'
  },
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 34799,
    uri: 'https://buildyourbet.prod.coral.co.uk/api'
  },
  HORSE_RACING_CATEGORY_ID: '21',
  UPCELL_ENDPOINT: 'https://betreceipts.prod.coral.co.uk',
  TOTE_CATEGORY_ID: '151',
  RULE_FOUR_URL: 'https://help.coral.co.uk/s/article/Rule-4-deductions',
  EXTERNAL_URL: {},
  CASHOUT_MS: 'https://cashout.prod.coral.co.uk',
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  DESKTOP_VIP_USERS_EXTERNAL_URL: 'https://casino.ladbrokes.com/en/vip/new-benefits',
  MINI_GAMES_IFRAME_URL: 'https://cachedownload.coral.co.uk/casinoclient.html',
  STORAGE_SERVICE_PREFIX: 'OX',
  RPG_API_CONFIG: {
    GAMES_URL: 'https://gaming.coral.co.uk/',
    FETCH_URL: 'https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.3/fetch.min.js',
    XBC_LOADER: {
      data_bundle: 'https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/feature/GEM-5061-MWSS-Recently-Migration',
      src: 'https://apk.coral.co.uk/XBC/xbc/feature/GEM-5061-MWSS-Recently-tag/loader.js'
    }
  },
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.prod.coral.co.uk/api',
  IDENTITY_ID: 'eu-west-2:69c5eb81-6abc-4ce9-88cf-44346c17734d',
  TIMELINE_MS: 'wss://timeline-api.prod.coral.co.uk',
  HOME_PAGE: 'https://sports.coral.co.uk',
  OXYMS: '',
  CMS_ASSETS: '/cms/',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcJiz8aAAAAACmWVFTuZDP4BvXoLMrt0jmua-Wu'
  },
  ISEVENTCOALESCING: true,
  FLAG_CLIENT_KEY: '64eca041795d241275a129f5'
};
/* tslint:enable */
