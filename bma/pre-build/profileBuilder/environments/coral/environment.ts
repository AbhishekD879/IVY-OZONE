import * as merge from 'lodash.merge';

import { toteClasses } from '../configs/toteClasses';
import { lotteriesConfig } from '../configs/lotteriesConfig';
import productionConfig from './environment.production';
const packageData = require('../../../package.json');
const prodConfig = JSON.parse(JSON.stringify(productionConfig));

/* tslint:disable */
export default merge(prodConfig, {
  production: false,
  ENVIRONMENT: 'dev',
  version: packageData.version,
  HORSE_RACING_CATEGORY_ID: '21',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '161'],
  BPP_ENDPOINT: 'https://bpp-dev0.coralsports.dev.cloud.ladbrokescoral.com/Proxy',
  SITESERVER_BASE_URL: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer',
  SITESERVER_DNS: 'https://backoffice-tst2.coral.co.uk',
  SITESERVER_ENDPOINT: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.31',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  IMAGES_RACE_ENDPOINT: 'https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost',
  CMS_ENDPOINT: 'https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api',
  CMS_ROOT_URI: 'https://coral-cms-api-dev.s3.eu-west-1.amazonaws.com',
  CMS_LINK: 'https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  UPCELL_ENDPOINT: 'https://betreceipts.beta.coral.co.uk',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www.racemodlr.com/coral-invictus/live_sim/mobile',
  VISUALIZATION_ENDPOINT: 'https://vis-tst2-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis-tst2.symphony-solutions.eu',
  PROMO_LB_ENDPOINT: 'https://promo-sandbox.internal.dev.coral.co.uk/promosandbox/api/user-rank',
  QUANTUMLEAP_BOOKMAKER: 'Coral-Test-2',
  VISUALIZATION_IFRAME_URL: 'https://vis-static-tst2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-tst2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coraldev',
  DIGITAL_SPORTS_SYSTEM_ID: 982,
  STATS_CENTRE_ENDPOINT: 'https://spark-br-tst.symphony-solutions.eu/api',
  OPT_IN_ENDPOINT: 'https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-dev0.coral.co.uk/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame',
  TRENDING_BETS_API_ENDPOINT: 'https://trending-bets.internal.tst.coral.co.uk/api',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://df-api-gw-cr-test.ladbrokescoral.com/v4/customer-api/customers',
    API_KEY: 'CR78F5FF85A16547109CBAAFCC3CF0D2D4'
  },
  BET_FINDER_ENDPOINT: 'https://api.racemodlr.com/cypher/coralTest2/0/',
  BET_FILTER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/oxygen/',
  BET_TRACKER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/bettracker/',
  COUPON_BUDDY_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/oxygen/coupon-buddy-oxygen.js',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.internal.tst.coral.co.uk',
  LIVESERV: {
    PUSH_URL: 'https://push-tst2.coral.co.uk',
    PUSH_INSTANCE_URL: 'push-tst2.coral.co.uk',
    PUSH_VERSION: 'c3e5103c451ba491d75a024811deba7f'
  },
  BR_TYPE_ID: ['3048', '3049', '3123'],
  LOTTERIES_CONFIG: lotteriesConfig.tst,
  TOTE_CLASSES: toteClasses.tst,
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-dev0.coral.co.uk',
    ENV: 'dev'
  },
  FEATURED_SPORTS: 'wss://featured-sports-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  INPLAYMS: 'wss://inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  LIVESERVEMS: 'wss://liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  EDPMS: 'https://edp-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  BIG_COMPETITION_MS: 'https://bigcompetition-dev0.coralsports.dev.cloud.ladbrokescoral.com/competition',
  BET_GENIUS_SCOREBOARD: {
    scorecentre: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre',
    api: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/public/bg_api.js'
  },
  AEM_CONFIG: {
    server: 'https://banners-cms.coral.co.uk'
  },
  TIMEFORM_ENDPOINT: 'https://timeform-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  RACING_POST_API_ENDPOINT: 'https://sb-api-dev.coral.co.uk/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api.coral.co.uk/v4/sportsbook-api',
  RACING_POST_API_KEY: 'CD11beae13fa47459ba472e0b743822846',
  GAMING_URL: ['https://mcasino-tst2.coral.co.uk'],
  VS_QUOLITY_MAP: {
    desktop: 'web',
    tablet: 'mobhi',
    mobile: 'moblo'
  },
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player-test.igamemedia.com/lib/v1.0/streamservice.js',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api'
  },
  TOTE_CATEGORY_ID: '161',
  EXTERNAL_URL: {
    accountone: 'https://accountone-test.ladbrokes.com',
  },
  CASHOUT_MS: 'https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine-dev0.coralsports.dev.cloud.ladbrokescoral.com/api',
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  RPG_API_CONFIG: {
    GAMES_URL: 'https://gaming.coral.co.uk/',
    FETCH_URL: 'https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.3/fetch.min.js',
    XBC_LOADER: {
      data_bundle: 'https://lci-coral-sports-react-bundler.surge.sh',
      src: 'https://apk.coral.co.uk/XBC/xbc/1.0.4/loader.js'
    }
  },
  FLAG_CLIENT_KEY: '64eca041795d241275a129f4'
});
/* tslint:enable */
