import { lotteriesConfig } from '../configs/lotteriesLadbrokesConfig';
import { toteClasses } from '../configs/toteClasses';
import productionConfig from './environment.production';

import * as merge from 'lodash.merge';

const prodConfig = JSON.parse(JSON.stringify(productionConfig));

/* tslint:disable */
export default merge(prodConfig, {
  ENVIRONMENT: 'dev0',
  HORSE_RACING_CATEGORY_ID: '21',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '161'],
  UPCELL_ENDPOINT: 'https://betreceipts.internal.tst.ladbrokes.com',
  BPP_ENDPOINT: 'https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy',
  SITESERVER_BASE_URL: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-tst2.ladbrokes.com',
  SITESERVER_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-tst2.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT:
    'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Commentary/2.31',
  SURFACE_BETS_URL: 'https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api',
  CMS_ENDPOINT: 'https://cms-dev0.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-dev0.ladbrokes.com/cms',
  CMS_LINK: 'https://cms-dev0.ladbrokes.com/cms',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.dev.coral.co.uk/promosandbox/api/user-rank',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/ladbrokesV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-tst2-coral.symphony-solutions.eu',
  QUANTUMLEAP_BOOKMAKER: 'Ladbrokes-Test2',
  VISUALIZATION_IFRAME_URL: 'https://vis-static-tst2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-tst2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coraldev',
  DIGITAL_SPORTS_SYSTEM_ID: 982,
  DOMAIN: '.ladbrokes.com',
  STATS_CENTRE_ENDPOINT: 'https://statscenter-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api',
  OPT_IN_ENDPOINT: 'https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-dev0.coral.co.uk/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame',
  IMAGES_RACE_ENDPOINT: 'https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://df-api-gw-lr-test.ladbrokescoral.com/v4/customer-api/customers',
    API_KEY: 'LR4248266D8DE44AD3A163532230B78CC3'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown.internal.dev.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown.internal.dev.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown.internal.dev.ladbrokes.com/showdown/api/mybets'
  },
  SHOWDOWN_MS: 'https://showdown.internal.dev.ladbrokes.com/showdown/api',
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/ladbrokesTest2/0/',
  LIVESERV: {
    PUSH_URL: 'https://tst2-push-lcm.ladbrokes.com',
    PUSH_INSTANCE_URL: 'tst2-push-lcm.ladbrokes.com',
    PUSH_VERSION: '1dd785e1de9a32e236b624ae268bb803',
    DOMAIN: 'ladbrokes.com',
    PUSH_COMMON_SUBDOMAIN: 'ladbrokes.com',
    PUSH_LOCATION_HANDLER: '',
  },
  BR_TYPE_ID: ['3048', '3049', '3123'],
  LOTTERIES_CONFIG: lotteriesConfig.tst,
  TOTE_CLASSES: toteClasses.tst,
  FEATURED_SPORTS: 'wss://featured-sports-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  INPLAYMS: 'wss://inplay-publisher-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  CASHOUT_MS: 'https://cashout-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  LIVESERVEMS: 'wss://liveserve-publisher-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  EDPMS: 'https://edp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  BIG_COMPETITION_MS: 'https://bigcompetition-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/competition',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.ladbrokes.com',
    at_property: 'abaf3459-6df6-2b23-a718-f37546afeac0',
    betslip_at_property: '1b7662de-2a43-49f7-ec35-3afa39ad6b4a'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  TIME_ENDPOINT: 'https://hydra-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  TIMEFORM_ENDPOINT: 'https://timeform-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  RACING_POST_API_ENDPOINT: 'https://sb-api-dev.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'LDaa2737afbeb24c3db274d412d00b6d3b',
  VS_QUOLITY_MAP: {
    desktop: 'adpt',
    tablet: 'adpt',
    mobile: 'adpt'
  },
  GAMING_URL: ['https://slots.ladbrokes.com/en/games-tab'],
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-dev0.ladbrokes.com',
    ENV: 'dev'
  },
  COUPON_STATS_EXTERNAL_URL:'https://df-api-gw-com-test.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  googleTagManagerID: 'GTM-MZ45BFM',
  EXTERNAL_URL: {
    accountone: 'https://accountone-test.ladbrokes.com',
    gaming: 'https://gaming.ladbrokes.com',
    help: 'https://help.ladbrokes.com',
    'accountone-stg': 'https://accountone-stg.ladbrokes.com',
    'accountone-test': 'https://accountone-test.ladbrokes.com'
  },
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  DESKTOP_VIP_USERS_EXTERNAL_URL: 'https://casino.ladbrokes.com/en/vip/new-benefits',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api'
  },
  TOTE_CATEGORY_ID: '161',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player-test.igamemedia.com/lib/v1.0/streamservice.js',
  TIMELINE_MS: 'wss://timeline-api-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld-test.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '64eca02c6a21dd1213f03acb'
});
/* tslint:enable */

