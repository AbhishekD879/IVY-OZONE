import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';
import {
  CompetitionsFutureSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { Subscription, of } from 'rxjs';

describe('#CompetitionsFutureSportTabComponent', () => {
  let component: CompetitionsFutureSportTabComponent;

  let pubSubService;
  let sportTabsService;
  let routingHelperService;
  let activatedRoute;
  let deviceService;
  let cmsService;
  let marketSortService;
  let competitionFiltersService;

  const events = [{ id: '1' }, {}, {}, {}, {}] as any;
  const limitedEvents = [{ id: '1' }, {}, {}] as any;

  const eventsBySections = [{
    typeId: 1,
    isExpanded: false,
    events: _.clone(events)
  },
  {
    typeId: 2,
    isExpanded: false,
    events: _.clone(events)
  },
  {
    typeId: 3,
    isExpanded: false,
    events: _.clone(events)
  },
  {
    typeId: 4,
    isExpanded: false,
    events: _.clone(events)
  }] as any;

  const limitedEventsBySections = [{
    typeId: 1,
    isExpanded: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 2,
    isExpanded: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 3,
    isExpanded: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 4,
    isExpanded: false,
    events: _.clone(limitedEvents)
  }] as any;

  const dacvtEventsBySections = [{
    typeId: 1,
    isExpanded: false,
    deactivated: true,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 2,
    isExpanded: false,
    deactivated: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 3,
    isExpanded: false,
    deactivated: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 4,
    isExpanded: false,
    deactivated: false,
    events: _.clone(limitedEvents)
  },
  {
    typeId: 5,
    isExpanded: false,
    deactivated: false,
    events: _.clone(limitedEvents)
  }] as any;


  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, methods, callback) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    sportTabsService = {
      deleteEvent: jasmine.createSpy('deleteEvent'),
      eventsBySections: jasmine.createSpy('eventsBySections').and.returnValue(eventsBySections)
    };
    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy('formCompetitionUrl')
    };
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get')
        }
      }
    };
    deviceService = {
      isDesktop: false
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        SportCompetitionsTab: {
          eventsLimit: 4
        }
      })),
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(of(Boolean))
    };
    marketSortService = {
      setMarketFilterForMultipleSections: jasmine.createSpy()
    };
    competitionFiltersService = {
      formTimeFilters: jasmine.createSpy('formTimeFilters').and.returnValue([]),
      filterEvents: jasmine.createSpy('filterEvents').and.returnValue([]),
      filterEventsByHiddenMarkets: jasmine.createSpy('filterEventsByHiddenMarkets').and.returnValue([]),
    };

    component = new CompetitionsFutureSportTabComponent(
      sportTabsService,
      routingHelperService,
      pubSubService,
      activatedRoute,
      deviceService,
      cmsService,
      marketSortService,
      competitionFiltersService
    );

    component.sport = {
      config: {
        name: 'football',
        request: {
          categoryId: '16'
        },
        tier: 1,
      },
      sportConfig: { tabs: [] },
      subscribeLPForUpdates: jasmine.createSpy('subscribeLPForUpdates'),
      unSubscribeLPForUpdates: jasmine.createSpy('unSubscribeLPForUpdates'),
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection'),
      getByTab: jasmine.createSpy('getByTab')
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit if tier 2 sport', fakeAsync(() => {
      component['updateLoadingState'].emit = jasmine.createSpy('updateLoadingState.emit');
      component['prepareEvents'] = jasmine.createSpy('updateLoadingState.emit').and.returnValue(limitedEvents);
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve(events));
      component.ngOnInit();
      tick(200);
      expect(component.isResponseError).toEqual(false);
      expect(component.displayFilters).toBeTrue();
      expect(component.sport.getByTab).toHaveBeenCalledWith('antepost');
      expect(component.sport.getByTab).toHaveBeenCalledWith('outrights');
      expect(component.sport.subscribeLPForUpdates).toHaveBeenCalledWith(limitedEvents);
      expect(sportTabsService.eventsBySections).toHaveBeenCalled();
      expect(sportTabsService.deleteEvent).toHaveBeenCalled();
      expect(component['prepareEvents']).toHaveBeenCalled();
    }));

    it('#ngOnInit if tier 2 sport (getByTab should return empty array)', fakeAsync(() => {
      component['updateLoadingState'].emit = jasmine.createSpy('updateLoadingState.emit');
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve([]));
      component.ngOnInit();
      tick(200);
      expect(component.isResponseError).toEqual(false);
      expect(component.displayFilters).toBeFalse();
      expect(component.sport.getByTab).toHaveBeenCalledWith('antepost');
      expect(component.sport.getByTab).toHaveBeenCalledWith('outrights');
      expect(component.sport.subscribeLPForUpdates).toHaveBeenCalledWith([]);
      expect(component.eventsBySections).toEqual([]);
      expect(component.eventsBySectionsCopy).toEqual([]);
      expect(sportTabsService.eventsBySections).not.toHaveBeenCalled();
      expect(sportTabsService.deleteEvent).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component['componentName'],
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
    }));

    it('#ngOnInit if tier 2 sport (getByTab should return error)', fakeAsync(() => {
      component['updateLoadingState'].emit = jasmine.createSpy('updateLoadingState.emit');
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.reject('error'));
      component.ngOnInit();
      tick(200);
      expect(component.isResponseError).toEqual(true);
      expect(component.sport.getByTab).toHaveBeenCalledWith('antepost');
      expect(component.sport.subscribeLPForUpdates).not.toHaveBeenCalled();
      expect(sportTabsService.eventsBySections).not.toHaveBeenCalled();
      expect(sportTabsService.deleteEvent).not.toHaveBeenCalled();
    }));

    it('should not prepare events for desktop', fakeAsync(() => {
      component['updateLoadingState'].emit = jasmine.createSpy('updateLoadingState.emit');
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve([]));
      component['prepareEvents'] = jasmine.createSpy();
      deviceService.isDesktop = true;
      component.ngOnInit();
      expect(component['prepareEvents']).not.toHaveBeenCalled();
    }));

    it('should not set eventsLimit', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      (component.sport.getByTab as any).and.returnValue(of([]));
      component.ngOnInit();
      expect(component['eventsLimit']).toBe(3);
    });
    it('should prepare events with matches if CMS Configured', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve(events));
      cmsService.getMarketSwitcherFlagValue.and.returnValue(of(true));
      component.ngOnInit();
      expect(component.isLoaded).toEqual(false);
    });
    it('should prepare events with matches if CMS not Configured', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve(events));
      cmsService.getMarketSwitcherFlagValue.and.returnValue(of(false));
      component.ngOnInit();
      expect(component.isLoaded).toEqual(false);
    });

    it('should get competitions filter and sport filters availability', () => {
      component.sportTabs = [];
      cmsService.getSystemConfig.and.returnValue(of({}));
      (component.sport.getByTab as any).and.returnValue(of([]));

      component.ngOnInit();

      expect(component.competitionFilters).toEqual([]);
      expect(competitionFiltersService.formTimeFilters).toHaveBeenCalledWith('competitions', []);
    });

    describe('should get Sport Event Filters availability', () => {
      it('when it is set', () => {
        cmsService.getSystemConfig.and.returnValue(of({ FeatureToggle: { SportEventFilters: true } }));
        (component.sport.getByTab as any).and.returnValue(of([]));

        component.ngOnInit();

        expect(component.isSportEventFiltersEnabled).toBeTruthy();
      });

      it('when it is not set', () => {
        cmsService.getSystemConfig.and.returnValue(of({ FeatureToggle: { SportEventFilters: false } }));
        (component.sport.getByTab as any).and.returnValue(of([]));

        component.ngOnInit();

        expect(component.isSportEventFiltersEnabled).toBeFalsy();
      });

      afterEach(() => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
      });
    });
  });

  it('#ngOnDestroy', () => {
    component['loadEventsSubscription'] = new Subscription();
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CompetitionsFutureSportTabComponent');
    expect(component.sport.unSubscribeLPForUpdates).toHaveBeenCalled();
    expect(component['loadEventsSubscription'].closed).toBeTruthy();
  });

  it('#ngOnDestroy', () => {
    component['loadEventsSubscription'] = undefined;
    component.ngOnDestroy();
    expect(component['loadEventsSubscription']).not.toBeDefined();
  });

  describe('#goToCompetition', () => {
    it('should build competition URL and redirect', () => {
      routingHelperService.formCompetitionUrl.and.returnValue('some/url');
      const result = component.goToCompetition({
        typeName: 'typeName',
        clasName: 'clasName'
      } as any);
      expect(routingHelperService.formCompetitionUrl).toHaveBeenCalled();
      expect(result).toEqual('some/url');
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
  });

  describe('#updateState', () => {
    it('should upodate section expanded state', () => {
      const section = {
        isExpanded: false
      } as any;
      component.updateState(true, section);
      expect(section.isExpanded).toEqual(true);
    });
  });

  describe('#trackByTypeId', () => {
    it('should update section expanded state', () => {
      const result = component.trackByTypeId(1, {
        isExpanded: true,
        typeId: '17'
      } as any);
      expect(result).toEqual('17');
    });
  });

  describe('#prepareAccordions', () => {
    it('should prepare accordions', () => {
      expect(component['prepareAccordions'](limitedEventsBySections)).toEqual([{
        typeId: 1,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 2,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 3,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 4,
        isExpanded: false,
        events: [{ id: '1' }, {}, {}]
      }] as any);
    });
    it('should prepare accordions when deactivated is true', () => {
      expect(component['prepareAccordions'](dacvtEventsBySections)).toEqual([{
        typeId: 1,
        deactivated: true,
        isExpanded: false,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 2,
        deactivated: false,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 3,
        deactivated: false,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 4,
        deactivated: false,
        isExpanded: true,
        events: [{ id: '1' }, {}, {}]
      },
      {
        typeId: 5,
        deactivated: false,
        isExpanded: false,
        events: [{ id: '1' }, {}, {}]
      }] as any);
    });
  });

  it('#prepareEvents', () => {
    component['getEventsFromSections'] = jasmine.createSpy();
    component['prepareEvents'](events);
    expect(component['getEventsFromSections']).toHaveBeenCalled();
    expect(component.sport.arrangeEventsBySection).toHaveBeenCalled();
  });

  it('#getEventsFromSections', () => {
    const res = component['getEventsFromSections']([{
      isExpanded: true,
      events: [{ id: '1' }]
    }, {
      isExpanded: true,
      events: [{ id: '2' }]
    }] as any);

    expect(res).toEqual([{ id: '1' }, { id: '2' }] as any);
  });

  describe('#limitSections', () => {
    it('when section.events.length > limitTo', () => {
      const res = component['limitSections'](eventsBySections);
      expect(res).toEqual(limitedEventsBySections);
      expect(component.limitedSections.length).toEqual(5);
    });
    it('when section.events.length < limitTo', () => {
      const res = component['limitSections'](limitedEventsBySections);
      expect(res).toEqual(limitedEventsBySections);
      expect(component.limitedSections.length).toEqual(0);
    });
  });

  describe('#filterEvents', () => {
    beforeEach(() => {
      component.eventsBySections = [{ categoryId: '1' }] as any;
    });
    it('filter should be defined', () => {
      component.filterEvents({output: '', value: 'someFilter'});
      expect(component['activeMarketFilter']).toBe('someFilter');
    });

    it('filter should not be defined', () => {
      expect(component['activeMarketFilter']).not.toBeDefined();
    });

    it('when filters are the same', () => {
      component['activeMarketFilter'] = 'someFilter';
      component.filterEvents({output: '', value: 'someFilter'});
      expect(marketSortService.setMarketFilterForMultipleSections).not.toHaveBeenCalled();
    });

    it('when filters are different', () => {
      component['activeMarketFilter'] = 'someFilter';
      component.filterEvents({output: '', value: 'someOtherFilter'});
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalled();
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
    });

    it('when filter not defined', () => {
      component.filterEvents({output: '', value: 'someOtherFilter'});
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalled();
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
    });

    it('when filters are available', () => {
      component.isSportEventFiltersEnabled = true;
      component.filterEvents({output: '', value: 'someOtherFilter'});
      expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalledTimes(2);
      expect(component['activeMarketFilter']).toBe('someOtherFilter');
      expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith(null, undefined, []);
      expect(competitionFiltersService.selectedMarket).toEqual('someOtherFilter');
    });
  });

  describe('handleCompetitionFilterOutput', () => {
    beforeEach(() => {
      component.timeFilter = null;
    });

    it('should not update filter if no output', () => {
      component.handleCompetitionFilterOutput({} as any);

      expect(component.timeFilter).toBeNull();
    });

    it('should update time filter', () => {
      const timeFilter = { id: 1, name: '1h', type: 'TIME', value: 1, active: true } as any;
      const expected = { ...timeFilter, active: false };

      component.timeFilter = timeFilter;

      component.handleCompetitionFilterOutput({ output: 'filterChange', value: { ...timeFilter, active: false } });

      expect(component.timeFilter).toEqual(expected);
      expect(component.eventsBySections).toEqual([]);
      expect(component.eventsBySectionsCopy).toEqual([]);
      expect(competitionFiltersService.filterEvents).toHaveBeenCalledWith(null, expected, []);
    });
  });

  describe('check for isMarketSwitcherConfigured', () => {
    it('should set isMarketSwitcherConfigured to true if cmsService getMarketSwitcherFlagValue return true', () => {
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = true;
          expect(component.isMarketSwitcherConfigured).toBe(true);
        });
    });
    it('should set isMarketSwitcherConfigured to false if cmsService getMarketSwitcherFlagValue return false', () => {
      cmsService.getMarketSwitcherFlagValue.subscribe = jasmine.createSpy('cmsService.getMarketSwitcherFlagValue')
        .and.callFake((flag) => {
          expect(cmsService.getMarketSwitcherFlagValue).toHaveBeenCalled();
          flag = false;
          expect(component.isMarketSwitcherConfigured).toBe(false);
        });
    });
  });

  describe('activeIndex', () => {
    it('should call activeIndex', () => {
      component.eventsBySections = [{deactivated: false}, {deactivated: true}] as any;
      const retVal = component.activeIndex(2);
      expect(retVal).toBe(1);
    });
  });
});
