import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';

export const horseracingConfig: IInitialSportConfig = {
  config: {
    name: 'horseracing',
    categoryType: 'racing',
    path: 'horse-racing',
    sportModule: 'horseracing',
    request: {
      categoryId: '21',
      isRacing: true,
      typeFlagCodes: 'UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR',
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
      groupByFlagCodesSortOrder: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      breadcrumbsNavMenuFlags: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      date: null,
      priceHistory: true,
      externalKeysEvent: true,
      modules: {
        dailyRacing: {
          classIds: [],
          typeNames: ['Enhanced Multiples', 'Mobile Exclusive', 'Price Bomb', 'Winning Distances'],
          collapsedSections: 'Winning Distances'
        }
      }
    },
    tabs: {
      featured: {
        eventDrilldownTagNamesNotContains: 'EVFLAG_AP',
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP',
        marketTemplateMarketNameIntersects: '|Win or Each Way|,|Win Only|',
        limitOutcomesCount: 1,
        limitMarketCount: 1
      },
      today: {
        eventDrilldownTagNamesNotContains: 'EVFLAG_AP',
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
      },
      tomorrow: {
        eventDrilldownTagNamesNotContains: 'EVFLAG_AP',
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
      },
      future: {
        eventDrilldownTagNamesContains: 'EVFLAG_AP',
        eventDrilldownTagNamesIntersects: 'EVFLAG_FT,EVFLAG_IT,EVFLAG_NH',
        limitOutcomesCount: 1,
        limitMarketCount: 1,
        typeFlagCodes: ''
      },
      specials: {
        hidden: true,
        isNotStarted: true,
        typeFlagCodes: 'SP',
        isNotResulted: true,
        externalKeysEvent: false,
        excludeEventsClassIds: ''
      }
    },
    eventMethods: {
      featured: 'todayEventsByClasses',
      yourcall: 'getYourCallSpecials',
      antepost: 'getAntepostEvents',
      today: 'todayEventsByClasses',
      tomorrow: 'todayEventsByClasses',
      future: 'todayEventsByClasses',
      results: 'results',
      past: 'results',
      specials: 'todayEventsByClasses',
      ms: 'getFeatured'
    }
  },
  filters: {
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
    ENHRCS: 'sb.flagENHRCS'
  },
  isRunnerNumber: false,
  tabs: [
    { id: 'tab-featured', label: 'sb.tabsNameFeatured', url: '/horse-racing/featured' },
    { id: 'tab-future', label: 'sb.tabsNameAntepost', url: '/horse-racing/future' },
    { id: 'tab-specials', label: 'sb.tabsNameSpecials', url: '/horse-racing/specials' }
  ],
  MARKETS_NAME_SORT_ORDER: ['Win or Each Way', 'Win Only', 'Place Only',
    'To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish',
    'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places'],
  GROUPED_MARKETS_NAME: ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish',
    'Top 3 Finish', 'Top 4 Finish', 'Top 2', 'Top 3', 'Top 4', 'To Finish 2nd', 'To Finish 3rd', 'Insurance 2 Places',
    'Insurance 3 Places', 'Insurance 4 Places', 'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4'],
  RACE_MARKET_ORDER: ['customOrder', 'displayOrder', 'name'],
  PRESIM_STOP_TRACK_INTERVAL: 300000,
  MARKET_FLEX_TABS: 4
};
