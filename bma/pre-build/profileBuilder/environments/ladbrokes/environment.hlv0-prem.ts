import productionConfig from './environment.production';

import * as merge from 'lodash.merge';
const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  ENVIRONMENT: 'hiddenprod',
  HORSE_RACING_CATEGORY_ID: '21',
  BPP_ENDPOINT: 'https://hl-bpp.ladbrokes.com/Proxy',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.beta.ladbrokes.com/silks/racingpost',
  SURFACE_BETS_URL: 'https://surface-bets-hlv0.ladbrokes.com/cms/api',
  CMS_ENDPOINT: 'https://cms-hl.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-hl.ladbrokes.com/cms',
  UPCELL_ENDPOINT: 'https://betreceipts.beta.ladbrokes.com',
  CMS_LINK: 'https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com',
  OPT_IN_ENDPOINT: 'https://optin.beta.ladbrokes.com',
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.beta.coral.co.uk/api',
  COMMUNICATION_URL: 'https://beta-myaccount.ladbrokes.com/en/mobileportal/communication',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.beta.ladbrokes.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.beta.ladbrokes.com/api/video/igame',
  FEATURED_SPORTS: 'wss://featured-publisher.beta.ladbrokes.com',
  INPLAYMS: 'wss://inplay-publisher.beta.ladbrokes.com',
  LIVESERVEMS: 'wss://liveserve-publisher.beta.ladbrokes.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip.beta.ladbrokes.com',
  EDPMS: 'https://edp.beta.ladbrokes.com',
  BIG_COMPETITION_MS: 'https://bigcompetition.beta.ladbrokes.com/competition',
  UPMS: 'https://upms.beta.ladbrokes.com/oddsPreference',
  TIME_ENDPOINT: 'https://hydra.beta.ladbrokes.com',
  TIMEFORM_ENDPOINT: 'https://timeform.beta.coral.co.uk',
  FREE_RIDE_PLACEBET_ENDPOINT: 'https://freeride.beta.ladbrokes.com/v1/api/freeride/placeBet',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.beta.ladbrokes.com/promosandbox/api/user-rank',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-hlv0.ladbrokes.com/',
  ONE_TWO_FREE_API_ENDPOINT:'https://otf-api.beta.ladbrokes.com/',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.beta.ladbrokes.com',
  BYB_CONFIG: {
    uri: 'https://buildyourbet.beta.ladbrokes.com/api'
  },
  FIVEASIDE: {
    contestPath: 'https://showdown2.beta.ladbrokes.com/showdown/api/contest/contest-prizes/',
    svgImagePath: '/images/uploads/svg/',
    entryConfirmationPath:'https://showdown2.beta.ladbrokes.com/showdown/api/entryconfirmation',
    fiveasidebetsPath: 'https://showdown2.beta.ladbrokes.com/showdown/api/mybets'
  },
  GAMING_URL: ['https://beta-www.ladbrokes.com/en/games'],
  AEM_CONFIG: {
    server: 'https://banners-cms.ladbrokes.com',
    at_property: 'd01b458f-4505-86d5-3d58-64113bb70196',
    betslip_at_property: '4b720044-1be9-de72-e197-8c8b530537a6'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  CASHOUT_MS: 'https://cashout.beta.ladbrokes.com',
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-hl.ladbrokes.com',
    ENV: 'prod'
  },
  COUPON_STATS_EXTERNAL_URL: 'https://df-api-gw-com.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  //QUESTION_ENGINE_ENDPOINT: 'https://question-engine.beta.coral.co.uk/api',
  QUESTION_ENGINE_ENDPOINT: 'https://question-engine.beta.ladbrokes.com/api',
  TIMELINE_MS: 'wss://timeline-api.beta.ladbrokes.com',
  // Adding BET_TRACKER_ENDPOINT for testing purpose
  BET_TRACKER_ENDPOINT: 'https://modules-beta.coral.co.uk/coupon-buddy/bettracker-grid/',
  BET_FILTER_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/oxygen-grid/',
  SHOWDOWN_MS: 'https://showdown2.beta.ladbrokes.com/showdown/api',
  HOME_PAGE: 'https://beta-sports.ladbrokes.com',
  DIGITAL_COUPONS_ENDPOINT: 'https://modules-tst2.coral.co.uk/coupon-buddy/digital/grid/static/',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  ISEVENTCOALESCING: true,
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '65116d28c20b3112c6bab1b7'
});
