export const cashoutConstants = {
  tooltipTime: 5000,
  flashingTime: 6200,
  balanceTimeInterval: 5000,
  readBetTime: 2000,
  second: 1000,
  displaySuccess: 3900,
  partialAnimatingTime: 500,
  partialFinishAnimating: 500,
  decrease: 'decrease',
  suspend: 'SELN_SUSP',
  pending: 'CASHOUT_PENDING',
  changed: 'CASHOUT_VALUE_CHANGED',
  priceChange: 'PRICE_CHANGE',
  success: 'Y',
  betWorthNothing: '0.00',
  betLowCashout: 'BET_LOW_CASHOUT',
  minValueForPartial: 0.1,
  status: ['SELN_SUSP ', 'SELN_NOT_DISP ', 'LINE_NO_CASHOUT ', 'BET_WORTH_NOTHING ', 'INTERNAL_ERROR '],
  values: ['CASHOUT_SELN_SUSPENDED', 'DB_ERROR'],
  cashoutSuspendedStatuses: ['SELN_SUSP', 'SELN_NOT_DISP', 'CASHOUT_SELN_SUSPENDED'],
  betLocation: {
    MY_BETS: 'myBetsTab',
    CASH_OUT_SECTION: 'cashOutSection',
    REGULAR_BETS: 'openBets'
  },
  gtmBetLocation: {
    MY_BETS: 'event page',
    CASH_OUT_SECTION: 'cash out page',
    REGULAR_BETS: 'openBets'
  },
  controllers: {
    CASH_OUT_WIDGET_CTRL: 'CashoutWidgetController',
    MY_BETS_CTRL: 'MyBetsController',
    REGULAR_BETS_CTRL: 'RegularBetsController'
  },
  result: {
    YES: 'Y',
    NO: 'N',
    MISSED: 'N/A'
  },
  cashOutType: {
    FULL: 'full',
    PARTIAL: 'partial'
  },
  cashOutAttempt: {
    SUCCESS: 'success',
    ERROR: 'error',
    SUSPENDED: 'suspended'
  },
  cashOutGtm: {
    EVENT: 'trackEvent',
    CATEGORY: 'cash out',
    ACTION: 'attempt',
    SUCCESS: 'success',
    FAILURE: 'failure'
  },
  channelName: {
    event: 'sEVENT',
    score: 'sSCBRD',
    clock: 'sCLOCK',
    market: 'sEVMKT',
    selection: 'sSELCN',
    facts: 'sFACTS'
  },
  keyProperties: {
    outcome: 'outcome',
    market: 'market',
    event: 'event'
  },
  resultCodes: {
    W: 'won', L: 'lost', V: 'void'
  },
  handicapResultCode: 'H',
  betSettledStatus: 'BET_SETTLED'
};

