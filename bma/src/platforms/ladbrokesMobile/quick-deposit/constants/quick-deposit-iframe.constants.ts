export const QUICK_DEPOSIT_IFRAME_CONSTANTS = {
  ACTIONS: {
    OPEN: 'open',
    CLOSE: 'close',
    RESIZE: 'resize'
  },
  URL_PARAMS: {
    BRAND_ID: 'LADBROKEUK',
    PRODUCT_ID: 'SPORTSBOOK',
    // channel id diferentiation depends on platform BMA-47218
    CHANNEL_ID:  {
      mobile: 'MW',
      tablet: 'TB',
      landscapeTablet: 'TB',
      desktop: 'WC'
    },
    LANG_ID: 'en',
    PREFIX: 'ld'
  },
  EVENTS: {
    STAKE_CHANGE: 'StakeChange',
    PRICE_CHANGE: 'PriceChange',
    SUSPENDED: 'EventSuspended',
    UNSUSPENDED: 'EventUnSuspended'
  }
};
