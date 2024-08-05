import { toteClasses } from '../configs/toteClasses';
import { lotteriesConfig } from '../configs/lotteriesLadbrokesConfig';
import { sportsConfig } from '../configs/sportsConfig';
declare var require: any;
const packageData = require('../../../../package.json');

/* tslint:disable */
export default {
  brand: 'ladbrokes',
  settingsApiIms: {}, // 6.3 Android wrapper is crashing when this prop is missing. Removed in 6.4 ver.
  version: packageData.version,
  production: true,
  ENVIRONMENT: 'prod',
  CURRENT_PLATFORM: 'mobile',
  DOMAIN: '.ladbrokes.com',
  BETRADAR_WIDGETLOADERURL: 'https://widgets.sir.sportradar.com/2ed374901e6972e6e1cca123cbe41fb8/widgetloader',
  IMG_ARENA_SCOREBOARD: 'https://unpkg.com/@img-arena/front-row-seat',
  IMG_ARENA_OPERATOR_ID: '42',
  IMG_ARENA_OPERATOR_SECRET_KEY: 'HnLdyNYfX6',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '151'],
  BPP_ENDPOINT: 'https://bpp.ladbrokes.com/Proxy',
  SITESERVER_VERSION: '2.31',
  SITESERVER_DNS: 'https://ss-aka-ori.ladbrokes.com',
  SITESERVER_BASE_URL: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer',
  SITESERVER_ENDPOINT: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Commentary/2.31',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.prod.ladbrokes.com/silks/racingpost',
  SURFACE_BETS_URL: 'https://surface-bets.ladbrokes.com/cms/api',
  IMAGES_ENDPOINT: 'https://img.coral.co.uk/img',
  INT_TOTE_IMAGES_ENDPOINT: 'https://tote-silks.ladbrokes.com',
  CMS_ENDPOINT: 'https://cms-prod.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-prod.ladbrokes.com/cms',
  CMS_LINK: 'https://cms-api-ui-prd0.coralsports.prod.cloud.ladbrokescoral.com/',
  PERFORM_GROUP_END_POINT: 'https://secure.mobile.ladbrokes.performgroup.com/streaming',
  PERFORM_GROUP_END_POINT_DESKTOP: 'https://secure.ladbrokes.performgroup.com/streaming',
  IMG_END_POINT: 'https://api.livestreaming.imgarena.com/api/v2/streaming',
  ATR_END_POINT: 'https://bw102.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/ladbrokesV3/live_sim/mobile/?ver=7Sep2023',
  QUANTUMLEAP_BOOKMAKER: 'Ladbrokes',
  VISUALIZATION_ENDPOINT: 'https://vis-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis.symphony-solutions.eu',
  VISUALIZATION_IFRAME_URL: 'https://vis-static.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coral',
  DIGITAL_SPORTS_SYSTEM_ID: 993,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.prod.ladbrokes.com/api',
  OPT_IN_ENDPOINT: 'https://optin.prod.ladbrokes.com',
  FREE_RIDE_PLACEBET_ENDPOINT: 'https://freeride.prod.ladbrokes.com/v1/api/freeride/placeBet',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.prod.ladbrokes.com/promosandbox/api/user-rank',
  ONE_TWO_FREE_ENDPOINT: 'https://otf.ladbrokes.com/',
  ONE_TWO_FREE_API_ENDPOINT:'https://otf-api.prod.ladbrokes.com/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.prod.ladbrokes.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.prod.ladbrokes.com/api/video/igame',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player.igamemedia.com/lib/v1.0/streamservice.js',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-mobile-pro.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'index.php',
    CARD_ENDPOINT: 'https://one-api-retail.ladbrokes.com/v4/customer-api/customers',
    API_KEY: 'LRa7d8867104b549e48f4ff6c1ef50d759'
  },
  DIGITAL_COUPONS_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/digital/grid/static/',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcJiz8aAAAAACmWVFTuZDP4BvXoLMrt0jmua-Wu'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/ladbrokes/0/',
  BET_FILTER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/oxygen-grid/',
  BET_TRACKER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/bettracker-grid/',
  SHOP_LOCATOR_ENDPOINT: 'https://www.blipstar.com/blipstarplus/viewer/map?uid=2470030&value=10&gui=true&type=nearest&width=auto&tag=&autolocate=true&nocss=true&search=NW1',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.prod.ladbrokes.com',
  LIVESERV: {
    DOMAIN: 'ladbrokes.com',
    PUSH_COMMON_SUBDOMAIN: 'ladbrokes.com',
    PUSH_LOCATION_HANDLER: '',
    PUSH_URL: 'https://push-lcm.ladbrokes.com',
    PUSH_INSTANCE_URL: 'push-lcm.ladbrokes.com',
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
    CDN: 'https://opta-scoreboards.ladbrokes.com',
    ENV: 'prod'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-com.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  mobileWidth: 767,
  landTabletWidth: 1024,
  desktopWidth: 1025,
  FEATURED_SPORTS: 'wss://featured-publisher.prod.ladbrokes.com',
  INPLAYMS: 'wss://inplay-publisher.prod.ladbrokes.com',
  CASHOUT_MS: 'https://cashout.prod.ladbrokes.com',
  LIVESERVEMS: 'wss://liveserve-publisher.prod.ladbrokes.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip.prod.ladbrokes.com',
  EDPMS: 'https://edp.prod.ladbrokes.com',
  BIG_COMPETITION_MS: 'https://bigcompetition.prod.ladbrokes.com/competition',
  UPMS: 'https://upms.prod.ladbrokes.com/oddsPreference',
  BET_GENIUS_SCOREBOARD: {
    scorecentre: 'https://ladbrokescoral.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre',
    api: 'https://ladbrokescoral.betstream.betgenius.com/betstream-view/public/bg_api.js'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  AEM_CONFIG: {
    server: 'https://banners-cms.ladbrokes.com',
    at_property: 'd01b458f-4505-86d5-3d58-64113bb70196',
    betslip_at_property: '4b720044-1be9-de72-e197-8c8b530537a6'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown2.prod.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown2.prod.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown2.prod.ladbrokes.com/showdown/api/mybets'
  },
  COMMUNICATION_URL: 'https://myaccount.ladbrokes.com/en/mobileportal/communication',
  HELP_SUPPORT_URL: 'https://myaccount.ladbrokes.com/en/mobileportal/contact',
  HELP_LOTTO_RULES: 'https://help.ladbrokes.com/en/general-information/legal-matters/lottorules',
  RULE_FOUR_URL: 'https://help.ladbrokes.com/s/article/LB-Rule-4-Deductions',
  TIME_ENDPOINT: 'https://hydra.prod.ladbrokes.com',
  TIMEFORM_ENDPOINT: 'https://timeform.prod.coral.co.uk',
  RACING_POST_API_ENDPOINT: 'https://sb-api.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'LDc7c2ede219f84f95b81f3e87e2800a3c',
  GAMING_URL: ['https://gaming.ladbrokes.com'],
  VS_QUOLITY_MAP: {
    desktop: 'adpt',
    tablet: 'adpt',
    mobile: 'adpt'
  },
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 34799,
    uri: 'https://buildyourbet.prod.ladbrokes.com/api'
  },
  HORSE_RACING_CATEGORY_ID: '21',
  UPCELL_ENDPOINT: 'https://betreceipts.prod.ladbrokes.com',
  TOTE_CATEGORY_ID: '151',
  EXTERNAL_URL: {
    accountone: 'https://accountone.ladbrokes.com',
    gaming: 'https://gaming.ladbrokes.com',
    help: 'https://help.ladbrokes.com',
  },
  MINI_GAMES_IFRAME_URL: 'https://cachedownload.ladbrokes.com/casinoclient.html',
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  DESKTOP_VIP_USERS_EXTERNAL_URL: 'https://casino.ladbrokes.com/en/vip/new-benefits',
  STORAGE_SERVICE_PREFIX: 'OX',
  RPG_API_CONFIG: {
    GAMES_URL: 'https://gaming.ladbrokes.com/',
    FETCH_URL: 'https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.3/fetch.min.js',
    XBC_LOADER: {
      data_bundle: 'https://apk.coral.co.uk/XBC/bundler-ladbrokes-bundler/feature/GEM-5061-MWSS-Recently-Migration-Oxygen',
      src: 'https://apk.coral.co.uk/XBC/xbc/feature/GEM-5061-MWSS-Recently-tag/loader.js'
    }
  },
  LIVE_COMMENTARY_URL: 'https://commentaries.mediaondemand.net/?c=ladbrokes&cl=ladbrokes&menu=true',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.prod.ladbrokes.com/api',
  TIMELINE_MS: 'wss://timeline-api.prod.ladbrokes.com',
  SHOWDOWN_MS: 'https://showdown2.prod.ladbrokes.com/showdown/api',
  IDENTITY_ID: 'eu-west-2:69c5eb81-6abc-4ce9-88cf-44346c17734d',
  HOME_PAGE: 'https://sports.ladbrokes.com',
  OXYMS: '',
  ISEVENTCOALESCING: true,
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '64eca02c6a21dd1213f03acc'
};
/* tslint:enable */

