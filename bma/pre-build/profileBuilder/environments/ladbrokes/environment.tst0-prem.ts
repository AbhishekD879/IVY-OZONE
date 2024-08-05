import { lotteriesConfig } from '../configs/lotteriesLadbrokesConfig';
import { toteClasses } from '../configs/toteClasses';
import productionConfig from './environment.production';

import * as merge from 'lodash.merge';

const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  production: false,
  ENVIRONMENT: 'tst2',
  HORSE_RACING_CATEGORY_ID: '21',
  UPCELL_ENDPOINT: 'https://betreceipts.internal.tst.ladbrokes.com',
  BPP_ENDPOINT: 'https://bpp.internal.tst.ladbrokes.com/Proxy',
  SITESERVER_BASE_URL: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-tst2.ladbrokes.com',
  SITESERVER_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-tst2.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT:
    'https://ss-tst2.ladbrokes.com/openbet-ssviewer/Commentary/2.31',
  SURFACE_BETS_URL: 'https://surface-bets-tst0.ladbrokes.com/cms/api',
  CMS_ENDPOINT: 'https://cms-tst0.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-tst0.ladbrokes.com/cms',
  CMS_LINK: 'https://cms-api-ui-tst0.coralsports.nonprod.cloud.ladbrokescoral.com',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/ladbrokesV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-tst2-coral.symphony-solutions.eu',
  QUANTUMLEAP_BOOKMAKER: 'Ladbrokes-Test2',
  VISUALIZATION_IFRAME_URL: 'https://vis-static-tst2.coral.co.uk',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.tst.ladbrokes.com/promosandbox/api/user-rank',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-tst2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coraldev',
  DIGITAL_SPORTS_SYSTEM_ID: 982,
  DOMAIN: '.ladbrokes.com',
  COMMUNICATION_URL: 'https://qa2.myaccount.ladbrokes.com/en/mobileportal/communication',
  STATS_CENTRE_ENDPOINT: 'https://statscenter-tst0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api',
  OPT_IN_ENDPOINT: 'https://optin.internal.tst.ladbrokes.com',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-dev0.coral.co.uk/',
  ONE_TWO_FREE_API_ENDPOINT:'https://otf-api.internal.dev.ladbrokes.com/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.internal.tst.ladbrokes.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.internal.tst.ladbrokes.com/api/video/igame',
  IMAGES_RACE_ENDPOINT: 'https://aggregation-tst0.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com/silks/racingpost',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://one-api-retail-stg.ladbrokes.com/v4/customer-api/customers',
    API_KEY: 'LR4248266D8DE44AD3A163532230B78CC3'
  },
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/ladbrokesTest2/0/',
  BET_FILTER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/oxygen-grid/',
  BET_TRACKER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/bettracker-grid/',
  DIGITAL_COUPONS_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/digital/grid/static/',
  LIVESERV: {
    PUSH_URL: 'https://tst2-push-lcm.ladbrokes.com',
    PUSH_INSTANCE_URL: 'tst2-push-lcm.ladbrokes.com',
    PUSH_VERSION: '1dd785e1de9a32e236b624ae268bb803',
    DOMAIN: 'ladbrokes.com',
    PUSH_COMMON_SUBDOMAIN: 'ladbrokes.com',
    PUSH_LOCATION_HANDLER: ''
  },
  FIVEASIDE: {
    contestPath: 'https://showdown2.internal.tst.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown2.internal.tst.ladbrokes.com/showdown/api',
    fiveasidebetsPath: 'https://showdown2.internal.tst.ladbrokes.com/showdown/api/mybets'
  },
  BR_TYPE_ID: ['3048', '3049', '3123'],
  LOTTERIES_CONFIG: lotteriesConfig.tst,
  TOTE_CLASSES: toteClasses.tst,
  FEATURED_SPORTS: 'wss://featured-publisher.internal.tst.ladbrokes.com',
  INPLAYMS: 'wss://inplay-publisher.internal.tst.ladbrokes.com',
  CASHOUT_MS: 'https://cashout.internal.tst.ladbrokes.com',
  LIVESERVEMS: 'wss://liveserve-publisher.internal.tst.ladbrokes.com',
  HOME_PAGE: 'https://qa2.sports.ladbrokes.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip.internal.tst.ladbrokes.com',
  EDPMS: 'https://edp.internal.tst.ladbrokes.com',
  BIG_COMPETITION_MS: 'https://bigcompetition.internal.tst.ladbrokes.com/competition',
  UPMS:'https://upms.internal.tst.ladbrokes.com/oddsPreference',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.ladbrokes.com',
    at_property: 'abaf3459-6df6-2b23-a718-f37546afeac0',
    betslip_at_property: '1b7662de-2a43-49f7-ec35-3afa39ad6b4a'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  TIME_ENDPOINT: 'https://hydra.internal.tst.ladbrokes.com',
  TIMEFORM_ENDPOINT: 'https://timeform.internal.tst.coral.co.uk',
  RACING_POST_API_ENDPOINT: 'https://sb-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'LDb1f382b9d06a4d50985829d59994cdf3',
  GAMING_URL: ['https://slots.ladbrokes.com/en/games-tab'],
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-dev0.ladbrokes.com',
    ENV: 'dev'
  },
  COUPON_STATS_EXTERNAL_URL:'https://df-api-gw-com-test.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  googleTagManagerID: ['GTM-MZ45BFM'],
  EXTERNAL_URL: {
    accountone: 'https://accountone-test.ladbrokes.com',
    gaming: 'https://gaming.ladbrokes.com',
    help: 'https://help.ladbrokes.com',
    'accountone-stg': 'https://accountone-stg.ladbrokes.com',
    'accountone-test': 'https://accountone-test.ladbrokes.com'
  },
  VIP_USERS_EXTERNAL_URL: 'https://gaming.ladbrokes.com/vip',
  DESKTOP_VIP_USERS_EXTERNAL_URL: 'https://casino.ladbrokes.com/en/vip/new-benefits',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.internal.tst.ladbrokes.com',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet.internal.tst.ladbrokes.com/api'
  },
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.internal.dev.coral.co.uk/api',
  TIMELINE_MS: 'wss://timeline-api.internal.tst.ladbrokes.com',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player-test.igamemedia.com/lib/v1.0/streamservice.js',
  SHOWDOWN_MS: 'https://showdown2.internal.tst.ladbrokes.com/showdown/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  ISEVENTCOALESCING: true,
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld-test.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '64eca02c6a21dd1213f03acb'
});
