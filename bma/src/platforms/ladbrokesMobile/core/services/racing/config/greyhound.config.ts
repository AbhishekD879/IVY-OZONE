import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';

export const ladbrokesGreyhoundConfig: IInitialSportConfig = {
  config: {
    categoryType: 'racing',
    name: 'greyhound',
    path: 'greyhound-racing',
    sportModule: 'greyhound',
    request: {
      categoryId: '19',
      isRacing: true,
      siteChannels: 'M',
      racingFormOutcome: true,
      racingFormEvent: true,
      isResulted: true,
      resultedMarketName: '|Win or Each Way|',
      resultedMarketPriceTypeCodesIntersects: 'SP',
      resultedPriceTypeCodeToDisplay: 'SP',
      resultedOutcomeResultCodeNotEquals: 'V', // Void player
      // means exclude resulted Outcomes with names - Unnamed Favorite & Unnamed 2nd Favorite
      resultedOutcomesExcludeUnnamedFavourites: true,
      resultedIncludeUndisplayed: true,
      breadcrumbsNavMenuFlags: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      groupByFlagCodesSortOrder: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      date: null,
      priceHistory: true,
      modules: {
        dailyRacing: {
          classIds: []
        }
      }
    },
    tabs: {
      specials: {
        hidden: true,
        isNotStarted: true,
        typeFlagCodes: 'SP',
        isNotResulted: true,
        limitOutcomesCount: 1,
        limitMarketCount: 1,
        excludeEventsClassIds: '',
        externalKeysEvent: false
      },
      today: {
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP',
        limitOutcomesCount: 1,
        limitMarketCount: 1
      },
      tomorrow: {
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP',
        limitOutcomesCount: 1,
        limitMarketCount: 1
      },
      future: {
        limitOutcomesCount: 1,
        limitMarketCount: 1
      }
    },
    eventMethods: {
      today: 'todayEventsByClasses',
      tomorrow: 'todayEventsByClasses',
      specials: 'todayEventsByClasses',
      future: 'todayEventsByClasses',
      todayAndTomorrow: 'todayEventsByClasses',
      results: 'results',
      past: 'results',
      ms: 'getFeatured'
    }
  },
  filters: {
    RACING_FILTERS: [ 'by-meeting', 'by-time' ],
    RESULTS_FILTERS: [ 'by-latest-results', 'by-meetings' ]
  },
  order: {
    BY_LEAGUE_ORDER: ['classDisplayOrder', 'typeDisplayOrder'],
    // Sort list inside league section
    BY_LEAGUE_EVENTS_ORDER: ['startTime', 'displayOrder', 'name'],
    // Sort list by time
    BY_TIME_ORDER: ['startTime', 'classDisplayOrder', 'typeDisplayOrder',
      'displayOrder', 'name'],
    EVENTS_ORDER: ['startTime', 'name']
  },
  sectionTitle: {
    INT: 'sb.flagINTLong',
    UK: 'sb.flagUkLong',
    VR: 'sb.flagVRaces',
    US: 'sb.flagUSLong',
    ZA: 'sb.flagZALong',
    AE: 'sb.flagAELong',
    CL: 'sb.flagCLLong',
    IN: 'sb.flagINLong',
    AU: 'sb.flagAULong',
    FR: 'sb.flagFRLong',
    ALL: 'sb.flagALL',
    ENHRCS: 'sb.flagENHRCS'
  },
  isRunnerNumber: true,
  tabs: [
    { id: 'tab-races', label: 'sb.tabsNameNext', url: '/greyhound-racing/races/next' },
    { id: 'tab-today', label: 'sb.tabsNameToday', url: '/greyhound-racing/today' },
    { id: 'tab-tomorrow', label: 'sb.tabsNameTomorrow', url: '/greyhound-racing/tomorrow' },
    { id: 'tab-future', label: 'sb.tabsNameFuture', url: '/greyhound-racing/future' },
    { id: 'tab-specials', label: 'sb.tabsNameSpecials', url: '/greyhound-racing/specials' }
  ],
  MARKETS_NAME_SORT_ORDER: ['Win or Each Way', 'Win Only', 'Place Only',
    'To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish',
    'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places',
    'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
    'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4']
};


