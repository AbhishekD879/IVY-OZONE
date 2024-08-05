import { lotteriesConfig } from '../configs/lotteriesLadbrokesConfig';
import { toteClasses } from '../configs/toteClasses';
import productionConfig from './environment.production';

import * as merge from 'lodash.merge';

const prodConfig = JSON.parse(JSON.stringify(productionConfig));

export default merge(prodConfig, {
  ENVIRONMENT: 'stg',
  BPP_ENDPOINT: 'https://bpp.internal.stg.ladbrokes.com/Proxy',
  SITESERVER_BASE_URL: 'https://ss-stg.ladbrokes.com/openbet-ssviewer',
  SITESERVER_DNS: 'https://ss-stg.ladbrokes.com',
  SITESERVER_ENDPOINT: 'https://ss-stg.ladbrokes.com/openbet-ssviewer/Drilldown/2.31',
  SITESERVER_COMMON_ENDPOINT: 'https://ss-stg.ladbrokes.com/openbet-ssviewer/Common/2.31',
  SITESERVER_LOTTERY_ENDPOINT: 'https://ss-stg.ladbrokes.com/openbet-ssviewer/Lottery/2.31',
  SITESERVER_HISTORIC_ENDPOINT:
    'https://ss-stg.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.65',
  SITESERVER_COMMENTARY_ENDPOINT:
    'https://ss-stg.ladbrokes.com/openbet-ssviewer/Commentary/2.31',
  SURFACE_BETS_URL: 'https://surface-bets-stg0.ladbrokes.com/cms/api',
  CMS_ENDPOINT: 'https://cms-stg.ladbrokes.com/cms/api',
  CMS_ROOT_URI: 'https://cms-stg.ladbrokes.com/cms',
  CMS_LINK: 'https://cms-api-ui-stg0.coralsports.nonprod.cloud.ladbrokescoral.com/',
  CMS_DYNAMIC_ENDPOINT: 'https://bpp.internal.stg.ladbrokes.com/Proxy/cms',
  ATR_END_POINT: 'https://bwt1.attheraces.com/ps/api',
  API_KEY: '4EaZxV5ZaxVzVW1G!dbACRGc!2G$R$EqFFzEQxWGtfwT%st@rRXZXEb%qszcxFQ!',
  LIVE_SIM_ENDPOINT: 'https://www.racemodlr.com/coral-demo/visualiser/',
  QUANTUMLEAP_SCRIPT_ENDPOINT: 'https://www-racemodlr.quantumleapsolutions.co.uk/ladbrokesV3/live_sim/mobile/?ver=7Sep2023',
  VISUALIZATION_ENDPOINT: 'https://vis-tst2-coral.symphony-solutions.eu',
  PROMO_LB_ENDPOINT:'https://promo-sandbox.internal.tst.ladbrokes.com/promosandbox/api/user-rank',
  QUANTUMLEAP_BOOKMAKER: 'Ladbrokes-Stage',
  ACCOUNT_WITHDRAWAL_THRESHOLD: 100,
  VISUALIZATION_IFRAME_URL: 'https://vis-static-tst2.coral.co.uk',
  VISUALIZATION_PREMATCH_URL: 'https://vis-static-tst2.coral.co.uk/football/pre-match.html',
  DIGITAL_SPORTS_IFRAME_URL: 'https://betbuilder.digitalsportstech.com/?sb=coraldev',
  DIGITAL_SPORTS_SYSTEM_ID: 982,
  STATS_CENTRE_ENDPOINT: 'https://stats-centre.internal.stg.coral.co.uk/api',
  OPT_IN_ENDPOINT: 'https://optin.internal.stg.ladbrokes.com',
  ONE_TWO_FREE_ENDPOINT: 'https://otf-stg0.coral.co.uk/',
  ONE_TWO_FREE_API_ENDPOINT:'https://otf-api.internal.dev.ladbrokes.com/',
  IG_MEDIA_TOTE_ENDPOINT: 'https://optin.internal.stg.ladbrokes.com/api/igamemedia',
  IG_MEDIA_ENDPOINT: 'https://optin.internal.stg.ladbrokes.com/api/video/igame',
  APOLLO: {
    API_ENDPOINT: 'https://apollo-tst2.coral.co.uk',
    CWA_ROUTE: 'cwa_api_index.php',
    UCMS_ROUTE: 'ucms_api_index.php',
    CARD_ENDPOINT: 'https://one-api-retail-stg.ladbrokes.com/v4/customer-api/customers',
    API_KEY: 'LR4248266D8DE44AD3A163532230B78CC3'
  },
  COMMUNICATION_URL: 'https://test.myaccount.ladbrokes.com/en/mobileportal/communication',
  BET_FINDER_ENDPOINT: 'https://api-racemodlr.quantumleapsolutions.co.uk/cypher/ladbrokesStage/0/',
  LIVESERV: {
    PUSH_URL: 'https://stg-push-lcm.ladbrokes.com',
    PUSH_INSTANCE_URL: 'stg-push-lcm.ladbrokes.com',
    PUSH_VERSION: 'e95460e14c00a85c132637426ef177bc',
    DOMAIN: 'ladbrokes.com',
    PUSH_COMMON_SUBDOMAIN: 'ladbrokes.com',
    PUSH_LOCATION_HANDLER: '',
  },
  BR_TYPE_ID: ['3048', '3049', '3123'],
  LOTTERIES_CONFIG: lotteriesConfig.stg,
  TOTE_CLASSES: toteClasses.tst,
  FEATURED_SPORTS: 'wss://featured-publisher.internal.stg.ladbrokes.com',
  INPLAYMS: 'wss://inplay-publisher.internal.stg.ladbrokes.com',
  LIVESERVEMS: 'wss://liveserve-publisher.internal.stg.ladbrokes.com',
  REMOTEBETSLIPMS: 'wss://remotebetslip.internal.stg.ladbrokes.com',
  EDPMS: 'https://edp.internal.stg.ladbrokes.com',
  BIG_COMPETITION_MS: 'https://bigcompetition.internal.stg.ladbrokes.com/competition',
  UPMS:'https://upms.internal.stg.ladbrokes.com/oddsPreference',
  AEM_CONFIG: {
    server: 'https://banners-cms-stg.ladbrokes.com',
    at_property: 'abaf3459-6df6-2b23-a718-f37546afeac0',
    betslip_at_property: '1b7662de-2a43-49f7-ec35-3afa39ad6b4a'
  },
  CSS_Lazy_loadash: '1234545464646464646',
  IMAGES_RACE_ENDPOINT: 'https://aggregation.internal.stg.ladbrokes.com/silks/racingpost',
  TIME_ENDPOINT: 'https://hydra.prod.ladbrokes.com',
  TIMEFORM_ENDPOINT: 'https://timeform-dev0.coralsports.dev.cloud.ladbrokescoral.com',
  FREE_RIDE_PLACEBET_ENDPOINT: 'https://freeride.internal.stg.ladbrokes.com/v1/api/freeride/placeBet',
  RACING_POST_API_ENDPOINT: 'https://sb-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_ONE_API_ENDPOINT: 'https://one-api-stg.ladbrokes.com/v4/sportsbook-api',
  RACING_POST_API_KEY: 'LDb1f382b9d06a4d50985829d59994cdf3',
  GAMING_URL: ['https://wpl-stg4-admin-gaming.ladbrokes.com'],
  IGAME_MEDIA_STREAM_ENDPOINT: 'https://player-test.igamemedia.com',
  IGM_STREAM_SERVICE_ENDPOINT: 'https://player-test.igamemedia.com/lib/v1.0/streamservice.js',
  VS_IGAME_MEDIA_STEAM_ID: '30473', // Temporary pointed to coral
  VS_QUOLITY_MAP: {
    desktop: 'adpt',
    tablet: 'adpt',
    mobile: 'adpt'
  },
  OPTA_SCOREBOARD: {
    CDN: 'https://opta-scoreboards-hl.ladbrokes.com',
    ENV: 'stage'
  },
  COUPON_STATS_EXTERNAL_URL:'https://df-api-gw-com-stage.ladbrokescoral.com/sdm-fe-scoreboards/ladbrokes/js/sdm-scoreboard-min.js',
  EXTERNAL_URL: {
    accountone: 'https://accountone-stg.ladbrokes.com',
    gaming: 'https://wpl-stg4-admin-gaming.ladbrokes.com',
    help: 'https://help.ladbrokes.com',
    'accountone-stg': 'https://accountone-stg.ladbrokes.com'
  },
  VIP_USERS_EXTERNAL_URL: 'https://wpl-stg4-admin-gaming.ladbrokes.com/vip',
  DESKTOP_VIP_USERS_EXTERNAL_URL: 'https://casino.ladbrokes.com/en/vip/new-benefits',
  NOTIFICATION_CENTER_ENDPOINT: 'https://notification-center.internal.stg.ladbrokes.com',
  BYB_CONFIG: {
    HR_YC_EVENT_TYPE_ID: 15031,
    uri: 'https://buildyourbet.internal.stg.ladbrokes.com/api'
  },
  CASHOUT_MS: 'https://cashout.internal.stg.ladbrokes.com',
  IDENTITY_ID: 'eu-west-2:45d28ab7-f7ee-47ac-b0f6-27c4d10c593a',
  BET_TRACKER_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/bettracker-grid/',
  BET_FILTER_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/oxygen-grid/',
  TIMELINE_MS: 'wss://timeline-api.internal.stg.ladbrokes.com',
  DIGITAL_COUPONS_ENDPOINT: 'https://modules-stg.coral.co.uk/coupon-buddy/digital/grid/static/',
  GOOGLE_RECAPTCHA: {
    uri: 'https://www.google.com/recaptcha/enterprise.js?render=',
    ACCESS_TOKEN: '6LcEiHIaAAAAAJUAFVjakE1JSlikDZHWlGxnlKjW'
  },
  ISEVENTCOALESCING: true,
  FANZONE_PREMIER_LEAGUE_ENDPOINT: 'https://df-api-gw-ld-stage.ladbrokescoral.com/sdm-fanzone/standings',
  FLAG_CLIENT_KEY: '65116d3ae7089d128d9aaf85'
});
