import * as merge from 'lodash.merge';
import productionConfig from './environment.production';
const prodConfig = JSON.parse(JSON.stringify(productionConfig));
export default merge(prodConfig, {
  googleTagManagerID: ['GTM-KW37JJ9'],
  production: true,
  ENVIRONMENT: 'hiddenprod',
  HORSE_RACING_CATEGORY_ID: '21',
  UPCELL_ENDPOINT: 'https://betreceipts.stress.coral.co.uk',
  SITESERVER_BASE_URL: 'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-aka-ori-gib.coral.co.uk',
  SITESERVER_ENDPOINT: 'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT: 'https://ss-aka-ori-gib.coral.co.uk/openbet-ssviewer/Commentary/2.31',
  BPP_ENDPOINT: 'https://bpp-perf.coral.co.uk/Proxy',
  LIVESERV: {
    DOMAIN: 'coral.co.uk',
    PUSH_COMMON_SUBDOMAIN: 'coral.co.uk',
    PUSH_LOCATION_HANDLER: '',
    PUSH_URL: 'https://push-perf.coral.co.uk',
    PUSH_INSTANCE_URL: 'push-perf.coral.co.uk',
    PUSH_INSTANCE_PORT: '443',
    PUSH_INSTANCE_TYPE: 'AJAX',
    PUSH_IFRAME_ID: 'push_iframe',
    PUSH_VERSION: 'e8382d8b7866e9a11d3529d8fe438008'
  },
  IMAGES_RACE_ENDPOINT: 'https://aggregation.stress.coral.co.uk/silks/racingpost',
  RACING_POST_API_ENDPOINT: 'https://df-api-gw-cdr-stage.ladbrokescoral.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.coral.co.uk/v4/sportsbook-api',
  RACING_POST_API_KEY: 'CD3DDB282FF116480AB3BB3113AAF316FE',
  SURFACE_BETS_URL: 'https://surface-bets-hlv1.coral.co.uk/cms/api',
  CMS_ENDPOINT: 'https://cms-hlv1.coral.co.uk/cms/api',
  CMS_ROOT_URI: 'https://cms-hlv1.coral.co.uk/cms',
  CMS_LINK: 'https://cms-hlv1.coral.co.uk/',
  OPT_IN_ENDPOINT: 'https://optin.stress.coral.co.uk',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.stress.coral.co.uk/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.stress.coral.co.uk/api/video/igame',
  FEATURED_SPORTS: 'wss://featured-publisher.stress.coral.co.uk',
  INPLAYMS: 'wss://inplay-publisher.stress.coral.co.uk',
  LIVESERVEMS: 'wss://liveserve-publisher.stress.coral.co.uk',
  REMOTEBETSLIPMS: 'wss://remotebetslip.stress.coral.co.uk',
  EDPMS: 'https://edp.stress.coral.co.uk',
  BIG_COMPETITION_MS: 'https://bigcompetition.stress.coral.co.uk/competition',
  UPMS: 'https://upms.stress.coral.co.uk/oddsPreference',
  TIME_ENDPOINT: 'https://hydra.stress.coral.co.uk',
  CASHOUT_MS: 'https://cashout.stress.coral.co.uk',
  NOTIFICATION_CENTER_ENDPOINT:
    'https://notification-center.stress.coral.co.uk',
  VISUALIZATION_ENDPOINT: 'https://vis-stg2-coral.symphony-solutions.eu',
  VISUALIZATION_TENNIS_ENDPOINT: 'https://coral-vis-tennis-stg2.symphony-solutions.eu',
  VISUALIZATION_IFRAME_URL: 'https://vis-static-stg2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-stg2.coral.co.uk/football/pre-match.html',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.stress.coral.co.uk/promosandbox/api/user-rank',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.coral.co.uk',
    at_property: '63909eaa-a987-2833-6631-85b5ced26e68',
    betslip_at_property: '0c727079-a884-88b9-1fd8-faa96c1a6fa7'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  GAMING_URL: ['https://beta-www.coral.co.uk/en/games'],
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 34799,
    uri: 'https://buildyourbet.stress.coral.co.uk/api'
  },
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-hl.coral.co.uk',
    ENV: 'perf'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-cdd-stage.ladbrokescoral.com/sdm-fe-scoreboards/coral/js/sdm-scoreboard-min.js',
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/coralDublin/0/',
  BET_FILTER_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/oxygen/',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.stress.coral.co.uk/api/v1',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  TIMELINE_MS: 'wss://timeline-api.stress.coral.co.uk',
  ISEVENTCOALESCING: true,
  FLAG_CLIENT_KEY: '651185f89d1f2d12c00ce71f'
});
