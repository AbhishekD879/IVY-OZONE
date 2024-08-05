import { toteClasses } from '../../pre-build/profileBuilder/environments/configs/toteClasses';
import { lotteriesConfig } from '../../pre-build/profileBuilder/environments/configs/lotteriesConfig';
import { sportsConfig } from '../../pre-build/profileBuilder/environments/configs/sportsConfig';
declare let require: any;
const packageData = require('../../package.json');

/* eslint-disable */
export default {
  brand: 'bma',
  settingsApiIms: {}, // 6.3 Android wrapper is crashing when this prop is missing. Removed in 6.4 ver.
  version: packageData.version,
  production: true,
  ENVIRONMENT: 'dev',
  CURRENT_PLATFORM: 'mobile',
  DOMAIN: '.coral.co.uk',
  googleTagManagerID: ['gtmId1', 'gtmId2'],
  QUBIT_SCRIPT: 'https://static.goqubit.com/smartserve-4945.js',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '151'],
  BPP_ENDPOINT: 'https://bp.coral.co.uk/Proxy',
  SITESERVER_BASE_URL: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer',
  SITESERVER_VERSION: '2.31',
  SITESERVER_DNS: 'https://ss-aka-ori.coral.co.uk',
  BETRADAR_WIDGETLOADERURL: 'https://widgets.sir.sportradar.com/7a46ac03acda6cd30e5817cf905ae88d/widgetloader',
  IMG_ARENA_SCOREBOARD: 'https://unpkg.com/@img-arena/front-row-seat',
  IMG_ARENA_OPERATOR_ID: '11',
  IMG_ARENA_OPERATOR_SECRET_KEY: 'abcfABDC',
  SITESERVER_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.coral.co.uk/silks/racingpost',
  IMAGES_ENDPOINT: 'https://img.coral.co.uk/img',
  INT_TOTE_IMAGES_ENDPOINT: 'https://tote-silks.coral.co.uk',
  SURFACE_BETS_URL: 'https://surface-bets.coral.co.uk/cms/api',
  CMS_ENDPOINT: 'https://cms.coral.co.uk/cms/api',
  UPCELL_ENDPOINT: 'https://betreceipts.beta.coral.co.uk',
  CMS_ROOT_URI: 'https://cms.coral.co.uk/cms/',
  CMS_LINK: 'https://cms.coral.co.uk/cms/',
  PERFORM_GROUP_END_POINT: 'https://secure.mobile.coral.performgroup.com/streaming',
  PERFORM_GROUP_END_POINT_DESKTOP: 'https://secure.coral.performgroup.com/streaming',
  IMG_END_POINT: 'https://api.livestreaming.imgarena.com/api/v2/streaming',
  ATR_END_POINT: 'https://bw106.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/coral/live_sim/mobile/?ver=23Aug2023',
  VISUALIZATION_ENDPOINT: 'https://vis-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis.symphony-solutions.eu',
  QUANTUMLEAP_BOOKMAKER: 'Coral',
  VISUALIZATION_IFRAME_URL: 'https://vis-static.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coral',
  DIGITAL_SPORTS_SYSTEM_ID: 993,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.coral.co.uk/api',
  OPT_IN_ENDPOINT: 'https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-hlv0.coral.co.uk/',
  ONE_TWO_FREE_API_ENDPOINT:'https://otf-api.beta.ladbrokes.com/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player.igamemedia.com/lib/v1.0/streamservice.js',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-mobile-pro.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'index.php',
    CARD_ENDPOINT: 'https://one-api-retail.coral.co.uk/v4/customer-api/customers',
    API_KEY: 'CRfeeacf03c008454b82f0176b5b63beb3'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown.beta.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown.beta.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown.beta.ladbrokes.com/showdown/api/mybets'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/coral/0/',
  BET_FILTER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/oxygen/',
  BET_TRACKER_ENDPOINT: 'https://modules.coral.co.uk/coupon-buddy/bettracker/',
  SHOP_LOCATOR_ENDPOINT:
    'https://www.blipstar.com/blipstarplus/viewer/map?uid=4566046&value=10&gui=true&type=nearest&width=auto&tag=&autolocate=true&search=NW1',
  NOTIFICATION_CENTER_ENDPOINT:
    'https://notification-center-prd0.coralsports.prod.cloud.ladbrokescoral.com',
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
  BR_TYPE_ID: ['3048', '3049', '3123'],
  CATEGORIES_DATA: sportsConfig,
  LOTTERIES_CONFIG: lotteriesConfig.prod,
  TOTE_CLASSES: toteClasses.prod,
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards.coral.co.uk',
    ENV: 'prod'
  },
  mobileWidth: 767,
  landTabletWidth: 1024,
  desktopWidth: 1025,
  FEATURED_SPORTS: 'wss://featured-sports-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  INPLAYMS: 'wss://inplay-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  LIVESERVEMS: 'wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  EDPMS: 'https://edp-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  BIG_COMPETITION_MS:
    'https://bigcompetition-prd0.coralsports.prod.cloud.ladbrokescoral.com/competition',
  UPMS: 'http://upms.internal.tst.coral.co.uk/oddsPreference',
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
  COMMUNICATION_URL: 'https://qa2.myaccount.ladbrokes.com/en/mobileportal/communication',
  HELP_SUPPORT_URL: 'https://help.coral.co.uk/s/article/Contact-Us',
  HELP_LOTTO_RULES: 'https://help.coral.co.uk/en/general-information/legal-matters/lottorules',
  TIME_ENDPOINT: 'https://hydra-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  TIMEFORM_ENDPOINT: 'https://timeform-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  FREE_RIDE_PLACEBET_ENDPOINT: 'https://freeride.internal.stg.ladbrokes.com/v1/api/freeride/placeBet',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.dev.coral.co.uk/promosandbox/api/user-rank',
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
    uri: 'https://buildyourbet.coral.co.uk/api'
  },
  HORSE_RACING_CATEGORY_ID: '21',
  TOTE_CATEGORY_ID: '161',
  HOME_PAGE: 'https://beta-sports.ladbrokes.com',
  RULE_FOUR_URL: 'https://help.coral.co.uk/s/article/Rule-4-deductions',
  EXTERNAL_URL: {},
  CASHOUT_MS: 'https://cashout-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  COUPON_STATS_EXTERNAL_URL:'https://df-api-gw-com-test.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
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
  LIVE_COMMENTARY_URL: 'https://commentaries.mediaondemand.net/?c=ladbrokes&cl=ladbrokes&menu=true',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine-dev0.coralsports.dev.cloud.ladbrokescoral.com/api',
  CMS_ASSETS: '/cms/',
  TIMELINE_MS: 'wss://timeline-api-prd0.coralsports.prod.cloud.ladbrokescoral.com',
  SHOWDOWN_MS: 'https://showdown.beta.ladbrokes.com/showdown/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '64eca02c6a21dd1213f03acb'
};
/* eslint-enable */
