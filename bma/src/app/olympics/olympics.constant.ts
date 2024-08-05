import { ISportConfig } from '@app/core/services/cms/models';
import { tier2EventMethods } from '@app/sb/services/sportsConfig/event-methods.constant';

export const OUTRIGHT_CONFIG: ISportConfig = {
  config: {
    request: {
      isActive: true
    },
    tabs: {
      live: {},
      today: {
        outrightsSport: true,
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
      },
      tomorrow: {
        outrightsSport: true,
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
      },
      future: {
        outrightsSport: true,
        marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
      },
      specials: {
        marketDrilldownTagNamesContains: 'MKTFLAG_SP'
      }
    },
    eventMethods: tier2EventMethods
  }
};

export const SPORTS_CONFIG: ISportConfig = {
  config: {
    categoryType: 'gaming',
    tier: 2,
    request: {
      siteChannels: 'M'
    },
    tabs: {
      live: {},
      today: {
        isNotStarted: true
      },
      tomorrow: {},
      future: {},
      outrights: {}
    },
    eventMethods: tier2EventMethods
  },
  tabs: [
    {
      id: 'tab-live',
      label: 'sb.tabsNameInPlay',
      name: 'live'
    },
    {
      id: 'tab-matches',
      label: 'sb.tabsNameMatches',
      name: 'matches',
      subTabs: [
        {
          id: 'tab-today',
          label: 'sb.tabsNameToday',
          name: 'today',
          hidden: false
        }, {
          id: 'tab-tomorrow',
          label: 'sb.tabsNameTomorrow',
          name: 'tomorrow',
          hidden: false
        }, {
          id: 'tab-future',
          label: 'sb.tabsNameFuture',
          name: 'future',
          hidden: false
        }
      ]
    },
    {
      id: 'tab-outrights',
      label: 'sb.tabsNameOutrights',
      name: 'outrights'
    },
    {
      id: 'tab-specials',
      label: 'sb.tabsNameSpecials',
      name: 'specials'
    }
  ]
};

export const PROPS_CONFIG: string[] = ['isOutrightSport', 'typeIds', 'dispSortName',
  'primaryMarkets', 'viewByFilters', 'oddsCardHeaderType', 'isMultiTemplateSport'];

export const SPECIALS_FILTERS: string[] = ['startTime', 'endTime', 'siteChannels', 'suspendAtTime',
  'isNotStarted', 'marketDrilldownTagNamesContains'];

export const OUTRIGHTS_FILTERS: string[] = ['startTime', 'endTime', 'siteChannels', 'eventSortCode',
  'suspendAtTime', 'isNotStarted', 'marketDrilldownTagNamesNotContains'];

export const EVENTS_FILTERS: string[] = ['categoryId', 'siteChannels', 'typeFlagCodes', 'startTime',
  'marketDrilldownTagNamesContains', 'endTime', 'dispSortName', 'dispSortNameIncludeOnly',
  'marketTemplateMarketNameIntersects', 'marketDrilldownTagNamesNotContains', 'eventSortCode',
  'isNotStarted', 'isStarted', 'marketName', 'suspendAtTime', 'excludeEventsClassIds',
  'templateMarketNameOnlyIntersects'];
