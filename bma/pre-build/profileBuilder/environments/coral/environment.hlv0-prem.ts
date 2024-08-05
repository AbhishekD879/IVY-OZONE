import productionConfig from './environment.production';
import * as merge from 'lodash.merge';

const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  googleTagManagerID: ['GTM-KW37JJ9'],
  production: true,
  ENVIRONMENT: 'hiddenprod',
  HORSE_RACING_CATEGORY_ID: '21',
  BPP_ENDPOINT: 'https://bp-hl.coral.co.uk/Proxy',
  INPLAYMS_ENDPOINT: 'https://bp-stg-coral.symphony-solutions.eu:444',
  SURFACE_BETS_URL: 'https://surface-bets-hlv0.coral.co.uk/cms/api',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.beta.coral.co.uk/silks/racingpost',
  CMS_ENDPOINT: 'https://cms-hl.coral.co.uk/cms/api',
  CMS_ROOT_URI: 'https://cms-hl.coral.co.uk/cms',
  CMS_LINK: 'https://cms-hl.coral.co.uk/cms',
  UPCELL_ENDPOINT: 'https://betreceipts.beta.coral.co.uk',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/coralV3/live_sim/mobile/?ver=7Sep2023',
  OPT_IN_ENDPOINT: 'https://optin.beta.coral.co.uk',
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.beta.coral.co.uk/api',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.beta.coral.co.uk/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.beta.coral.co.uk/api/video/igame',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-hlv0.coral.co.uk/',
  FEATURED_SPORTS: 'wss://featured-publisher.beta.coral.co.uk',
  INPLAYMS: 'wss://inplay-publisher.beta.coral.co.uk',
  LIVESERVEMS: 'wss://liveserve-publisher.beta.coral.co.uk',
  REMOTEBETSLIPMS: 'wss://remotebetslip.beta.coral.co.uk',
  EDPMS: 'https://edp.beta.coral.co.uk/',
  BIG_COMPETITION_MS: 'https://bigcompetition.beta.coral.co.uk/competition',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.beta.coral.co.uk/promosandbox/api/user-rank',
  UPMS: 'https://upms.beta.coral.co.uk/oddsPreference',
  TIME_ENDPOINT: 'https://hydra.beta.coral.co.uk',
  TIMEFORM_ENDPOINT: 'https://timeform.beta.coral.co.uk',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.beta.coral.co.uk',
  BYB_CONFIG: {
    uri: 'https://buildyourbet.beta.coral.co.uk/api'
  },
  GAMING_URL: ['https://beta-www.coral.co.uk/en/games'],
  AEM_CONFIG: {
    server: 'https://banners-cms.coral.co.uk',
    at_property: 'b637a0ef-3583-855d-e895-29b3eb3894e3',
    betslip_at_property: 'b7d701f3-01c8-23b7-2b1f-48b4423f6c8b'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  CASHOUT_MS: 'https://cashout.beta.coral.co.uk',
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-hl.coral.co.uk',
    ENV: 'prod'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-com.ladbrokescoral.com/sdm-fe-scoreboards/coral/js/sdm-scoreboard-min.js',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.beta.coral.co.uk/api',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  TIMELINE_MS: 'wss://timeline-api.beta.coral.co.uk',
  HOME_PAGE: 'https://beta-sports.coral.co.uk',
  BET_TRACKER_ENDPOINT: 'https://modules-beta.coral.co.uk/coupon-buddy/bettracker/',
  ISEVENTCOALESCING: true,
  FLAG_CLIENT_KEY: '651186094e07df121ec376bb' 
});
