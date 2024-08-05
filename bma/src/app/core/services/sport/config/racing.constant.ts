export const RACING_CONFIG = {
  FLAGS_MAP: {
    11: ['F', '2F'],
    12: ['F', '2JF', '2JF'],
    21: ['JF', 'JF', '2F'],
    22: ['JF', 'JF', '2JF', '2JF'],
    31: ['', '', '', '2F'],
    32: ['', '', '', '2JF', '2JF'],
    13: ['F', '', '', ''],
    23: ['JF', 'JF', '', '', ''],
    33: ['', '', '', '', '', '']
  },
  MAIN_RACING_MARKETS: {
    'Win or Each Way': {path: 'win-or-each-way'},
    'Win Only': {path: 'win-only'}
  },
  WO_MARKET: {
    PATH: 'betting-without',
    CUSTOM_ORDER: 3,
    SUB_MARKETS: ['Betting Without']
  },
  TO_FINISH_MARKET: {
    PATH: 'to-finish',
    SUB_MARKETS: ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'To Finish 2nd', 'To Finish 3rd'],
    CUSTOM_ORDER: 4,
    HEADERS: ['2nd', '3rd', '4th']
  },
  TOP_FINISH_MARKET: {
    PATH: 'top-finish',
    SUB_MARKETS: ['Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish'],
    CUSTOM_ORDER: 5,
    HEADERS: ['Top 2', 'Top 3', 'Top 4']
  },
  INSURANCE_MARKETS: {
    PATH: 'insurance',
    SUB_MARKETS: ['Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places'],
    CUSTOM_ORDER: 6,
    HEADERS: ['2nd', '3rd', '4th']
  },
  OTHER_MARKETS: {
    PATH: 'more-markets'
  },
  YC_WIDGET_FILTER: 'Featured',
  COUNTRY_FLAGS: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
  ANTEPOST_SWITCHER_KEYS: ['EVFLAG_FT', 'EVFLAG_NH', 'EVFLAG_IT'],
  US_IGNORE_TIME: {
    START_TIME: 6,
    END_TIME: 18
  },
  FEATURED_TABS: ['featured', 'today', 'tomorrow'],
  FEATURED_MS: 'ms',
  GTM_ARGS: {
    HORSE_RACING_CATEGORY: 'horse racing',
    RACE_CARD_ACTION: 'race card',
    SORTBY_PRICE_RACECARD_LABEL: 'sort by - '
  }
};
