import productionConfig from './environment.production';

import * as merge from 'lodash.merge';

const prodConfig = JSON.parse(JSON.stringify(productionConfig));

/* tslint:disable */
export default merge(prodConfig, {
  ENVIRONMENT: 'hiddenprod',
  brand: 'ladbrokes',
  BPP_ENDPOINT: 'https://bpp-perf.ladbrokes.com/Proxy',
  SURFACE_BETS_URL: 'https://surface-bets-hlv1.ladbrokes.com/cms/api',
  UPCELL_ENDPOINT: 'https://betreceipts.stress.ladbrokes.com',
  HORSE_RACING_CATEGORY_ID: '21',
  CMS_ENDPOINT: 'https://cms-hlv1.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-hlv1.ladbrokes.com/cms',
  CMS_LINK: 'https://cms-api-ui-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com',

  IMAGES_RACE_ENDPOINT: 'https://aggregation.stress.coral.co.uk/silks/racingpost',

  OPT_IN_ENDPOINT: 'https://optin.stress.ladbrokes.com',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.stress.ladbrokes.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.stress.ladbrokes.com/api/video/igame',
  FEATURED_SPORTS: 'wss://featured-publisher.stress.ladbrokes.com',
  INPLAYMS: 'wss://inplay-publisher.stress.ladbrokes.com',
  LIVESERVEMS: 'wss://liveserve-publisher.stress.ladbrokes.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip.stress.ladbrokes.com',
  EDPMS: 'https://edp.stress.ladbrokes.com',
  BIG_COMPETITION_MS: 'https://bigcompetition.stress.ladbrokes.com/competition',
  UPMS: 'https://upms.stress.ladbrokes.com/oddsPreference',
  TIME_ENDPOINT: 'https://hydra.stress.ladbrokes.com',
  TIMEFORM_ENDPOINT: 'https://timeform.beta.coral.co.uk',
  FREE_RIDE_PLACEBET_ENDPOINT: 'https://freeride.stress.ladbrokes.com/v1/api/freeride/placeBet',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.stress.ladbrokes.com/promosandbox/api/user-rank',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-hlv0.ladbrokes.com/',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.stress.ladbrokes.com',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet.stress.ladbrokes.com/api'
  },
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.ladbrokes.com',
    at_property: 'abaf3459-6df6-2b23-a718-f37546afeac0',
    betslip_at_property: '1b7662de-2a43-49f7-ec35-3afa39ad6b4a'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-hl.ladbrokes.com',
    ENV: 'perf'
  },
  //CASHOUT_MS: 'https://cashout-hlv2.ladbrokesoxygen.nonprod.cloud.ladbrokescoral.com',
  CASHOUT_MS: 'https://cashout.stress.ladbrokes.com',

  RACING_POST_API_ENDPOINT: 'https://df-api-gw-ldp-stage.ladbrokescoral.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'LDb1f382b9d06a4d50985829d59994cdf3',

  SITESERVER_DNS: 'https://ss-aka-ori-gib.ladbrokes.com',
  SITESERVER_BASE_URL: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer',
  SITESERVER_ENDPOINT: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-aka-ori-gib.ladbrokes.com/openbet-ssviewer/Commentary/2.31',

  LIVESERV: {
    DOMAIN: 'ladbrokes.com',
    PUSH_COMMON_SUBDOMAIN: 'ladbrokes.com',
    PUSH_LOCATION_HANDLER: '',
    PUSH_URL: 'https://push-perf.ladbrokes.com',
    PUSH_INSTANCE_URL: 'push-perf.ladbrokes.com',
    PUSH_INSTANCE_PORT: '443',
    PUSH_INSTANCE_TYPE: 'AJAX',
    PUSH_IFRAME_ID: 'push_iframe',
    PUSH_VERSION: 'e8382d8b7866e9a11d3529d8fe438008'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown2.stress.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath: 'https://showdown2.stress.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown2.stress.ladbrokes.com/showdown/api/mybets'
  },
  GAMING_URL: ['https://beta-www.ladbrokes.com/en/games'],
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.beta.coral.co.uk/api',
  TIMELINE_MS: 'wss://timeline-api.stress.ladbrokes.com',
  // Added for performance testing
  BET_TRACKER_ENDPOINT: 'https://modules-tst1.coral.co.uk/coupon-buddy/bettracker-grid/',
  SHOWDOWN_MS: 'https://showdown2.stress.ladbrokes.com/showdown/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://one-api-retail-stg.ladbrokes.com/v4/customer-api/customers',
    API_KEY: 'LR040572f6adf949ef8ee30dc328bd8f46'
  },
  ISEVENTCOALESCING: true,
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld-stage.ladbrokescoral.com/sdm-fanzone/standings',
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-cdd-stage.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  FLAG_CLIENT_KEY: '65116d0b24aa8411dbc31170'
});
/* tslint:enable */
