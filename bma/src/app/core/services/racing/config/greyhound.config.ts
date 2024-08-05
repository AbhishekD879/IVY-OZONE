import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';

export const greyhoundConfig: IInitialSportConfig = {
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
      resultedMarketName: '|Win or Each Way|,|Win Only|,|Win or Eachway - Legends|',
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
      },
    },
    eventMethods: {
      today: 'todayEventsByClasses',
      tomorrow: 'todayEventsByClasses',
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
    INT: 'sb.flagINT',
    UK: 'sb.flagUK',
    VR: 'sb.flagVR',
    US: 'sb.flagUS',
    ZA: 'sb.flagZA',
    AE: 'sb.flagAE',
    CL: 'sb.flagCL',
    IN: 'sb.flagIN',
    AU: 'sb.flagAU',
    FR: 'sb.flagFR',
    ALL: 'sb.flagALL',
    ENHRCS: 'sb.flagENHRCS'
  },
  isRunnerNumber: true,
  tabs: [
    { id: 'tab-today', label: 'sb.tabsNameToday', url: '/greyhound-racing/today' },
    { id: 'tab-tomorrow', label: 'sb.tabsNameTomorrow', url: '/greyhound-racing/tomorrow' },
    { id: 'tab-future', label: 'sb.tabsNameFuture', url: '/greyhound-racing/future' }
  ],
  MARKETS_NAME_SORT_ORDER: ['Win or Each Way', 'Win Only', 'Place Only',
    'To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish',
    'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
};
