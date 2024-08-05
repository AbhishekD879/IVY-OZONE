const filters = ['by-meeting', 'by-time'];
const resultFilters = ['by-latest-results', 'by-meetings'];

export const TOTE_CONFIG = {
  moduleName: 'tote',
  POOLS_BET_STORAGE_NAME: 'TOTE_BETSLIP_POOLS',
  filters,
  filtersName: ['byMeeting', 'byTime'],
  resultFilters,
  resultFiltersName: ['byLatestResults', 'byMeetings'],
  order: {
    // Meetings order
    BY_MEETINGS_ORDER: ['typeDisplayOrder', 'name'],
    // Sort list by time
    BY_TIME_ORDER: ['localTime'],
    EVENTS_ORDER: ['localTime', 'typeName']
  },
  DEFAULT_POOL_TYPE: 'WN',
  // order will be extended, currently we supported only those types
  POOLS_TYPE_ORDER: ['WN', 'PL', 'SH', 'EX', 'TR'],
  TOTE_BANNER_TARGET_URI: 'tote',
  TOTE_INFO_BANNER_TARGET_URI: 'tote-information',
  DEFAULT_TOTE_SPORT: 'horseracing',
  currecySymbols: {
    USD: '$',
    GBP: '£',
    EUR: '€',
    HKD: 'HK$',
    SGD: 'SGD$'
  },
  poolsReqConfig: {
    poolProvider: 'P,E,A,H,V'
  },
  RESULT_REQUEST: {
    // should be used unique category ID after OB fix (OB has different ids for tote on each env), temp in env configs
    // categoryId: '161',
    date: 'results',
    isRacing: true,
    isResulted: true,
    priceHistory: true,
    racingFormEvent: true,
    racingFormOutcome: true,
    resultedMarketName: 'Win',
    resultedPriceTypeCodeToDisplay: 'LP',
    resultedOutcomeResultCodeNotEquals: 'V',
    resultedOutcomesExcludeUnnamedFavourites: true,
    siteChannels: 'M'
  },
  eventsReqConfig: {
    marketIds: [],
    siteChannels: 'M',
    timeRange: 'today'
  },
  eventReqConfig: {
    marketIds: [],
    eventIdEquals: undefined,
    racingFormOutcome: true,
    racingFormEvent: true
  },
  tabs: [
    {
      id: 'tab-horseracing',
      label: 'tt.tabsNameHorseRacing',
      url: `/tote/horseracing/${filters[0]}`,
      title: 'horse racing',
      originalTitle: 'horseracing'
    }, {
      id: 'tab-results',
      label: 'tt.tabsNameResults',
      url: `/tote/results/${resultFilters[0]}`,
      title: 'results',
      originalTitle: 'results'
    }
  ],
  RECORDS_LIMIT_BY_TIME: 10,
  LIVE_STREAM_CONFIG: [
    {
      type: 'iGameMedia',
      typeFlagCodes: 'GVA',
      drilldownTagNames: 'EVFLAG_GVM'
    }
  ],
  SUPPORTED_LIVE_STREAMS: ['iGameMedia', 'ATR'],
  TOTE_GENERAL_BET_ERROR_KEY: {
    bet: 'BET_GEN_ERR',
    service: 'SERVICE_GEN_ERR'
  },
  TOTE_EVENT_RELATED_ERRORS: {
    eventSuspended: 'This event is suspended',
    marketSuspended: 'This market is suspended',
    eventStarted: 'Event has started'
  }
};
