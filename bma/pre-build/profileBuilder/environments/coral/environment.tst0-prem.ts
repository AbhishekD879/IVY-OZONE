import { lotteriesConfig } from '../configs/lotteriesConfig';
import { toteClasses } from '../configs/toteClasses';

import productionConfig from './environment.production';
import * as merge from 'lodash.merge';
const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  production: true,
  ENVIRONMENT: 'tst2',
  HORSE_RACING_CATEGORY_ID: '21',
  BPP_ENDPOINT: 'https://bpp.internal.tst.coral.co.uk/Proxy',
  UPCELL_ENDPOINT: 'https://betreceipts.internal.tst.coral.co.uk',
  SITESERVER_BASE_URL: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-tst2-tmp.coral.co.uk',
  SITESERVER_ENDPOINT: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-tst2-tmp.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  SURFACE_BETS_URL: 'https://surface-bets-tst0.coral.co.uk/cms/api',
  CMS_ENDPOINT: 'https://cms-tst0.coral.co.uk/cms/api',
  CMS_ROOT_URI: 'https://cms-tst0.coral.co.uk/cms',
  CMS_LINK: 'https://cms-api-ui-tst0.coralsports.nonprod.cloud.ladbrokescoral.com',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/coralV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-tst2-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis-tst2.symphony-solutions.eu',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.tst.coral.co.uk/promosandbox/api/user-rank',
  QUANTUMLEAP_BOOKMAKER: 'Coral-Test-2',
  TOTE_CLASSES: toteClasses.tst,
  LOTTERIES_CONFIG: lotteriesConfig.tst,
  VISUALIZATION_IFRAME_URL: 'https://vis-static-tst2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-tst2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coraldev',
  DIGITAL_SPORTS_SYSTEM_ID: 982,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre-tst0.coral.co.uk/api',
  OPT_IN_ENDPOINT: 'https://optin.internal.tst.coral.co.uk',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.internal.tst.coral.co.uk/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.internal.tst.coral.co.uk/api/video/igame',
  VS_QUOLITY_MAP: {
    desktop: 'web',
    tablet: 'mobhi',
    mobile: 'moblo'
  },
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player-test.igamemedia.com/lib/v1.0/streamservice.js',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://one-api-retail-stg.coral.co.uk/v4/customer-api/customers',
    API_KEY: 'CRfc83f4d5d5e14eeab096e072fe6851b7'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown.internal.tst.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown.internal.tst.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown.internal.tst.ladbrokes.com/showdown/api/mybets'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/coralTest2/0/',
  BET_FILTER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/oxygen/',
  BET_TRACKER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/bettracker/',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.internal.tst.coral.co.uk',
  LIVESERV: {
    PUSH_URL: 'https://push-tst2.coral.co.uk',
    PUSH_INSTANCE_URL: 'push-tst2.coral.co.uk',
    PUSH_VERSION: 'c3e5103c451ba491d75a024811deba7f'
  },
  BR_TYPE_ID: ['3048', '3049', '3123'],
  FEATURED_SPORTS: 'wss://featured-publisher.internal.tst.coral.co.uk',
  INPLAYMS: 'wss://inplay-publisher.internal.tst.coral.co.uk',
  LIVESERVEMS: 'wss://liveserve-publisher.internal.tst.coral.co.uk',
  HOME_PAGE: 'https://qa2.sports.coral.co.uk',
  REMOTEBETSLIPMS: 'wss://remotebetslip.internal.tst.coral.co.uk',
  EDPMS: 'https://edp.internal.tst.coral.co.uk',
  BIG_COMPETITION_MS: 'https://bigcompetition.internal.tst.coral.co.uk/competition',
  UPMS: 'https://upms.internal.tst.coral.co.uk/oddsPreference',
  IMAGES_RACE_ENDPOINT: 'https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost',
  RACING_POST_API_ENDPOINT: 'https://sb-api-dev.coral.co.uk/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'CD3DDB282FF116480AB3BB3113AAF316FE',  
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-dev0.coral.co.uk',
    ENV: 'dev'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-com-test.ladbrokescoral.com/sdm-fe-scoreboards/coral/js/sdm-scoreboard-min.js',
  BET_GENIUS_SCOREBOARD: {
    scorecentre: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/page/ladbrokescoral/basketballscorecentre',
    api: 'https://ladbrokescoral-uat.betstream.betgenius.com/betstream-view/public/bg_api.js'
  },
  TIME_ENDPOINT: 'https://hydra.internal.tst.coral.co.uk',
  TIMEFORM_ENDPOINT: 'https://timeform.internal.tst.coral.co.uk',
  GAMING_URL: ['https://mcasino-tst2.coral.co.uk'],

  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet.internal.tst.coral.co.uk/api'
  },
  CASHOUT_MS: 'https://cashout.internal.tst.coral.co.uk',
  CSS_Lazy_loadash: '1234545464646464646',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.coral.co.uk',
    at_property: '63909eaa-a987-2833-6631-85b5ced26e68',
    betslip_at_property: '0c727079-a884-88b9-1fd8-faa96c1a6fa7'
  },
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.internal.dev.coral.co.uk/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  TIMELINE_MS: 'wss://timeline-api.internal.tst.coral.co.uk',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  ISEVENTCOALESCING: true,
  FLAG_CLIENT_KEY: '64eca041795d241275a129f4'
});
