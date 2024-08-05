import { lotteriesConfig } from '../configs/lotteriesConfig';
import { toteClasses } from '../configs/toteClasses';
import productionConfig from './environment.production';

import * as merge from 'lodash.merge';
const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  production: false,
  ENVIRONMENT: 'stg',
  HORSE_RACING_CATEGORY_ID: '21',
  EVENT_CATEGORIES_WITH_WATCH_RULES: ['21', '19', '152'],
  BPP_ENDPOINT: 'https://bpp-stg.coral.co.uk/Proxy',
  SITESERVER_BASE_URL: 'https://ss-stg.coral.co.uk/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-stg.coral.co.uk',
  SITESERVER_ENDPOINT: 'https://ss-stg.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-stg.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-stg.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT: 'https://ss-stg.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-stg.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  SURFACE_BETS_URL: 'https://surface-bets-stg0.coral.co.uk/cms/api',
  CMS_ENDPOINT: 'https://cms-stg.coral.co.uk/cms/api',
  CMS_ROOT_URI: 'https://cms-stg.coral.co.uk/cms',
  CMS_LINK: 'https://cms-api-ui-stg0.coralsports.nonprod.cloud.ladbrokescoral.com',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/coralV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-stg2-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis-stg2.symphony-solutions.eu',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.tst.coral.co.uk/promosandbox/api/user-rank',
  QUANTUMLEAP_BOOKMAKER: 'Coral-Stage',
  VISUALIZATION_IFRAME_URL: 'https://vis-static-stg2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-stg2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coralstg',
  DIGITAL_SPORTS_SYSTEM_ID: 983,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.internal.stg.coral.co.uk/api',
  OPT_IN_ENDPOINT: 'https://optin.internal.stg.coral.co.uk',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.internal.stg.coral.co.uk/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.internal.stg.coral.co.uk/api/video/igame',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-mobile-stg.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'index.php',
    CARD_ENDPOINT: 'https://one-api-retail-stg.coral.co.uk/v4/customer-api/customers',
    API_KEY: 'CRfc83f4d5d5e14eeab096e072fe6851b7'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/coralStage/0/',
  BET_FILTER_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/oxygen/',
  BET_TRACKER_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/bettracker/',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.internal.stg.coral.co.uk',
  LIVESERV: {
    PUSH_URL: 'https://push-stg.coral.co.uk',
    PUSH_INSTANCE_URL: 'push-stg.coral.co.uk',
    PUSH_VERSION: 'c3e5103c451ba491d75a024811deba7f'
  },
  BR_TYPE_ID: ['16576', '16575', '16602'],
  LOTTERIES_CONFIG: lotteriesConfig.tst,
  TOTE_CLASSES: toteClasses.stg,
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-dev0.coral.co.uk',
    ENV: 'stage'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-com-stage.ladbrokescoral.com/sdm-fe-scoreboards/coral/js/sdm-scoreboard-min.js',
  FEATURED_SPORTS: 'wss://featured-publisher.internal.stg.coral.co.uk',
  INPLAYMS: 'wss://inplay-publisher.internal.stg.coral.co.uk',
  LIVESERVEMS: 'wss://liveserve-publisher.internal.stg.coral.co.uk',
  REMOTEBETSLIPMS: 'wss://remotebetslip.internal.stg.coral.co.uk',
  EDPMS: 'https://edp.internal.stg.coral.co.uk',
  BIG_COMPETITION_MS: 'https://bigcompetition.internal.stg.coral.co.uk/competition',
  UPMS: 'https://upms.internal.stg.coral.co.uk/oddsPreference',
  BET_GENIUS_SCOREBOARD: {
    scorecentre: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre',
    api: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/public/bg_api.js'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.coral.co.uk',
    at_property: '63909eaa-a987-2833-6631-85b5ced26e68',
    betslip_at_property: '0c727079-a884-88b9-1fd8-faa96c1a6fa7'
  },
  IMAGES_RACE_ENDPOINT: 'https://aggregation.internal.stg.coral.co.uk/silks/racingpost',
  TIME_ENDPOINT: 'https://hydra.prod.coral.co.uk',
  TIMEFORM_ENDPOINT: 'https://timeform.internal.stg.coral.co.uk',
  GAMING_URL: ['https://wpl-stg-admin-coral.coral.co.uk', 'https://wpl-stg-public-coral.coral.co.uk'],
  VS_QUOLITY_MAP: {
    desktop: 'web',
    tablet: 'mobhi',
    mobile: 'moblo'
  },
  RACING_POST_API_ENDPOINT: 'https://sb-api-stg.coral.co.uk/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.coral.co.uk/v4/sportsbook-api',
  RACING_POST_API_KEY:'CD3DDB282FF116480AB3BB3113AAF316FE',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 28337,
    uri: 'https://buildyourbet.internal.stg.coral.co.uk/api'
  },
  TOTE_CATEGORY_ID: '152',
  CASHOUT_MS: 'https://cashout.internal.stg.coral.co.uk',
  TIMELINE_MS: 'wss://timeline-api.internal.stg.coral.co.uk',
  QUESTION_ENGINE_ENDPOINT:'https://question-engine.internal.stg.coral.co.uk/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  ISEVENTCOALESCING: true,
  FLAG_CLIENT_KEY: '6511861398fc3f12abcd54fc'
});
