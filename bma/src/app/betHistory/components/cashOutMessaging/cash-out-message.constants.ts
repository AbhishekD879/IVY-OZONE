export const SUSPENSION = {
  eventCashoutSuspension: 'cashout-event-suspension',
  marketCashoutSuspension: 'cashout-market-suspension',
};

export const CASHOUT_GTM = {
  senarioOne: {
    eventLabel: 'scenario one',
    eventDetails: 'events not traded in-play'
  },
  senarioTwo: {
    eventLabel: 'scenario two',
    eventDetails: 'markets not traded in-play'
  }
};

export const CASHOUT_SUSPENDED_WS = 'Suspended by cashout microservice: bet has suspended selection(s)';
export const CASHOUT_SUSPENDED = 'CASHOUT_SELN_SUSPENDED';
export const MESSAGE_LIMIT = 70;

export const CASHOUT_FLAGS = {
  NO: 'N',
  YES: 'Y',
  SUSP: 'S',
  ACTIVE: 'A',
  MARKET: 'market',
  EVENT: 'event',
  TRUE: 'true',
  FALSE: 'false'
};

export const GTM_DATA = {
  TRACKEVENT: 'trackEvent',
  LINK_CLICK: 'link click',
  CASHOUT_MESSAGING: 'cash out messaging',
};