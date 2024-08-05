/**
 * @ngdoc const
 * @type {{accumulatorBet: string, mainBetTypes: string[]}}
 */
export const BET_TYPES = {
  accumulatorBet: 'AC',
  singleAboutBet: 'SS',
  doubleAboutBet: 'DS',
  mainBetTypes: ['DBL', 'TBL', 'TRX', 'GOL', 'HNZ', 'PAT', 'YAN', 'L15', 'YAN', 'SHNZ', 'L31', 'L63', 'CAN']
};

/**
 * @ngdoc const
 * @type {{ERRORS: {OUTCOME_SUSPENDED: string, SELECTION_SUSPENDED: string, MARKET_SUSPENDED: string,
 * EVENT_SUSPENDED: string, EVENT_STARTED: string, STAKE_TOO_HIGH: string, MINIMUM_STAKE: string,
 * HANDICAP_CHANGED: string, PRICE_CHANGED: string, SELECTION_REMOVED: string}, ANDROID_NATIVE: string,
 * OLD_IOS: number, MAX_AMOUNT: number}}
 */
export const BETSLIP_VALUES = {
  ERRORS: {
    OUTCOME_SUSPENDED: 'OUTCOME_SUSPENDED',
    SELECTION_SUSPENDED: 'SELECTION_SUSPENDED',
    MARKET_SUSPENDED: 'MARKET_SUSPENDED',
    EVENT_SUSPENDED: 'EVENT_SUSPENDED',
    EVENT_STARTED: 'EVENT_STARTED',
    STAKE_TOO_HIGH: 'STAKE_TOO_HIGH',
    STAKE_TOO_LOW: 'STAKE_TOO_LOW',
    MINIMUM_STAKE: 'MINIMUM_STAKE',
    HANDICAP_CHANGED: 'HANDICAP_CHANGED',
    PRICE_CHANGED: 'PRICE_CHANGED',
    SELECTION_REMOVED: 'SELECTION_REMOVED',
    BAD_FREEBET_TOKEN: 'BAD_FREEBET_TOKEN',
    INVALID_LUCKYDIP_SELECTION: 'LuckyDip selection is not allowed'
  },
  ANDROID_NATIVE: 'Android Browser',
  OLD_IOS: 9,
  MAX_AMOUNT: 999999999999,
  IN_MS:1000
};

/**
 * @ngdoc const
 * @type {{AH: string, HH: string, MH: string, WH: string, HL: string}}
 */
export const handicapByMarketCode = {
  AH: 'ASIAN_FULLTIME',
  HH: 'MATCH_HANDICAP',
  MH: 'MATCH_HANDICAP',
  WH: 'WESTERN_HANDICAP',
  HL: 'HIGHER_LOWER'
};

export const modelByType = {
  SGL: 'sportsLegService',
  FORECAST: 'forecastSportsLegService',
  TRICAST: 'forecastSportsLegService',
  SCORECAST: 'scorecastSportsLegService',
  MATCH_HANDICAP: 'handicapSportsLegService',
  ASIAN_FULLTIME: 'handicapSportsLegService',
  WESTERN_HANDICAP: 'handicapSportsLegService',
  HIGHER_LOWER: 'handicapSportsLegService'
};

export const LUCKY_TYPES = {
  L15:{
    NUM_WIN_1: '1',
    ALL_WIN: '4',
    TYPE: 'L15',
    NAME: 'LUCKY15'
  },
  L31:{
    NUM_WIN_1: '1',
    NUM_WIN_4: '4',
    ALL_WIN: '5',
    TYPE: 'L31',
    NAME: 'LUCKY31'
  },
  L63:{
    NUM_WIN_1: '1',
    NUM_WIN_5: '5',
    ALL_WIN: '6',
    TYPE: 'L63',
    NAME: 'LUCKY63'
  }
}

