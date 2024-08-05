import {
  CompetitionsMatchesTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';
import environment from '@environment/oxygenEnvConfig';
import { of as observableOf } from 'rxjs';

describe('#CompetitionsMatchesTabComponent', () => {
  let component: CompetitionsMatchesTabComponent;
  let marketSortService;
  let gamingService;
  let filterService;
  let cmsService;
  let competitionFiltersService;
  let pubSubService;

  let eventsByCategory;
  const orderedEvents = [1, 2, 3];

  beforeEach(() => {
    marketSortService = {
      setMarketFilterForOneSection: jasmine.createSpy('setMarketFilterForOneSection')
    };
    gamingService = {
      sportConfig: {
        config: {
          name: 'cricket',
          request: { marketTemplateMarketNameIntersects: '' },
          tier: 1
        }
      }
    };
    filterService = {
      orderBy: jasmine.createSpy('orderBy').and.returnValue(orderedEvents)
    };

    cmsService = {
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(Boolean))
    };

    eventsByCategory = {
      events: [{
        markets: [{
          name: '',
          templateMarketName: 'Match Betting Head/Head'
        }]
      }]
    } as any;
    competitionFiltersService = {
      filterEventsByHiddenMarkets: jasmine.createSpy('filterEventsByHiddenMarkets').and.returnValue([])
    };
    pubSubService  = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb('2123')),
      unsubscribe: jasmine.createSpy('unsubscribe'),
       API: {DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE' }
    };

    component = new CompetitionsMatchesTabComponent(marketSortService, filterService, cmsService, competitionFiltersService, pubSubService);
    component.sport = gamingService as any;
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      component.checkSelectedMarkets = jasmine.createSpy('checkSelectedMarkets');
    });

    it('should call checkSelectedMarkets and filteredMatches', () => {
      component.eventsByCategory = {
        groupedByDate: {
          1: {
            deactivated: false,
            events: [10, 20, 30]
          }
        }
      } as any;
      component.filteredMatches = [];

      const changes = {
        eventsByCategory: {
          currentValue: 'test'
        },
        isLoaded: {
          currentValue: true
        }
      };
      component.isMarketSwitcherConfigured = true;
      component.ngOnChanges(changes as any);
      expect(component.isLoadedFilter).toEqual(false);
      expect(component.checkSelectedMarkets).toHaveBeenCalledWith(changes.eventsByCategory.currentValue as any);
      expect(component.filteredMatches).toEqual([{
        deactivated: false,
        events: orderedEvents
      }] as any);
    });

    it('should call filteredQuickSwitchEvents', () => {
      component.filteredMatches = [];
      const filteredQuickSwitchEvents = [1, 2, 3];
      const changes = {
        filteredQuickSwitchEvents: {
          currentValue: filteredQuickSwitchEvents
        }
      };
      component.ngOnChanges(changes as any);
      expect(component.filteredQuickSwitchEvents).toEqual(changes.filteredQuickSwitchEvents.currentValue as any);
      expect(component.filteredMatches).toEqual(component.filteredQuickSwitchEvents as any);
    });

    it('should not call checkSelectedMarkets ', () => {
      const changes = {};

      component.ngOnChanges(changes as any);

      expect(component.checkSelectedMarkets).not.toHaveBeenCalled();
    });
  });
  describe('validateMatches', () => {
    it('should set showNoEvents to true when at least one event has no markets', () => {
      const Match1 = { events: [{ markets: [] }] }as any;
      const Match2 = { events: [{ markets: [{}] }] }as any;
      component.filteredMatches = [Match1, Match2];
      component.validateMatches();
      expect(component.showNoEvents).toBe(true);
    });

    it('should not set showNoEvents to true when all events have markets', () => {
      const Match1 = { events: [{ markets: [{}] }] } as any;
      const Match2 = { events: [{ markets: [{}] }] } as any;
      component.filteredMatches = [Match1, Match2];
      component.validateMatches();
      expect(component.showNoEvents).toBe(false);
    });

    it('should not set showNoEvents to true when no matches are present', () => {
      component.filteredMatches = [];
      component.validateMatches();
      expect(component.showNoEvents).toBe(false);
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from marketSwitcherConfig',  () => {
      component['marketSwitcherConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['marketSwitcherConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
    it('should unsubscribe from pubsub', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['componentId'])
    });
  });

  describe('selectedMarket', () => {
    // it('should return selected market name if it previously defined defined', () => {
    //   // component.defaultSelectedMarket = 'market name';

    //   const result = component.selectedMarket({} as any);

    //   expect(result).toEqual('market name');
    // });

    it('should return `Match Result`', () => {
      component.sportId = environment.CATEGORIES_DATA.footballId;
      const result = component.selectedMarket(eventsByCategory);

      expect(result).toEqual('Match Result');
    });

    it('should return `Default`', () => {
      component.sportId = environment.CATEGORIES_DATA.footballId;
      eventsByCategory = {
        events: [{
          markets: [{
            name: '',
            templateMarketName: 'Match Result'
          }]
        }],
        defaultValue: 'Default'
      };
      const result = component.selectedMarket(eventsByCategory);

      expect(result).toEqual('Default');
    });

    it('should return default selected market (no default selected, not football)', () => {
      // component.defaultSelectedMarket = null;
      component.sportId = null;
      expect(component.selectedMarket({} as any)).toEqual(undefined);
    });

    it('should return `Money Line` when sport is baseball', () => {
      component.sportId = '5';
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('Money Line');
    });
    it('should return `Default` when sport is baseball', () => {
      component.sportId = '5';
      eventsByCategory = {
        events: [{ markets: [{ name: '', templateMarketName: 'Match Result' }] }],
        defaultValue: 'Default'
      };
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('Default');
    });
    it('should return `Fight Betting` when sport is boxing', () => {
      component.sportId = '9';
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('Fight Betting');
    });
    it('should return `Default` when sport is boxing', () => {
      component.sportId = '9';
      eventsByCategory = {
        events: [{ markets: [{ name: '', templateMarketName: 'Fight Betting' }] }],
        defaultValue: 'Default'
      };
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('Default');
    });
    it('should return `2 Ball Betting` when sport is golf', () => {
      component.sportId = '18';
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('2 Ball Betting');
    });
    it('should return `Default` when sport is golf', () => {
      component.sportId = '18';
      eventsByCategory = {
        events: [{ markets: [{ name: '', templateMarketName: '2 Ball Betting' }] }],
        defaultValue: 'Default'
      };
      const result = component.selectedMarket(eventsByCategory);
      expect(result).toEqual('Default');
    });
  });

  describe('filterEvents', () => {
    it('should filter Events', () => {
      (component.eventsByCategory as any) = {};
      (component.eventsByCategoryCopy as any) = {};

      component.filterEvents({output: '', value: 'MR'});

      expect(marketSortService.setMarketFilterForOneSection).toHaveBeenCalledTimes(2);
      expect(marketSortService.setMarketFilterForOneSection).toHaveBeenCalledWith({}, 'MR');
      expect(competitionFiltersService.filterEventsByHiddenMarkets).toHaveBeenCalledWith([]);
      expect(competitionFiltersService.selectedMarket).toEqual('MR');
      expect(component.filteredMatches).toEqual([]);
    });

    it('should filter events when no copy provided', () => {
      (component.eventsByCategory as any) = {};
      (component.eventsByCategoryCopy as any) = undefined;

      component.filterEvents({output: '', value: 'MR'});

      expect(marketSortService.setMarketFilterForOneSection).toHaveBeenCalled();
      expect(marketSortService.setMarketFilterForOneSection).toHaveBeenCalledWith({}, 'MR');
      expect(competitionFiltersService.filterEventsByHiddenMarkets).not.toHaveBeenCalledWith([]);
      expect(competitionFiltersService.selectedMarket).toBeUndefined();
      expect(component.filteredMatches).toEqual([]);
    });
  });

  describe('checkSelectedMarkets', () => {
    it('should return true', () => {
      spyOn<any>(component, 'selectedMarket').and.callFake(() => 'Match Betting Head/Head');
      component.sportId = environment.CATEGORIES_DATA.footballId;
      eventsByCategory.events[0].markets[0].name = 'Match Betting';

      const result = component.checkSelectedMarkets(eventsByCategory);

      expect(result).toBeTruthy();
    });

    it('should return false', () => {
      spyOn<any>(component, 'selectedMarket').and.callFake(() => 'Match Betting');
      component.sportId = environment.CATEGORIES_DATA.footballId;
      eventsByCategory.events[0].markets[0].name = 'Match Result';

      const result = component.checkSelectedMarkets(eventsByCategory);

      expect(result).toBeFalsy();
    });
  });

  describe('trackByTypeId', () => {
    it('should trackBy TypeId', () => {
      const result = component.trackByTypeId({
        typeId: 'typeId'
      } as any);

      expect(result).toEqual('typeId');
    });
  });

  describe('getFilteredMatches', () => {
    it('should get Filtered Matches', () => {
      component.eventsByCategory = {
        groupedByDate: {
          0: {
            deactivated: true
          },
          1: {
            deactivated: false,
            events: [10, 20, 30]
          }
        }
      } as any;

      const result = component.getFilteredMatches();

      expect(result).toEqual([component.eventsByCategory.groupedByDate[1]] as any);
      expect(filterService.orderBy).toHaveBeenCalledWith([10, 20, 30], ['startTime', 'displayOrder', 'name']);
      expect(filterService.orderBy).toHaveBeenCalledTimes(1);
      expect(component.eventsByCategory.groupedByDate['1'].events).toEqual(orderedEvents);
    });

    it('should get filteredQuickSwitchEvents', () => {
      component.eventQuickSwitch = true;
      component.getFilteredMatches();
      expect(component.filteredQuickSwitchEvents).toBeDefined();
    });

    it('should return empty array if no eventsByCategory', () => {
      component.eventsByCategory = undefined;

      expect(component.getFilteredMatches()).toEqual([]);
    });

    it('should return empty array if no groupedByDate', () => {
      component.eventsByCategory = {
        groupedByDate: undefined
      } as any;

      expect(component.getFilteredMatches()).toEqual([]);
    });
  });

  describe('#reinitHeader', () => {
    it('should assign changed Market', () => {
      const changedMarket = {
        id: '1',
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
      };

      component.reinitHeader(changedMarket as any);

      expect(component.undisplayedMarket).toEqual(changedMarket as any);
    });
  });

  describe('#ngOninit', () => {
    it('check for Tier1', () => {
      component.sportId = environment.CATEGORIES_DATA.footballId;
      component.eventQuickSwitch = true;
      component.ngOnInit();
      expect(component.isMarketSelectorAvailable).toBe(true);
    });
    it('should subscribe to DELETE_EVENT_FROM_CACHE event and call validateMatches on callback', () => {
      component.eventQuickSwitch = true;
      spyOn(component, 'validateMatches');
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(component['componentId'], 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
      expect(component.validateMatches).toHaveBeenCalled();
    });
  });

  describe('check for isMarketSwitcherConfigured', () => {
    it('should set isMarketSwitcherConfigured to true when cmsService getMarketSwitcherFlagValue return true', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(true);
    });
    it('should set isMarketSwitcherConfigured to false when cmsService getMarketSwitcherFlagValue return false', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(false));
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(false);
    });
    it('set isMarketSwitcherLoaded false with competitionPage true and cmsService true', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.competitionPage = true;
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(true);
      expect(component.isMarketSwitcherLoaded).toBe(false);
    });
    it('set isMarketSwitcherLoaded false with competitionPage true and cmsService true and isLoaded false', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.competitionPage = true;
      component.isLoaded = false;
      environment.CURRENT_PLATFORM = 'mobile';
      component.ngOnInit();
      expect(component.isLoaded).toBe(false);
    });
    it('set isMarketSwitcherLoaded false with competitionPage true and cmsService true and isLoaded true', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.competitionPage = true;
      component.isLoaded = true;
      environment.CURRENT_PLATFORM = 'desktop';
      component.eventsByCategoryCopy = [{id:1}] as any;
      component.ngOnInit();
      expect(component.isLoaded).toBe(false);
    });
    it('set isMarketSwitcherLoaded false with competitionPage true and cmsService true and isLoaded true', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.competitionPage = true;
      component.isLoaded = true;
      environment.CURRENT_PLATFORM = 'desktop';
      component.eventsByCategoryCopy = undefined;
      component.ngOnInit();
      expect(component.isLoaded).toBe(true);
    });
    
    it('set isMarketSwitcherLoaded true with competitionPage true and cmsService false', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(false));
      component.competitionPage = true;
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(false);
      expect(component.isMarketSwitcherLoaded).toBe(true);
    });
    it('set isMarketSwitcherLoaded true with competitionPage false and cmsService true', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(true));
      component.competitionPage = false;
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(true);
      expect(component.isMarketSwitcherLoaded).toBe(true);
    });
    it('set isMarketSwitcherLoaded true with competitionPage false and cmsService false', () => {
      cmsService.getMarketSwitcherFlagValue.and.returnValue(observableOf(false));
      component.competitionPage = false;
      component.ngOnInit();
      expect(component.isMarketSwitcherConfigured).toBe(false);
      expect(component.isMarketSwitcherLoaded).toBe(true);
    });
  });
});
