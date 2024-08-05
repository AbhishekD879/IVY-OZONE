import { OlympicsService } from '@sb/services/olympics/olympics.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { SPORTS_CONFIG } from '@app/olympics/olympics.constant';

describe('OlympicsService', () => {
  let service;

  const timeService = {},
    templateService = {},
    cacheEventsService = {},
    simpleFiltersService = {},
    routingHelperService = {
      formEdpUrl: (event) => {
        return ''
      }
    },
    coreToolsService = new CoreToolsService(),
    siteServerRequestHelperService = {},
    loadByPortionsService = {},
    buildUtilityService = {},
    liveStreamService = {},
    gamingService = {},
    cmsService = {},
    sportsConfigHelperService = {
      getSportConfigName: jasmine.createSpy('getSportConfigName').and.returnValue('football')
    };

  const sportCMSConfig = {
    dispSortName: ['MR'],
    categoryId: '16',
    isMultiTemplateSport: false,
    oddsCardHeaderType: 'homeDrawAwayType',
    targetUri: 'football',
    primaryMarkets: '|Match Betting|',
    viewByFilters: ['byCompetitions', 'byTime'],
    typeIds: ['3650', '442', '435'],
    sport: 'football',
    imageTitle: 'football',
    id: '4235235',
    tabs: {
      'tab-live': {
        tablabel: '',
        visible: true
      },
      'tab-matches': {
        tablabel: 'Matches Tab',
        visible: true
      },
      'tab-outrights': {
        tablabel: '',
        visible: true
      },
      'tab-specials': {
        tablabel: '',
        visible: false
      }
    }
  } as any;

  const sportConfig = {
    config: {
      categoryType: 'gaming',
      defaultTab: 'football',
      tier: 2,
      eventMethods: {
        today: 'todayEventsByTypesIds',
        tomorrow: 'todayEventsByTypesIds',
        future: 'todayEventsByClasses',
        upcoming: 'todayEventsByTypesIds',
        antepost: 'todayEventsByTypesIds',
        coupons: 'coupons',
        outrights: 'outrights',
        live: 'blocker',
        results: 'results',
        specials: 'specials',
        allEvents: 'todayEventsByClasses',
        matchesTab: 'todayEventsByClasses'
      },
      extension: 'olympics',
      name: 'football',
      path: 'football',
      request: {
        categoryId: '16',
        siteChannels: 'M',
        typeIds: ['3650', '442', '435']
      },
      tabs: {
        live: {},
        today: {
          dispSortName: ['MR'],
          dispSortNameIncludeOnly: ['MR'],
          isNotStarted: true,
          marketTemplateMarketNameIntersects: '|Match Betting|',
          marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
        },
        tomorrow: {
          dispSortName: ['MR'],
          dispSortNameIncludeOnly: ['MR'],
          marketTemplateMarketNameIntersects: '|Match Betting|',
          marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
        },
        future: {
          dispSortName: ['MR'],
          dispSortNameIncludeOnly: ['MR'],
          marketTemplateMarketNameIntersects: '|Match Betting|',
          marketDrilldownTagNamesNotContains: 'MKTFLAG_SP'
        },
        outrights: {
          isActive: true
        },
        specials: {
          marketDrilldownTagNamesContains: 'MKTFLAG_SP'
        }
      },
      title: 'football'
    },
    tabs: [
      {
        url: '/olympics/football/live',
        hidden: false,
        id: 'tab-live',
        name: 'live',
        label: 'In-Play'
      },
      {
        hidden: false,
        id: 'tab-matches',
        label: 'Matches Tab',
        name: 'matches',
        url: '/olympics/football/matches/today',
        subTabs: [
          {
            hidden: false,
            id: 'tab-today',
            label: 'sb.tabsNameToday',
            name: 'today',
            url: 'football/matches/today'
          }, {
            hidden: false,
            id: 'tab-tomorrow',
            label: 'sb.tabsNameTomorrow',
            name: 'tomorrow',
            url: 'football/matches/tomorrow'
          }, {
            hidden: false,
            id: 'tab-future',
            label: 'sb.tabsNameFuture',
            name: 'future',
            url: 'football/matches/future'
          }
        ]
      },
      {
        hidden: false,
        id: 'tab-outrights',
        label: 'Outrights',
        name: 'outrights',
        url: '/olympics/football/outrights'
      },
      {
        hidden: true,
        id: 'tab-specials',
        label: 'Specials',
        name: 'specials',
        url: '/olympics/football/specials'
      }
    ]
  };

  beforeEach(() => {
    service = new OlympicsService(
      timeService as any,
      templateService as any,
      cacheEventsService as any,
      simpleFiltersService as any,
      coreToolsService as any,
      siteServerRequestHelperService as any,
      loadByPortionsService as any,
      buildUtilityService as any,
      liveStreamService as any,
      gamingService as any,
      cmsService as any,
      sportsConfigHelperService as any,
      routingHelperService as any
    );
  });

  describe('#generatePreMatchSportConfig', () => {
    it('should generate Sport Config', () => {
      service.sportsConfigTemplate = SPORTS_CONFIG;
      const result = service.generatePreMatchSportConfig(sportCMSConfig);
      expect(result as any).toEqual(sportConfig);
    });
  });
  it('should  call getCollectionsTabs', () => {
    const marketsByCollection = [
      { name: 'c', markets: [{ name: 'a' }] }, { name: 'a', markets: [{ name: 'a' }] },
      { name: 'a', markets: [{ name: 'a' }] }, { name: 'd', markets: [{ name: 'a' }] },
      { name: 'b', markets: [{ name: 'a' }] }
    ];
    service.getCollectionsTabs(marketsByCollection,{});
    expect(service).toBeTruthy();
  });
});
