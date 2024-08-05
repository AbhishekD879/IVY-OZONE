export const commandApi = {
  LAZY_LOAD: 'LAZY_LOAD',
  EVENT_VIDEO_STREAM: '@lazy-modules-module/eventVideoStream/event-video-stream.module#LazyEventVideoStreamModule:foo',

  GET_OPEN_BETS_COUNT: '@betHistoryModule/bet-history.module#BetHistoryModule:getOpenBetsCount',
  UNSUBSCRIBE_OPEN_BETS_COUNT: '@betHistoryModule/bet-history.module#BetHistoryModule:unsubscribeOpenBetsCount',
  GET_CASH_OUT_BETS_ASYNC: '@betHistoryModule/bet-history.module#BetHistoryModule:cashoutBets',
  GET_PLACED_BETS_ASYNC: '@betHistoryModule/bet-history.module#BetHistoryModule:placedBets',
  GET_BETS_FOR_EVENT_ASYNC: '@betHistoryModule/bet-history.module#BetHistoryModule:betsForEvent',
  OPEN_CASHOUT_STREAM: '@betHistoryModule/bet-history.module#BetHistoryModule:openBetsStream',
  CLOSE_CASHOUT_STREAM: '@betHistoryModule/bet-history.module#BetHistoryModule:closeStream',

  BETSLIP_READY: '@betslipModule/betslip.module#BetslipModule:init',
  BETSLIP_UPDATE_CARD_EXPIRATION_DATE: '@betslipModule/betslipDeposit/updateCardExpirationAge',
  SYNC_TO_BETSLIP: '@betslipModule/betslip.module#BetslipModule:syncToBetslip',
  ADD_TO_BETSLIP_BY_OUTCOME_IDS: '@betslipModule/betslip.module#BetslipModule:addToBetSlip',
  IS_ADDTOBETSLIP_IN_PROCESS: '@betslipModule/betslip.module#BetslipModule:isAddToBetslip',
  GET_EVENTS_BY_OUTCOME_IDS: '@betslipModule/betslip.module#BetslipModule:getEventsByOutcomeIds',
  OPEN_BETSLIP: '@betslipModule/betslip.module#BetslipModule:openBetslip',

  SHOW_QUICKBET: '@quickbetModule/quickbet.module#QuickbetModule:show',
  QUICKBET_RESTORE: '@quickbetModule/quickbet.module#QuickbetModule:restoreSelection',
  QUICKBET_SHOW_ERROR: '@quickbetModule/quickbet.module#QuickbetModule:showErrorMessage',
  QUICKBET_CLEAR_ERROR: '@quickbetModule/quickbet.module#QuickbetModule:clearErrorMessage',

  BESTLIP_ERROR_TRACKING: 'app/betPlacementErrorTracking',
  CHECK_USER_PLACED_RETAIL_BET: 'connect/checkUserPlacedRetailBet',
  DS_READY: '@player-props/player-props.module#PlayerPropsModule:init',

  // your call  module comands
  DS_WHEN_YC_READY: '@yourCallModule/your-call.module#YourCallModule:whenYCReady',
  DS_WHEN_YC_STATIC_BLOCKS_READY: '@yourCallModule/your-call.module#YourCallModule:whenYCStaticBlocksReady',
  DS_GET_GAME: '@yourCallModule/your-call.module#YourCallModule:getGame',
  GET_YC_TAB: '@yourCallModule/your-call.module#YourCallModule:insertYCTab',
  GET_YC_BETS: '@yourCallModule/your-call.module#YourCallModule:getYCbets',
  DS_IS_AVAILABLE_FOR_COMPETITION: '@yourCallModule/your-call.module#YourCallModule:dsIsAvailableForCompetition',
  DS_IS_AVAILABLE_FOR_EVENTS: '@yourCallModule/your-call.module#YourCallModule:dsIsAvailableForEvents',


  // auth module commands
  BPP_AUTH_SEQUENCE: 'auth/bppAuthSequence',
  WHEN_PROXY_SESSION: 'auth/whenSesionFactory/whenProxySession',

  // stats module commands
  GET_COMPETITION_AND_SEASON: '@app/stats/stats.module#StatsModule:getCompetitionAndSeason',
  GET_SEASON: '@app/stats/stats.module#StatsModule:getSeason',
  GET_SEASONS: '@app/stats/stats.module#StatsModule:getSeasons',
  GET_MATCHES_BY_SEASON: '@app/stats/stats.module#StatsModule:getMatchesBySeasonByPage',
  GET_RESULTS_BY_PAGE: '@app/stats/stats.module#StatsModule:getPage',
  GET_MATCHES_BY_DATE: '@app/stats/stats.module#StatsModule:getMatchesByDate',
  GET_RESULT_TABLES: '@app/stats/stats.module#StatsModule:getResultsTables',
  GET_LEAGUE_TABLE: '@app/stats/stats.module#StatsModule:leagueTableCompetitionSeason',

  // vip module commands
  GET_VIP_INFO: 'vip/getVipInfo',

  // oddsboost module commands
  GET_ODDS_BOOST_ACTIVE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:isBoostActive',
  GET_ODDS_BOOST_ACTIVE_FROM_STORAGE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getBoostActiveFromStorage',
  GET_ODDS_BOOST_TOKENS: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getOddsBoostTokens',
  ODDS_BOOST_SET_MAX_VAL: '@oddsBoostModule/odds-boost.module#OddsBoostModule:setMaxBoostValue',
  ODDS_BOOST_MAX_STAKE_EXCEEDED: '@oddsBoostModule/odds-boost.module#OddsBoostModule:isMaxStakeExceeded',
  ODDS_BOOST_SHOW_FB_DIALOG: '@oddsBoostModule/odds-boost.module#OddsBoostModule:showOddsBoostFreeBetDialog',
  ODDS_BOOST_SHOW_SP_DIALOG: '@oddsBoostModule/odds-boost.module#OddsBoostModule:showOddsBoostSpDialog',
  ODDS_BOOST_OLD_PRICE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getOldPriceFromBetslipStake',
  ODDS_BOOST_NEW_PRICE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getNewPriceFromBetslipStake',
  ODDS_BOOST_OLD_QB_PRICE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getOldPriceFromQuickBet',
  ODDS_BOOST_NEW_QB_PRICE: '@oddsBoostModule/odds-boost.module#OddsBoostModule:getNewPriceFromQuickBet',
  ODDS_BOOST_TOKENS_SHOW_POPUP: '@oddsBoostModule/odds-boost.module#OddsBoostModule:showTokensInfoDialog',
  ODDS_BOOST_SETTLE_TOKEN: '@oddsBoostModule/odds-boost.module#OddsBoostModule:settleOddsBoostTokens',
  ODDS_BOOST_INIT: '@oddsBoostModule/odds-boost.module#OddsBoostModule:init',

  PROMOTIONS_SHOW_OVERLAY: 'promotions/promotionsFactory/openPromotionOverlay',

  // racing
  HR_ENHANCED_MULTIPLES_EVENTS: '@racingModule/racing.module#RacingModule:getEnhancedMultiplesEvents',
  RACING_GA_SERVICE: '@racingModule/racing.module#RacingModule:racingGaService',

  SYNC_FAVOURITES_FROM_NATIVE: 'favourites/favouritesService/syncFromNative',

  OPT_IN_SPLASH_UPDATE_STATE: 'bma/optInSplash/updateState',
  OPT_IN_INACTIVE_USER: 'bma/policiesBanner/optInChecked',
  UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE: 'bma/updateEventWithLiveUpdate',
  GET_SYS_CONFIG: 'bma/main',
  TOGGLE_FOOTER_MENU: 'bma/footerSection/toggleFooterVisibility',
  SHOW_HIDE_FOOTER_MENU: 'bma/footerSection/showHideFooterVisibility',

  LOAD_COMPETITION_EVENTS: '@inplayModule/inplay.module#InplayModule:loadData',
  SUBSCRIBE_FOR_LIVE_UPDATES: '@inplayModule/inplay.module#InplayModule:subscribeForLiveUpdates',
  UNSUBSCRIBE_FOR_LIVE_UPDATES: '@inplayModule/inplay.module#InplayModule:unsubscribeForLiveUpdates',
  GET_LIVE_STREAM_STATUS: 'sb/eventVideoStream',
  IS_ACCOUNT_CLOSED: '@accountModule/account.module#AccountModule:isAccountClosed', // TODO: Should be removed after Vanilla integration
  KYC_REDIRECT_TO_NETVERIFY: 'kyc/redirectToNetverify',
  KYC_REDIRECT_TO_NETVERIFY_MULTIDOC: 'kyc/redirectToNetverifyMultidoc'
};
