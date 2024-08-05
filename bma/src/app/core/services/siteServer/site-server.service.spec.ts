import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';

describe('SiteServerService', () => {
  let service;
  let buildUtility;
  let simpleFilters;
  let ssUtility;
  let eventsByClasses;
  let loadByPortions;
  let ssRequestHelper;
  let time;
  let filter;
  let eventFilters;
  let slicePipe;

  beforeEach(() => {
    time = {
      getSuspendAtTime: jasmine.createSpy().and.returnValue(new Date()),
      createTimeRange: jasmine.createSpy().and.returnValue({startDate: '12/02/1982', endDate: '13/03/2090'})
    };

    filter = {
      objectPromise: jasmine.createSpy().and.callFake(returnObject => returnObject)
    };

    eventFilters = {
      applyFilters: jasmine.createSpy('applyFilters').and.returnValue(events => events)
    };

    slicePipe = {
      transform: jasmine.createSpy().and.returnValue([{ event: {id: 1}}])
    };

    ssRequestHelper = {
      getEvent: jasmine.createSpy().and.returnValue(Promise.resolve([{id: 1}, {id: 2}])),
      getEventsList: jasmine.createSpy().and.returnValue(Promise.resolve([{id: 5, event: {intId: 50}}, {id: 6, event: {intId: 60}}])),
      getNextEventsByType: jasmine.createSpy(),
      getNextNEventToOutcomeForClass: jasmine.createSpy('getNextNEventToOutcomeForClass'),
      getEventToMarketForClass: jasmine.createSpy('getEventToMarketForClass'),
      getEventByIds: jasmine.createSpy('getEventByIds').and.returnValue(Promise.resolve({ event: { id: 1 } })),
      getCommentsByEventsIds: jasmine.createSpy('getCommentsByEventsIds').and.returnValue(Promise.resolve([])),
      getEventsByEvents: jasmine.createSpy('getEventsByEvents').and.returnValue(Promise.resolve({ event: { id: 1 } })),
      getEventsByClasses: jasmine.createSpy('getEventsByClasses'),
      getResultedEventByEvents: jasmine.createSpy('getResultedEventByEvents'),
      getEventsByOutcomes: jasmine.createSpy('getEventsByOutcomes'),
      getOutrightsByTypeIds: jasmine.createSpy(),
      getEventsByType: jasmine.createSpy(),
      getEventToMarketForEvent: jasmine.createSpy().and.returnValue(Promise.resolve({ event: { id: 1 } })),
      getMarketsCountByClasses: jasmine.createSpy(),
      getMarketsCountByEventsIds: jasmine.createSpy(),
      getCouponsList: jasmine.createSpy().and.returnValue(Promise.resolve('getCouponsList')),
      getCouponsByIds: jasmine.createSpy().and.returnValue(Promise.resolve([{coupon: {children: [{childrenId: 1, event: {id: 5}}]}}])),
      getJackpotPools: jasmine.createSpy(),
      getEventsByMarkets: jasmine.createSpy().and.returnValue(Promise.resolve({SSResponse: {children: [
                                                                                              {childrenId: 12},
                                                                                              {childrenId: 22},
                                                                                              {childrenId: 32}]}})),
      getCategories: jasmine.createSpy(),
      getSportToCollection: jasmine.createSpy().and.returnValue(Promise.resolve('getSportToCollection')),
      getClassesByCategory: jasmine.createSpy().and.returnValue(Promise.resolve('getClassesByCategory')),
      getClassToSubTypeForClass: jasmine.createSpy().and.returnValue(Promise.resolve('getClassToSubTypeForClass')),
      getClassToSubTypeForType: jasmine.createSpy(),
      getEventToLinkedOutcomeForEvent: jasmine.createSpy().and.returnValue(Promise.resolve('getEventToLinkedOutcomeForEvent')),
      getClasses: jasmine.createSpy().and.returnValue(Promise.resolve({SSResponse: {children: [
                                                                                      {childrenId: 1},
                                                                                      {childrenId: 2},
                                                                                      {childrenId: 3}]}}))
    };

    loadByPortions = {
      get: jasmine.createSpy('get').and.callFake(cb => {
        cb && cb({});
        return Promise.resolve([{event: {children: []}}]);
      })
    };

    ssUtility = {
      queryService: jasmine.createSpy('queryService').and.returnValue(Promise.resolve([])),
      stripResponse: jasmine.createSpy('stripResponse').and.callFake(e => e),
      filterEventsWithPrices: jasmine.createSpy().and.returnValue([{eventId: 1}]),
    };

    simpleFilters = {
      simpleFiltersBank: {
        nextEventsByIds: ['filter'],
        nextEventsByType: ['nextEventsByType'],
        eventsByTypeId: ['eventsByTypeId'],
        eventsByCategory: ['eventsByCategory'],
        eventsByOutcomeIds: [{}],
        eventsList: [0, 2, 4],
        liveEventsByEvents: {
          push: jasmine.createSpy()
        },
        resultsByClasses: ['resultsByClasses'],
        resultedEvents: ['resultedEvents'],
        inPlayEventsByIds: ['inPlayEventsByIds'],
        couponEventsByCouponId: ['couponEventsByCouponId', 'dispSortName'],
        eventsByMarkets: ['eventsByMarkets'],
        typesByClasses: ['typesByClasses'],
        inPlayEventsWithOutOutcomes: ['eventStatusCode'],
      },
      getFilterParams: jasmine.createSpy('getFilterParams').and.returnValue({filteredData: true}),
      genFilters: jasmine.createSpy('genFilters').and.callFake(e => e)
    };

    buildUtility = {
      buildEvents: jasmine.createSpy(),
      buildEventsIds: jasmine.createSpy(),
      buildEventsWithScorecasts: jasmine.createSpy(),
      buildEventsWithRacingForm: jasmine.createSpy('buildEventsWithRacingForm').and.callFake(events => events),
      buildEventWithRacingFormOutcomes: jasmine.createSpy('buildEventWithRacingFormOutcomes').and.callFake(events => events),
      buildEventsWithOutMarketCounts: jasmine.createSpy('buildEventsWithOutMarketCounts').and.returnValue({}),
      buildCouponEventsWithMarketCounts: jasmine.createSpy('buildEventsWithOutMarketCounts').and.returnValue({}),
      buildEventsWithMarketCounts: jasmine.createSpy('buildEventsWithMarketCounts').and.returnValue([]),
      buildEventsWithScoresAndClock: jasmine.createSpy('buildEventsWithMarketCounts').and.returnValue([]),
      buildEventsWithExternalKeys: jasmine.createSpy('buildEventsWithExternalKeys').and.returnValue([{}]),
      buildEventWithScores: jasmine.createSpy('buildEventWithScores').and.callFake(events => events),
      eventBuilder: jasmine.createSpy().and.callFake(events => events),
      buildInPlayEventsWithMarketsCount: jasmine.createSpy().and.returnValue(Promise.resolve([{}, {}, {}])),
    };

    eventsByClasses = {
      getClasses: jasmine.createSpy('getClasses').and.returnValue(Promise.resolve(['1', '2'])),
      getClassesByParams: jasmine.createSpy('getClassesByParams').and.returnValue(Promise.resolve(['1', '2']))
    };

    service = new SiteServerService(
      ssRequestHelper as any,
      simpleFilters as any,
      buildUtility as any,
      loadByPortions as any,
      ssUtility as any,
      time as any,
      filter as any,
      eventFilters as any,
      slicePipe as any,
      eventsByClasses as any
    );
  });

  describe('getEventByEventId', () => {
    it('should call ssRequestHelper.getEvent, ssUtility.stripResponse and buildUtility.eventBuilder', fakeAsync(() => {
      service.getEventByEventId(123);
      tick();

      expect(ssRequestHelper.getEvent).toHaveBeenCalledWith({eventId: 123});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(buildUtility.eventBuilder).toHaveBeenCalled();
    }));

    it('should call ssRequestHelper.getEvent, ssUtility.stripResponse but not buildUtility.eventBuilder', fakeAsync(() => {
      ssUtility.stripResponse = jasmine.createSpy('stripResponse').and.returnValue([]);

      service.getEventByEventId(123);
      tick();

      expect(ssRequestHelper.getEvent).toHaveBeenCalledWith({eventId: 123});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(buildUtility.eventBuilder).not.toHaveBeenCalled();
    }));
  });

  describe('getEventsByClasses', () => {
    it('should call loadEventsWithOutMarketCounts and buildUtility.buildEventsWithOutMarketCounts', fakeAsync(() => {
      const params = {
        classIds: [{}]
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.returnValue(Promise.resolve([{id: 1}, {id: 2}]));

      service.getEventsByClasses(params);
      tick();

      expect(service.loadEventsWithOutMarketCounts).toHaveBeenCalled();
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));

    it('should not call loadEventsWithOutMarketCounts', () => {
      const params = {
        classIds: []
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.returnValue(Promise.resolve([{id: 1}, {id: 2}]));

      service.getEventsByClasses(params);
      expect(service.loadEventsWithOutMarketCounts).not.toHaveBeenCalled();
    });
  });

  describe('getEventsByClass', () => {
    it('should call loadEventsWithOutMarketCounts and stripResponse', fakeAsync(() => {
      const params = { classIds: '227'};
      ssRequestHelper.getEventsByClasses.and.returnValue(of([]));

      service.getEventsByClass(params).subscribe();
      tick();

      expect(ssRequestHelper.getEventsByClasses).toHaveBeenCalled();
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([]);
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([]);
    }));
  });

  describe('getRawEventsByClasses', () => {
    it('should call loadEventsByClasses, buildUtility.buildEventsWithExternalKeys and buildUtility.eventBuilder', fakeAsync(() => {
      const params = {
        classIds: [{}]
      };
      spyOn(service, 'loadEventsByClasses').and.returnValue(Promise.resolve([{id: 1}, {id: 2}]));

      service.getRawEventsByClasses(params);
      tick();

      expect(service.loadEventsByClasses).toHaveBeenCalled();
      expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(buildUtility.eventBuilder).toHaveBeenCalledTimes(1);
    }));

    it('should not call loadEventsByClasses', () => {
      const params = {
        classIds: []
      };
      spyOn(service, 'loadEventsByClasses').and.returnValue(Promise.resolve([{id: 1}, {id: 2}]));

      service.getRawEventsByClasses(params);

      expect(service.loadEventsByClasses).not.toHaveBeenCalled();
    });
  });

  describe('getEventsList', () => {
    it('should call ssRequestHelper.getEventsList, simpleFilters.genFilters and ssUtility.stripResponse', fakeAsync(() => {
      const params = [{id: 1}, {id: 2}, {id: 3}, {id: 4}, {id: 5}];
      const filters = {
              0: {id: 1},
              2: {id: 3},
              4: {id: 5}
            };

      service.getEventsList(params);
      tick();

      expect(ssRequestHelper.getEventsList).toHaveBeenCalled();
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(filters);
      expect(ssUtility.stripResponse).toHaveBeenCalled();
    }));
  });

  describe('getLiveEventsByEvents', () => {
    it('should call liveEventsByEvents and set limitOutcomesCount field', () => {
      const params = {
        limitOutcomesCount: 0,
        eventsIds: []
      };
      expect(params.limitOutcomesCount).toEqual(0);

      service.getLiveEventsByEvents(params, true);

      expect(simpleFilters.simpleFiltersBank.liveEventsByEvents.push).toHaveBeenCalledWith('limitOutcomesCount');
      expect(params.limitOutcomesCount).toEqual(1);
    });

    it('should not call liveEventsByEvents and not set limitOutcomesCount field and shouldn"t call loadEventsWithOutMarketCounts', () => {
      const params = {
        limitOutcomesCount: 0,
        eventsIds: []
      };
      spyOn(service, 'loadEventsWithOutMarketCounts');
      expect(params.limitOutcomesCount).toEqual(0);

      service.getLiveEventsByEvents(params, false);

      expect(service.loadEventsWithOutMarketCounts).not.toHaveBeenCalled();
      expect(simpleFilters.simpleFiltersBank.liveEventsByEvents.push).not.toHaveBeenCalled();
      expect(params.limitOutcomesCount).toEqual(0);
    });

    it('should call loadEventsWithOutMarketCounts, getEventsByEvents and then buildEventsWithOutMarketCounts', fakeAsync(() => {
      const params = {
        limitOutcomesCount: 0,
        eventsIds: [
          123,
          456
        ]
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.callFake(method => {
        method('loaded events');
        return Promise.resolve([{id: 1}, {id: 2}]);
      });

      service.getLiveEventsByEvents(params, false);
      tick();

      expect(service.loadEventsWithOutMarketCounts).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByEvents).toHaveBeenCalledWith('loaded events');
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));
  });

  describe('getLiveOutrightEventsByEvents', () => {
    it('should not call loadEventsWithOutMarketCounts', () => {
      const params = {
        eventsIds: []
      };
      spyOn(service, 'loadEventsWithOutMarketCounts');

      service.getLiveOutrightEventsByEvents(params);

      expect(service.loadEventsWithOutMarketCounts).not.toHaveBeenCalled();
    });

    it('should call loadEventsWithOutMarketCounts, getEventByIds and then buildEventsWithOutMarketCounts', fakeAsync(() => {
      const params = {
        eventsIds: [
          123,
          456
        ]
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.callFake(method => {
        method('loaded events');
        return Promise.resolve([{id: 1}, {id: 2}]);
      });

      service.getLiveOutrightEventsByEvents(params);
      tick();

      expect(service.loadEventsWithOutMarketCounts).toHaveBeenCalled();
      expect(ssRequestHelper.getEventByIds).toHaveBeenCalledWith('loaded events');
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));
  });

  describe('getEventsByEventsIds', () => {
    it('should not call loadEventsWithOutMarketCounts', () => {
      const params = {
        marketsCount: 0,
        eventsIds: []
      };
      spyOn(service, 'loadEventsWithOutMarketCounts');

      service.getEventsByEventsIds(params);

      expect(service.loadEventsWithOutMarketCounts).not.toHaveBeenCalled();
    });

    it('should choose loader and builder w/o market counts and call it', fakeAsync(() => {
      const params = {
        marketsCount: 0,
        eventsIds: [
          123,
          456
        ]
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.callFake(method => {
        method('loaded events');
        return Promise.resolve([{id: 1}, {id: 2}]);
      });

      service.getEventsByEventsIds(params);
      tick();

      expect(service.loadEventsWithOutMarketCounts).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByEvents).toHaveBeenCalledWith('loaded events', undefined);
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));

    it('should choose loader and builder with market counts and call it', fakeAsync(() => {
      const params = {
        marketsCount: 1,
        eventsIds: [
          123,
          456
        ]
      };
      spyOn(service, 'loadEventsWithMarketCounts').and.callFake(method => {
        method('loaded events');
        return Promise.resolve([{id: 1}, {id: 2}]);
      });

      service.getEventsByEventsIds(params, undefined);
      tick();

      expect(service.loadEventsWithMarketCounts).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByEvents).toHaveBeenCalledWith('loaded events', undefined);
      expect(buildUtility.buildEventsWithMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));

    it('should choose loader and builder with ChildCount', fakeAsync(() => {
      const params = {
        marketsCount: false,
        childCount: true,
        eventsIds: [
          123,
          456
        ]
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.callFake(method => {
        method('loaded events');
        return Promise.resolve([{id: 1}, {id: 2}]);
      });

      service.getEventsByEventsIds(params);
      tick();

      expect(service.loadEventsWithOutMarketCounts).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByEvents).toHaveBeenCalledWith('loaded events', true);
      expect(buildUtility.buildEventsWithMarketCounts).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
    }));
  });

  describe('getNextEventsByType', () => {
    it('should create extendedParams object (concated typeId value) according ingoming params and call methods', fakeAsync(() => {
      const params = {
        siteServerEventsCount: 1,
        typeId: [
          123,
          456
        ],
        eventsCount: 5,
        eventsIds: []
      };
      const extendedParams = {
        id: 555,
        typeId: '123,456',
        count: 1
      };
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });
      simpleFilters.getFilterParams.and.returnValue({ id: 555 });

      service.getNextEventsByType(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['nextEventsByType']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getNextEventsByType).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledWith([]);
      expect(eventFilters.applyFilters).toHaveBeenCalledWith(['hasOutcomes']);
      expect(slicePipe.transform).toHaveBeenCalledWith([], 0, 5);
    }));

    it('should create extendedParams object (typeId as is) according ingoming params and call methods', fakeAsync(() => {
      const params = {
        siteServerEventsCount: 1,
        typeId: 777,
        eventsCount: 5,
        eventsIds: []
      };
      const extendedParams = {
        id: 555,
        typeId: 777,
        count: 1
      };
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });
      simpleFilters.getFilterParams.and.returnValue({ id: 555 });

      service.getNextEventsByType(params).then(() => {

      });
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['nextEventsByType']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getNextEventsByType).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledWith([]);
      expect(eventFilters.applyFilters).toHaveBeenCalledWith(['hasOutcomes']);
      expect(slicePipe.transform).toHaveBeenCalledWith([], 0, 5);
    }));
  });

  describe('#getEventsByTypeWithMarketCounts', () => {
    it('it should load events with by type with Market Counts', fakeAsync(() => {
      const params = {
        marketsCount: true,
        noEventSortCodes: 'TNMT,TR01,TR02,TR03,TR04,TR05',
        typeId: '442'
      };
      const filters = [
        'isNotStarted', 'noEventSortCodes', 'typeHasOpenEvent', 'marketsCount',
        'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects',
        'templateMarketNameOnlyIntersects', 'competitionTemplateMarketNameOnlyIntersects'
      ];
      service.simpleFiltersBank.eventsByTypeWithMarketCounts = filters;

      service.getEventsByTypeWithMarketCounts(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, filters);
    }));
  });

  describe('getEventsByTypeId', () => {
    it('should create extendedParams object (concated typeId value) according ingoming params and call methods', fakeAsync(() => {
      const params = {
        siteServerEventsCount: 1,
        typeId: [
          123,
          456
        ]
      };
      const extendedParams = {
        id: 555,
        typeId: '123,456',
        count: 1
      };
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });
      simpleFilters.getFilterParams.and.returnValue({ id: 555 });

      service.getEventsByTypeId(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['eventsByTypeId']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getOutrightsByTypeIds).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([]);
    }));

    it('should create extendedParams object (typeId as is) according ingoming params and call methods', fakeAsync(() => {
      const params = {
        siteServerEventsCount: 1,
        typeId: 777
      };
      const extendedParams = {
        id: 555,
        typeId: 777,
        count: 1
      };
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });
      simpleFilters.getFilterParams.and.returnValue({ id: 555 });

      service.getEventsByTypeId(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['eventsByTypeId']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getOutrightsByTypeIds).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([]);
    }));
  });

  describe('getEventsByType', () => {
    it('should call queryService and getEventsByType methods', () => {
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });

      service.getEventsByType(999);

      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), { typeId: 999 });
      expect(ssRequestHelper.getEventsByType).toHaveBeenCalledWith('test data');
    });
  });

  describe('getEventsByCategory', () => {
    it('should choose loader and builder w/o market counts and call it', fakeAsync(() => {
      const params = {
        marketsCount: 0,
        eventsIds: [
          123,
          456
        ],
        categoryId: 150,
        siteChannels: ['channelOne', 'channelTwo']
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.returnValue([{id: 1}, {id: 2}]);
      spyOn(service, 'filterGamingEvents');

      service.getEventsByCategory(params);
      tick();

      expect(eventsByClasses.getClasses).toHaveBeenCalledWith(150, ['channelOne', 'channelTwo']);
      expect(service.loadEventsWithOutMarketCounts)
        .toHaveBeenCalledWith(ssRequestHelper.getEventsByClasses, params, ['eventsByCategory'], 'classIds', ['1', '2']);
      expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledWith([{}]);
      expect(service.filterGamingEvents).toHaveBeenCalledWith(150, ssUtility.filterEventsWithPrices, {});
    }));

    it('should choose loader and builder with market counts and call it', fakeAsync(() => {
      const params = {
        marketsCount: 1,
        eventsIds: [
          123,
          456
        ],
        categoryId: '21',
        siteChannels: ['channelOne', 'channelTwo']
      };

      spyOn(service, 'loadEventsWithMarketCounts').and.returnValue([{id: 1}, {id: 2}]);
      spyOn(service, 'filterGamingEvents');

      service.getEventsByCategory(params);
      tick();

      expect(eventsByClasses.getClasses).toHaveBeenCalledWith('21', ['channelOne', 'channelTwo']);
      expect(service.loadEventsWithMarketCounts)
        .toHaveBeenCalledWith(ssRequestHelper.getEventsByClasses, params, ['eventsByCategory'], 'classIds', ['1', '2']);
      expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(buildUtility.buildEventsWithMarketCounts).toHaveBeenCalledWith([{}]);
      expect(service.filterGamingEvents).toHaveBeenCalledWith('21', ssUtility.filterEventsWithPrices, []);
    }));
  });

  describe('getEventsToMarketsByEvents', () => {
    it('should call loadByPortions, ssRequestHelper.getEventToMarketForEvent and buildUtility.buildEvents methods', fakeAsync(() => {

      service.getEventsToMarketsByEvents([111, 222]);
      tick();

      expect(service.loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {}, 'eventsIds', [111, 222]);
      expect(ssRequestHelper.getEventToMarketForEvent).toHaveBeenCalledWith({});
      expect(buildUtility.buildEvents).toHaveBeenCalledWith([{event: {children: []}}]);
    }));
  });

  describe('getResultsByClasses', () => {
    it('should use loader w/o market and doesn"t update params.date', fakeAsync(() => {
      const params = {
        marketsCount: 0,
        eventsIds: [
          123,
          456
        ],
        categoryId: 150,
        siteChannels: ['channelOne', 'channelTwo'],
        date: 'default',
        marketName: 'default',
        resultedMarketName: 'resultedMarketName',
        isRacing: false
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.returnValue([{id: 1}, {id: 2}]);
      spyOn(service, 'loadResultedEvents').and.returnValue('results');
      spyOn(service, 'filterGamingEvents');

      expect(params.date).toEqual('default');
      expect(params.marketName).toEqual('default');

      service.getResultsByClasses(params);
      tick();

      expect(params.date).toEqual('default');
      expect(params.marketName).toEqual('resultedMarketName');
      expect(eventsByClasses.getClasses).toHaveBeenCalledWith(150, ['channelOne', 'channelTwo']);
      expect(service.loadEventsWithOutMarketCounts)
        .toHaveBeenCalledWith(ssRequestHelper.getEventsByClasses, params, ['resultsByClasses'], 'classIds', ['1', '2']);
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(service.filterGamingEvents).toHaveBeenCalledWith(150, ssUtility.filterEventsWithPrices, 'results');
    }));

    it('should use loader w/o market and update params.date', fakeAsync(() => {
      const params = {
        marketsCount: 0,
        eventsIds: [
          123,
          456
        ],
        categoryId: 150,
        siteChannels: ['channelOne', 'channelTwo'],
        date: 'default',
        marketName: 'default',
        resultedMarketName: 'resultedMarketName',
        resultsDay: 'resultsDay',
        isRacing: true
      };
      spyOn(service, 'loadEventsWithOutMarketCounts').and.returnValue([{id: 1}, {id: 2}]);
      spyOn(service, 'loadResultedEvents').and.returnValue('results');
      spyOn(service, 'filterGamingEvents');

      expect(params.date).toEqual('default');
      expect(params.marketName).toEqual('default');

      service.getResultsByClasses(params);
      tick();

      expect(params.date).toEqual('resultsDay');
      expect(params.marketName).toEqual('resultedMarketName');
      expect(eventsByClasses.getClasses).toHaveBeenCalledWith(150, ['channelOne', 'channelTwo']);
      expect(service.loadEventsWithOutMarketCounts)
        .toHaveBeenCalledWith(ssRequestHelper.getEventsByClasses, params, ['resultsByClasses'], 'classIds', ['1', '2']);
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledWith([{id: 1}, {id: 2}]);
      expect(service.filterGamingEvents).toHaveBeenCalledWith(150, ssUtility.filterEventsWithPrices, 'results');
    }));
  });

  describe('getInPlayEventsByClassesOnlyStream', () => {
    it('should call loadInPlayEvents with extended params and other methods', fakeAsync(() => {
      const params = {
        categoryId: 150
      };
      const extendedParams = {
        categoryId: 150,
        startTime: '12/02/1982',
        endTime: '13/03/2090',
        eventDrilldownTagNamesContains: 'EVFLAG_BL',
        eventDrilldownTagNamesIntersects: 'EVFLAG_PVM,EVFLAG_IVM,EVFLAG_GVM'
      };
      spyOn(service, 'loadInPlayEvents').and.returnValue(Promise.resolve('test data'));
      spyOn(service, 'loadScoresAndClock');

      service.getInPlayEventsByClassesOnlyStream(params);
      tick();

      expect(time.createTimeRange).toHaveBeenCalledWith('today');
      expect(service.loadInPlayEvents).toHaveBeenCalledWith(extendedParams);
      expect(buildUtility.buildInPlayEventsWithMarketsCount).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(3);
    }));
  });

  describe('isRacing', () => {
    beforeEach(() => {
      service.categories = {
        racing: {
          greyhound: {
            id: '19'
          }
        }
      };
    });

    it('should return true', () => {
      const result = service.isRacing('19');

      expect(result).toBe(true);
    });

    it('should return false', () => {
      const result = service.isRacing('999');

      expect(result).toBe(false);
    });
  });

  describe('filterGamingEvents', () => {
    let filterFunction;
    let events;

    beforeEach(() => {
      filterFunction = jasmine.createSpy().and.returnValue('filtered events');
      events = [{id: 1}, {id: 2}];
      spyOn(service, 'isRacing');
    });

    it('should call filterFunction', () => {
      service.isRacing.and.returnValue(false);

      const result = service.filterGamingEvents('19', filterFunction, events);

      expect(service.isRacing).toHaveBeenCalledWith('19');
      expect(filterFunction).toHaveBeenCalledWith(events);
      expect(result).toEqual('filtered events');
    });

    it('should not call filterFunction in case racing', () => {
      service.isRacing.and.returnValue(true);

      const result = service.filterGamingEvents('20', filterFunction, events);

      expect(service.isRacing).toHaveBeenCalledWith('20');
      expect(filterFunction).not.toHaveBeenCalled();
      expect(result).toEqual(events);
    });

    it('should not call filterFunction in case tote category', () => {
      service.isRacing.and.returnValue(false);

      const result = service.filterGamingEvents('161', filterFunction, events);

      expect(service.isRacing).toHaveBeenCalledWith('161');
      expect(filterFunction).not.toHaveBeenCalled();
      expect(result).toEqual(events);
    });
  });

  describe('loadEventsWithMarketCounts', () => {
    let loadEventsService;
    let params;
    let filterArr;
    let ids;

    beforeEach(() => {
      loadEventsService = jasmine.createSpy();
      params = {
        siteServerEventsCount: 150
      };
      filterArr = ['dispSortName',
      'marketTemplateMarketNameIntersects',
      'outcomeSiteChannels',
      'includeUndisplayed',
      'existsMarketOutcomeOutcomeMeaningMajorCodeIn',
      'limitToMarketDisplayOrderIsLowest',
      'templateMarketNameOnlyIntersects',
      'thisShouldStay',
      'andThisShoulsStayAlso'];
      ids = [1, 2];
    });

    it('should choose and call getMarketsCountByClasses', () => {
      const idsPropName = 'classIds';

      service.loadEventsWithMarketCounts(loadEventsService, params, filterArr, idsPropName, ids);

      expect(ssRequestHelper.getMarketsCountByClasses).toHaveBeenCalledWith({});
      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['thisShouldStay', 'andThisShoulsStayAlso'], true);
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true, count: 150}, 'classIds', [ 1, 2 ]);
      expect(loadByPortions.get).toHaveBeenCalledTimes(2);
    });

    it('should choose and call getMarketsCountByEventsIds', () => {
      const idsPropName = 'notClassIds';

      service.loadEventsWithMarketCounts(loadEventsService, params, filterArr, idsPropName, ids);

      expect(ssRequestHelper.getMarketsCountByEventsIds).toHaveBeenCalledWith({});
      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['thisShouldStay', 'andThisShoulsStayAlso'], true);
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true, count: 150}, 'notClassIds', [ 1, 2 ]);
      expect(loadByPortions.get).toHaveBeenCalledTimes(2);
    });
  });

  describe('loadEventsWithOutMarketCounts', () => {
    it('should call getFilterParams and loadByPortions.get', () => {
      const loadEventsService = jasmine.createSpy();
      const params = {
        siteServerEventsCount: 150,
        childCount: true
      };
      const filterArr = ['dispSortName',
      'marketTemplateMarketNameIntersects'];
      const ids = [1, 2];
      const propName = 'classIds';

      service.loadEventsWithOutMarketCounts(loadEventsService, params, filterArr, propName, ids);

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, filterArr);
      expect(loadEventsService).toHaveBeenCalledWith({}, true);
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true}, 'classIds', [1, 2]);
    });
  });

  describe('loadResultedEvents', () => {
    it('should map ids and call getResultedPricesByOutcomeIdFromResultedEvents and addResultedPricesToEvents', fakeAsync(() => {
      const params = {
        categoryId: 150,
        resultedPriceTypeCodeToDisplay: 'UAH'
      };
      const events = [{id: 10}, {id: 20}];
      const resultedPricesByOutcomeId = jasmine.createSpy();
      spyOn(service, 'getResultedPricesByOutcomeIdFromResultedEvents').and.returnValue(Promise.resolve(resultedPricesByOutcomeId));
      spyOn(service, 'addResultedPricesToEvents');

      service.loadResultedEvents(params, events);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['resultedEvents']);
      expect(service.getResultedPricesByOutcomeIdFromResultedEvents).toHaveBeenCalledWith('UAH', 150, [{event: {children: []}}]);
      expect(service.addResultedPricesToEvents).toHaveBeenCalledWith(events, jasmine.any(Function));
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true}, 'eventsIds', [10, 20]);
      expect(ssRequestHelper.getResultedEventByEvents).toHaveBeenCalledWith({});
    }));
  });

  describe('loadInPlayEvents', () => {
    beforeEach(() => {
      spyOn(service, 'loadInPlayEventsByIds');
      spyOn(service, 'getEventsList');
    });

    it('should call loadInPlayEventsByIds with default arguments and don"t call getEventsList', fakeAsync(() => {
      const params = {
        eventsIds: [150, 250]
      };

      service.loadInPlayEvents(params);
      tick();

      expect(service.loadInPlayEventsByIds).toHaveBeenCalledWith(params, true, true, false);
      expect(service.getEventsList).not.toHaveBeenCalled();
      expect(buildUtility.buildEventsIds).not.toHaveBeenCalled();
      expect(service.loadInPlayEventsByIds).toHaveBeenCalledTimes(1);
    }));

    it('should call loadInPlayEventsByIds with passed arguments and call getEventsList', fakeAsync(() => {
      const params = {
        eventsIds: null
      };
      const extendedParams = {
        eventsIds: [100, 200, 300]
      };
      service.getEventsList.and.returnValue(Promise.resolve('event list'));
      buildUtility.buildEventsIds.and.returnValue([100, 200, 300]);

      service.loadInPlayEvents(params, false, false, true);
      tick();

      expect(service.loadInPlayEventsByIds).toHaveBeenCalledWith(extendedParams, false, false, true);
      expect(service.getEventsList).toHaveBeenCalledWith(params);
      expect(buildUtility.buildEventsIds).toHaveBeenCalledWith('event list');
      expect(service.loadInPlayEventsByIds).toHaveBeenCalledTimes(1);
    }));
  });

  describe('loadInPlayEventsByIds', () => {
    const liveNowRequestParamsUniqueParams = {
      isStarted: true
    };
    const liveLaterRequestParamsUniqueParams = {
      isNotStarted: true
    };
    const outrightSpecificLiveNowParamsUniqueParams = {
      eventSortCode: OUTRIGHTS_CONFIG.outrightSortCode,
      categoryCode: OUTRIGHTS_CONFIG.outrightsSports,
      isStarted: true,
      limitMarketCount: 1
    };
    const outrightLiveNowParamsUniqueParams = {
      eventSortCode: OUTRIGHTS_CONFIG.sportSortCode,
      limitMarketCount: 1,
      isStarted: true,
      limitOutcomesCount: 1
    };
    const outrightSpecificLiveLaterParamsUniqueParams = {
      eventSortCode: OUTRIGHTS_CONFIG.outrightSortCode,
      categoryCode: OUTRIGHTS_CONFIG.outrightsSports,
      isNotStarted: true,
      limitMarketCount: 1
    };
    const outrightLiveLaterParamsUniqueParams = {
      eventSortCode: OUTRIGHTS_CONFIG.sportSortCode,
      isNotStarted: true,
      limitMarketCount: 1,
      limitOutcomesCount: 1
    };

    beforeEach(() => {
      spyOn(service, 'getParams').and.callFake((params, commonParams, uniqueParams) => uniqueParams);
      spyOn(service, 'getLiveEventsByEvents').and.callFake((params, marketsLevelOnly) => params);
      spyOn(service, 'getLiveOutrightEventsByEvents').and.callFake((params) => params);
      spyOn(service, 'getCommentsByEvents').and.returnValue('some comments');
    });

    it('should return filled object and not call getMarketsCountByEventsIds and getCommentsByEvents', () => {
      const commonParams = {
        marketBetInRun: true
      };
      const params = {
        eventsIds: [150, 250]
      };
      const controlReturnObject = {
        nowEvents: liveNowRequestParamsUniqueParams,
        laterEvents: liveLaterRequestParamsUniqueParams,
        outrightSpecificNowEvents: outrightSpecificLiveNowParamsUniqueParams,
        outrightNowEvents: outrightLiveNowParamsUniqueParams,
        outrightSpecificLaterEvents: outrightSpecificLiveLaterParamsUniqueParams,
        outrightLaterEvents: outrightLiveLaterParamsUniqueParams
      };

      const result = service.loadInPlayEventsByIds(params, false, false, true);

      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveNowRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveLaterRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveLaterParamsUniqueParams);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveNowRequestParamsUniqueParams, true);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveLaterRequestParamsUniqueParams, true);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveLaterParamsUniqueParams);
      expect(simpleFilters.getFilterParams).not.toHaveBeenCalled();
      expect(service.getCommentsByEvents).not.toHaveBeenCalled();
      expect(filter.objectPromise).toHaveBeenCalledWith(controlReturnObject);
      expect(result).toEqual(controlReturnObject);
    });

    it('should return filled object and call getMarketsCountByEventsIds but not getCommentsByEvents', () => {
      const commonParams = {
        marketBetInRun: true
      };
      const params = {
        eventsIds: [150, 250]
      };
      const marketNowCountsRequestParams = {
        eventsIds: [150, 250],
        marketBetInRun: true,
        isStarted: true
      };
      const controlReturnObject = {
        nowEvents: liveNowRequestParamsUniqueParams,
        laterEvents: liveLaterRequestParamsUniqueParams,
        outrightSpecificNowEvents: outrightSpecificLiveNowParamsUniqueParams,
        outrightNowEvents: outrightLiveNowParamsUniqueParams,
        outrightSpecificLaterEvents: outrightSpecificLiveLaterParamsUniqueParams,
        outrightLaterEvents: outrightLiveLaterParamsUniqueParams,
        nowMarkets: jasmine.any(Promise),
        laterMarkets: jasmine.any(Promise)
      };

      const result = service.loadInPlayEventsByIds(params, true, false, true);

      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveNowRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveLaterRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveLaterParamsUniqueParams);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveNowRequestParamsUniqueParams, true);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveLaterRequestParamsUniqueParams, true);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveLaterParamsUniqueParams);
      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(marketNowCountsRequestParams, ['inPlayEventsByIds'], true);
      expect(ssRequestHelper.getMarketsCountByEventsIds).toHaveBeenCalledWith({});
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true}, 'eventsIds', [150, 250]);
      expect(service.getCommentsByEvents).not.toHaveBeenCalled();
      expect(filter.objectPromise).toHaveBeenCalledWith(controlReturnObject);
      expect(result).toEqual(controlReturnObject);
    });

    it('should return filled object and not call getMarketsCountByEventsIds but call getCommentsByEvents', () => {
      const commonParams = {
        marketBetInRun: true
      };
      const params = {
        eventsIds: [150, 250]
      };
      const controlReturnObject = {
        nowEvents: liveNowRequestParamsUniqueParams,
        laterEvents: liveLaterRequestParamsUniqueParams,
        outrightSpecificNowEvents: outrightSpecificLiveNowParamsUniqueParams,
        outrightNowEvents: outrightLiveNowParamsUniqueParams,
        outrightSpecificLaterEvents: outrightSpecificLiveLaterParamsUniqueParams,
        outrightLaterEvents: outrightLiveLaterParamsUniqueParams,
        comments: 'some comments'
      };

      const result = service.loadInPlayEventsByIds(params, false, true, true);

      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveNowRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, liveLaterRequestParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveNowParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getParams).toHaveBeenCalledWith(params, commonParams, outrightLiveLaterParamsUniqueParams);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveNowRequestParamsUniqueParams, true);
      expect(service.getLiveEventsByEvents).toHaveBeenCalledWith(liveLaterRequestParamsUniqueParams, true);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveNowParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightSpecificLiveLaterParamsUniqueParams);
      expect(service.getLiveOutrightEventsByEvents).toHaveBeenCalledWith(outrightLiveLaterParamsUniqueParams);
      expect(simpleFilters.getFilterParams).not.toHaveBeenCalled();
      expect(ssRequestHelper.getMarketsCountByEventsIds).not.toHaveBeenCalled();
      expect(loadByPortions.get).not.toHaveBeenCalled();
      expect(service.getCommentsByEvents).toHaveBeenCalledWith([150, 250]);
      expect(filter.objectPromise).toHaveBeenCalledWith(controlReturnObject);
      expect(result).toEqual(controlReturnObject);
    });
  });

  describe('getEnhancedMultiplesEvents', () => {
    it('should return promise call getEventsList, buildEventsIds and extend params', fakeAsync(() => {
      const params = {
        categoryId: 150
      };
      const extendedParams = {
        categoryId: 150,
        eventsIds: [150, 250]
      };
      spyOn(service, 'getEventsList').and.returnValue(Promise.resolve([{}, {}]));
      spyOn(service, 'getEventsByEventsIds');
      buildUtility.buildEventsIds.and.returnValue(Promise.resolve([150, 250]));

      const result = service.getEnhancedMultiplesEvents(params);
      tick();

      expect(service.getEventsList).toHaveBeenCalledWith(params);
      expect(buildUtility.buildEventsIds).toHaveBeenCalledWith([{}, {}]);
      expect(service.getEventsByEventsIds).toHaveBeenCalledWith(extendedParams);
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getResultedPricesByOutcomeIdFromResultedEvents', () => {
    let resultedEventsArray;
    let controlResultedOutcomesByIds;

    beforeEach(() => {
      resultedEventsArray = [{resultedEvent: {
          children: [{resultedMarket: {
              children: [{ resultedOutcome: {
                  id: 555,
                  resultCode: 777,
                  children: [{resultedPrice: {
                    priceTypeCode: '1',
                    priceNum: 5,
                    priceDen: 6,
                    priceDec: 7
                  }}]
                }
              }]
            }
          }]
        }
      }];
      controlResultedOutcomesByIds = {
        555: {
          outcomeResultCode: 777,
          priceNum: 5,
          priceDen: 6,
          priceDec: '7.00'
        }
      };
    });

    it('should return promise and make resultedOutcomesByIds object w/o the position field', fakeAsync(() => {
      const result = service.getResultedPricesByOutcomeIdFromResultedEvents('1', '200', resultedEventsArray).then((data) => {
        expect(data).toEqual(controlResultedOutcomesByIds);
      });
      tick();

      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('should return promise and make resultedOutcomesByIds object with the position field', fakeAsync(() => {
      resultedEventsArray[0]
        .resultedEvent.children[0]
        .resultedMarket.children[0]
        .resultedOutcome.position = 333;

      delete resultedEventsArray[0]
              .resultedEvent.children[0]
              .resultedMarket.children[0]
              .resultedOutcome.children[0]
              .resultedPrice
              .priceDec;

      controlResultedOutcomesByIds[555].priceDec = 'NaN';
      controlResultedOutcomesByIds[555].outcomePosition = 333;


      const result = service.getResultedPricesByOutcomeIdFromResultedEvents('1', '161', resultedEventsArray).then((data) => {
        expect(data).toEqual(controlResultedOutcomesByIds);
      });
      tick();

      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('it should load events with by type with Market Counts and childCount', fakeAsync(() => {
      const params = {
        marketsCount: true,
        childCount: true,
        noEventSortCodes: 'TNMT,TR01,TR02,TR03,TR04,TR05',
        typeId: '442'
      };
      const filters = [
        'isNotStarted', 'noEventSortCodes', 'typeHasOpenEvent', 'marketsCount',
        'dispSortName', 'dispSortNameIncludeOnly', 'marketTemplateMarketNameIntersects',
        'templateMarketNameOnlyIntersects', 'competitionTemplateMarketNameOnlyIntersects'
      ];
      service.simpleFiltersBank.eventsByTypeWithMarketCounts = filters;

      service.getEventsByTypeWithMarketCounts(params).then(() => {
        expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, filters);
      });
    }));
  });

  describe('addResultedPricesToEvents', () => {
    it('should make and return events array', () => {
      const events = [
        {id: 1, markets: [{outcomes: [{id: 21}]}]},
        {id: 2, markets: [{outcomes: [{id: 22}]}]},
      ];
      const resultedPricesByOutcomeId = {21: {resulted: true}};
      const controlEventsArray = [
        {id: 1, markets: [{outcomes: [{id: 21, results: {resulted: true}}]}]},
        {id: 2, markets: [{outcomes: []}]},
      ];

      const result = service.addResultedPricesToEvents(events, resultedPricesByOutcomeId);

      expect(result).toEqual(controlEventsArray);
    });
  });

  describe('loadEventsByClasses', () => {
    it('should return promise, call passed service, getFilterParams and loadByPortions.get with extended params', () => {
      const serviceToPass = jasmine.createSpy();
      const params = {
        siteServerEventsCount: 5
      };
      const filterToPass = ['filter'];
      const classIds = [5, 7];


      const result = service.loadEventsByClasses(serviceToPass, params, filterToPass, classIds);

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, filterToPass);
      expect(serviceToPass).toHaveBeenCalledWith({});
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {filteredData: true, count: 5}, 'classIds', [5, 7]);
      expect(result).toEqual(jasmine.any(Promise));
    });
  });

  describe('getCouponsList', () => {
    it('should return promise, call getCouponsList and then stripResponse', fakeAsync(() => {
      const params = {
        categoryId: 150
      };

      const result = service.getCouponsList(params);
      tick();

      expect(ssRequestHelper.getCouponsList).toHaveBeenCalledWith({simpleFilters: params});
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(params);
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getCouponsList');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getCouponEventsByCouponId', () => {
    let params;

    beforeEach(() => {
      params = {
        categoryId: 150,
        couponId: 55,
        childCount: 1
      };
    });

    it('should return promise, call, getCouponsByIds, stripResponse, buildEvents', fakeAsync(() => {
      delete params.childCount;

      const result = service.getCouponEventsByCouponId(params);
      tick();

      expect(ssRequestHelper.getCouponsByIds).toHaveBeenCalledWith({couponsIds: 55, simpleFilters: params});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([{coupon: {children: [{childrenId: 1, event: {id: 5}}]}}]);
      expect(buildUtility.buildEvents).toHaveBeenCalledWith([{childrenId: 1, event: {id: 5}}]);
      expect(buildUtility.buildCouponEventsWithMarketCounts).not.toHaveBeenCalled();
      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('should return promise, call, getCouponsByIds, stripResponse and not call buildEvents', fakeAsync(() => {
      const result = service.getCouponEventsByCouponId(params);
      tick();

      expect(ssRequestHelper.getCouponsByIds).toHaveBeenCalledWith({couponsIds: 55, simpleFilters: params});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([{coupon: {children: [{childrenId: 1, event: {id: 5}}]}}]);
      expect(buildUtility.buildEvents).not.toHaveBeenCalled();
      expect(buildUtility.buildCouponEventsWithMarketCounts).toHaveBeenCalled();
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getJackpotList', () => {
    it('should return promise, call getJackpotPools and then stripResponse', fakeAsync(() => {
      ssRequestHelper.getJackpotPools.and.returnValue(Promise.resolve('getJackpotPools'));

      const result = service.getJackpotList();
      tick();

      expect(ssRequestHelper.getJackpotPools).toHaveBeenCalled();
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getJackpotPools');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getEventsByMarkets', () => {
    let params;
    let extendedParams;

    beforeEach(() => {
      params = {
        marketIds: [20, 30],
        racingFormOutcome: true
      };
      extendedParams = {
        id: 555,
        marketIds: [20, 30]
      };
      ssUtility.queryService.and.callFake(method => {
        method('test data');
        return Promise.resolve([]);
      });
      simpleFilters.getFilterParams.and.returnValue({ id: 555 });
    });

    it('should create extendedParams object and call methods but not buildEvents', fakeAsync(() => {
      const result = service.getEventsByMarkets(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['eventsByMarkets']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledWith([{}]);
      expect(buildUtility.buildEvents).not.toHaveBeenCalled();
      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('should create extendedParams object and call methods but not buildEventsWithRacingForm', fakeAsync(() => {
      params.racingFormOutcome = false;

      const result = service.getEventsByMarkets(params);
      tick();

      expect(simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['eventsByMarkets']);
      expect(ssUtility.queryService).toHaveBeenCalledWith(jasmine.any(Function), extendedParams);
      expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledWith('test data');
      expect(buildUtility.buildEventsWithRacingForm).not.toHaveBeenCalled();
      expect(buildUtility.buildEvents).toHaveBeenCalledWith([{}]);
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getCategories', () => {
    it('should create string of ids and map categories array', fakeAsync(() => {
      const categoriesIds = [20, 30];
      const response = {SSResponse: {
                              children: [
                                {category: {id: 111, displayOrder: 1}},
                                {category: {id: 222, displayOrder: 2}},
                                {category: {id: 333, displayOrder: 3}}
                              ]
                            }
                      };
      ssRequestHelper.getCategories.and.returnValue(Promise.resolve(response));

      const result = service.getCategories(categoriesIds).then((res) => {
                       expect(res).toEqual([{id: 111, displayOrder: 1}, {id: 222, displayOrder: 2}]);
                     });
      tick();

      expect(ssRequestHelper.getCategories).toHaveBeenCalledWith({ categoriesIds: '20,30' });
      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('should pass string id and throw error', fakeAsync(() => {
      const categoriesIds = '50';
      ssRequestHelper.getCategories.and.returnValue(Promise.reject('some error'));

      const result = service.getCategories(categoriesIds).then((res) => {}, (err) => {
                      expect(err).toEqual('some error');
                     });
      tick();

      expect(ssRequestHelper.getCategories).toHaveBeenCalledWith({ categoriesIds: '50' });
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getNamesOfMarketsCollection', () => {
    it('should call methods getSportToCollection, genFilters, stripResponse, filterCollections, sortCollection', fakeAsync(() => {
      spyOn(service, 'filterCollections').and.returnValue('filterCollections');
      spyOn(service, 'sortCollection');

      const result = service.getNamesOfMarketsCollection(51);
      tick();

      expect(ssRequestHelper.getSportToCollection).toHaveBeenCalledWith({simpleFilters: {sportId: 51}});
      expect(simpleFilters.genFilters).toHaveBeenCalledWith({sportId: 51});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getSportToCollection');
      expect(service.filterCollections).toHaveBeenCalledWith('getSportToCollection');
      expect(service.sortCollection).toHaveBeenCalledWith('filterCollections');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getClasses', () => {
    it('should call methods getClassesByCategory and stripResponse', fakeAsync(() => {
      const result = service.getClasses(51);
      tick();

      expect(ssRequestHelper.getClassesByCategory).toHaveBeenCalledWith({siteChannels: 'M',
                                                                         categoryId: 51,
                                                                         hasOpenEvent: '&simpleFilter=class.hasOpenEvent'});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getClassesByCategory');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getTypesByClasses', () => {
    it('should call methods getClassToSubTypeForClass, genFilters and stripResponse', fakeAsync(() => {
      const result = service.getTypesByClasses([51, 61]);
      tick();

      expect(ssRequestHelper.getClassToSubTypeForClass).toHaveBeenCalledWith({ classIds: [51, 61], simpleFilter: ['typesByClasses']});
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(['typesByClasses']);
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getClassToSubTypeForClass');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getClassToSubTypeForTypeByPortions', () => {
    it('should call loadByPortions.get', () => {
      const result = service.getClassToSubTypeForTypeByPortions([51, 61]);

      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), {}, 'typeIds', [51, 61]);
      expect(result).toEqual(jasmine.any(Promise));
    });
  });

  describe('getInPlayEventsWithOutOutcomes', () => {
    it('should choose filters and call methods getEventsList, genFilters, stripResponse and map events', fakeAsync(() => {
      const result = service.getInPlayEventsWithOutOutcomes({eventStatusCode: '161', outcomeStatusCode: '200'}).then((res) => {
                       expect(res).toEqual([{intId: 50}, {intId: 60}]);
                     });
      tick();

      expect(ssRequestHelper.getEventsList).toHaveBeenCalledWith({ simpleFilters: {eventStatusCode: '161'}});
      expect(simpleFilters.genFilters).toHaveBeenCalledWith({eventStatusCode: '161'});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith([{id: 5, event: {intId: 50}}, {id: 6, event: {intId: 60}}]);
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getData', () => {
    it('should choose bet level, call getClasses and return all children objects', fakeAsync(() => {
      const result = service.getData('CLASS', ['12', '13'], true).then((res) => {
        expect(res).toEqual([{childrenId: 1}, {childrenId: 2}]);
      });
      tick();

      expect(ssRequestHelper.getClasses).toHaveBeenCalledWith({ classIds: ['12', '13']});
      expect(result).toEqual(jasmine.any(Promise));
    }));

    it('should choose bet level, call getEventsByMarkets and return one children object', fakeAsync(() => {
      const result = service.getData('MARKET', ['12', '13'], false).then((res) => {
        expect(res).toEqual({childrenId: 12});
      });
      tick();

      expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledWith({ marketIds: ['12', '13']});
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getRacingSpecialsEvents', () => {
    it('should call getEventToLinkedOutcomeForEvent, stripResponse, buildEvents', fakeAsync(() => {
      const result = service.getRacingSpecialsEvents('161');
      tick();

      expect(simpleFilters.genFilters).toHaveBeenCalledWith({priceHistory: true});
      expect(ssRequestHelper.getEventToLinkedOutcomeForEvent).toHaveBeenCalledWith('161', {priceHistory: true});
      expect(ssUtility.stripResponse).toHaveBeenCalledWith('getEventToLinkedOutcomeForEvent');
      expect(buildUtility.buildEvents).toHaveBeenCalledWith('getEventToLinkedOutcomeForEvent');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getInspiredVirtualEvents', () => {
    it('should call getEventsList and buildEvents', fakeAsync(() => {
      const params = {
        racingFormOutcome: true
      };
      spyOn(service, 'getEventsList').and.returnValue(Promise.resolve('events list'));

      const result = service.getInspiredVirtualEvents(params);
      tick();

      expect(service.getEventsList).toHaveBeenCalledWith(params);
      expect(buildUtility.buildEvents).toHaveBeenCalledWith('events list');
      expect(result).toEqual(jasmine.any(Promise));
    }));
  });

  describe('getParams', () => {
    let params;
    let commonParams;

    beforeEach(() => {
      params = {
        racingFormOutcome: true
      };
      commonParams = {
        eventId: 161
      };
    });
    it('should return extended params according to arguments', () => {
      const uniqueParams = {
        crazyHorse: true
      };
      const extendedParams = {
        racingFormOutcome: true,
        eventId: 161,
        crazyHorse: true
      };

      const result = service['getParams'](params, commonParams, uniqueParams);

      expect(result).toEqual(extendedParams);
    });

    it('should return extended params according to arguments w/o unique params', () => {
      const extendedParams = {
        racingFormOutcome: true,
        eventId: 161
      };

      const result = service['getParams'](params, commonParams);

      expect(result).toEqual(extendedParams);
    });
  });

  describe('filterCollections', () => {
    it('should return array of filters', () => {
      const collections = [
        {sport: {
          children: [
            {collection: {drilldownTagNames: 'COLLFLAG_EP,'}},
            {collection: {drilldownTagNames: 'COLLFLAG_UA,'}},
            {collection: {drilldownTagNames: 'COLLFLAG_EP,'}}
          ]
        }}
      ];
      const controlArray = [
        {collection: {drilldownTagNames: 'COLLFLAG_EP,'}},
        {collection: {drilldownTagNames: 'COLLFLAG_EP,'}}
      ];
      const result = service['filterCollections'](collections);

      expect(result).toEqual(controlArray);
    });

    it('should return empty array', () => {
      const collections = [
        {sport: {
          children: [
            {collection: {id: 1}},
            {collection: {id: 2}},
            {collection: {id: 3}}
          ]
        }}
      ];
      const controlArray = [];
      const result = service['filterCollections'](collections);

      expect(result).toEqual(controlArray);
    });

    it('should return undefined', () => {
      const collections = [];
      const result = service['filterCollections'](collections);

      expect(result).toEqual(undefined);
    });
  });

  describe('sortCollection', () => {
    it('should return sorted collection', () => {
      const collections = [
        {collection: {name: 'b'}},
        {collection: {name: 'a'}},
        {collection: {name: 'c'}},
        {collection: {name: 'e'}},
        {collection: {name: 'd'}},
        {collection: {name: 'f'}},
      ];
      const controlArray = [
        {name: 'a'},
        {name: 'b'},
        {name: 'c'},
        {name: 'd'},
        {name: 'e'},
        {name: 'f'}
      ];

      const result = service['sortCollection'](collections);

      expect(result).toEqual(controlArray);
    });
  });

  describe('#getNextEvents', () => {
    let events, params;
    beforeEach(() => {
      params = { classIds: true, racingFormEvent: true, eventsCount: 2 };

      spyOn(service, 'loadEventsPartiallyByClasses').and.callFake(method => {
        method();
        return Promise.resolve(events);
      });
    });

    it('should request to get next races events with no outcomes', fakeAsync(() => {
      events = [{
        event: {
          startTime: 1,
          id: 1
        }
      }] as any;
      expect(simpleFilters.simpleFiltersBank.nextEventsByIds).toEqual(['filter']);
      service.getNextEvents(params).then(data => {
        expect(data).toEqual([] as any);
        expect(service.loadEventsPartiallyByClasses)
          .toHaveBeenCalledWith(jasmine.any(Function), params, simpleFilters.simpleFiltersBank.nextEventsByIds, true);
        expect(service.buildUtility.buildEventsWithRacingForm).toHaveBeenCalled();
        expect(service.ssRequestHelper.getNextNEventToOutcomeForClass).toHaveBeenCalled();
      });
      tick();
    }));

    it('should request to get next races events and isVirtualRacesEnabled', fakeAsync(() => {
      events = [{
        event: {
          startTime: 2,
          id: 1,
          categoryId: '39'
        },
        racingFormOutcome : [{
          refRecordId: '11219',
          silkName: 'Jon',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).toHaveBeenCalled();
      });
      tick();
    }));

    it('should request to get next races events and isVirtualRacesEnabled for includes with virtual racing events', fakeAsync(() => {
      events = [{
        event: {
          startTime: 2,
          endTime: 4,
          id: 1,
          categoryId: '39',
          className: 'greyhounds - Live',
          typeFlagCodes: 'VR'
        },
      }, {
        racingFormOutcome : [{
          refRecordId: '11219',
          silkName: 'Jon',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).toHaveBeenCalled();
      });
      tick();
    }));

    
    it('should call SORT includes with virtual racing events', fakeAsync(() => {
      events = [{
        event: {
          startTime: new Date(),
          endTime: 4,
          id: 1,
          categoryId: '39',
          className: 'greyhounds',
          typeFlagCodes: 'NE'
        },
      },
      {
        event: {
          startTime: new Date(),
          endTime: 5,
          id: 1,
          categoryId: '39',
          className: 'greyhounds',
          typeFlagCodes: 'VR'
        },
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).not.toHaveBeenCalled();
      });
      tick();
    }));

    it('should call SORT includes with virtual racing events', fakeAsync(() => {
      events = [{
        event: {
          startTime: 2,
          endTime: 4,
          id: 1,
          categoryId: '39',
          className: 'greyhounds',
          typeFlagCodes: 'NE'
        },
      },
      {
        event: {
          startTime: 3,
          endTime: 5,
          id: 1,
          categoryId: '39',
          className: 'greyhounds',
          typeFlagCodes: 'VR'
        },
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).not.toHaveBeenCalled();
      });
      tick();
    }));

    it('should request to get next races events and isVirtualRacesEnabled for includes with virtual racing events', fakeAsync(() => {
      events = [{
        event: {
          startTime: 2,
          endTime: 4,
          id: 1,
          categoryId: '39',
          className: 'greyhounds - Live',
          typeFlagCodes: 'VR'
        },
      }, {
        racingFormOutcome : [{
          refRecordId: '11219',
          silkName: 'Jon',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      },
      {
        event: {
          startTime: 3,
          endTime: 5,
          id: 1,
          categoryId: '39',
          className: 'greyhounds - Live',
          typeFlagCodes: 'VR'
        },
      }, {
        racingFormOutcome : [{
          refRecordId: '111219',
          silkName: 'Jon1',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).toHaveBeenCalled();
      });
      tick();
    }));

    it('should request to get next races events and isVirtualRacesEnabled racingoutcomes', fakeAsync(() => {
      events = [{
        racingFormOutcome : [{
          refRecordId: '11219',
          silkName: 'Jon',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      }] as any;
      params.isVirtualRacesEnabled = true;
      params.virtualRaceStartTime = 1;
      params.virtualRaceEndTime = 5;
      service.getNextEvents(params).then(data => {
        expect(service.buildUtility.buildEventWithRacingFormOutcomes).toHaveBeenCalled();
      });
      tick();
    }));

    it('should request to get next races events and isVirtualRacesEnabled category is different', fakeAsync(() => {
      events = [{
        event: {
          startTime: 2,
          id: 1,
          categoryId: '21'
        },
        racingFormOutcome : [{
          refRecordId: '11219',
          silkName: 'Jon',
          id: '121',
          jockey: 'Jon',
          trainer: 'Jon'
        }]
      }] as any;
      params.isVirtualRacesEnabled = true;
      service.getNextEvents(params).then(data => {
        expect(service.ssRequestHelper.getNextNEventToOutcomeForClass).toHaveBeenCalled();
      });
      tick();
    }));
    
    describe('should request to get next races events with', () => {
      events = [{
        event: {
          startTime: 1,
          id: 1
        }
      }] as any;
      it('empty markets', () => events[0].event.children = []);
      it('no valid markets', () => events[0].event.children = [{}]);
      it('no outcomes', () => events[0].event.children = [{ market: {} }]);
      it('empty outcomes', () => events[0].event.children = [{ market: { children: [] } }]);

      afterEach(fakeAsync(() => {
        service.getNextEvents(params).then(data => expect(data).toEqual([]));
        tick();
      }));
    });

    it('should request to get next races events with outcomes', fakeAsync(() => {
      events = [{
        event: {
          startTime: 3,
          id: 1,
          children: [{ market: { children: [{}] } }]
        }
      }, {
        event: {
          startTime: 1,
          id: 1,
          children: [{ market: { children: [{}] } }]
        }
      }, {
        event: {
          startTime: 2,
          id: 1,
          children: [{ market: { children: [{}] } }]
        }
      }] as any;

      const sortedResult = [{
        event: {
          startTime: 1,
          id: 1,
          children: [{ market: { children: [{}] } }]
        }
      }, {
        event: {
          startTime: 2,
          id: 1,
          children: [{ market: { children: [{}] } }]
        }
      }] as any;
      service.getNextEvents(params).then(data => {
        expect(data).toEqual(sortedResult);
      });
      tick();
    }));
  });
  describe('getEvent', ()=> {
    beforeEach(()=>{
      ssUtility.stripResponse.calls.reset();
      buildUtility.buildEventsWithExternalKeys.calls.reset();
      buildUtility.buildEventsWithRacingForm.calls.reset();
      buildUtility.buildEventWithScores.calls.reset();
    });
    it('should build racing event', done => {
      service.getEvent(1, {}, false).then(() => {
        expect(ssRequestHelper.getEventsByEvents).toHaveBeenCalledTimes(1);
        expect(ssUtility.stripResponse).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(1);
        done();
      });
    });

    it('should build gaming event with scorecast for MTA Sport', done => {
      service.getEvent(1, {scorecast: true}, true, true).then(() => {
        expect(ssRequestHelper.getEventToMarketForEvent).toHaveBeenCalledTimes(1);
        expect(ssUtility.stripResponse).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithScorecasts).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(1);
        done();
      });
    });

    it('should build gaming event without scorecast for non-MTA Sport', done => {
      service.getEvent(1, {scorecast: false}, true, false).then(() => {
        expect(ssRequestHelper.getEventByIds).toHaveBeenCalledTimes(1);
        expect(ssUtility.stripResponse).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEvents).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(1);
        done();
      });
    });
  });

  describe('getEventByMarkets', ()=>{
    beforeEach(()=>{
      ssUtility.stripResponse.calls.reset();
      buildUtility.buildEventsWithExternalKeys.calls.reset();
      buildUtility.buildEventsWithRacingForm.calls.reset();
      buildUtility.buildEventWithScores.calls.reset();
    });
    it('should build event for certain markets with scorecast', done => {
      service.getEventByMarkets([1], {scorecast: true}).then(() => {
        expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledTimes(1);
        expect(ssUtility.stripResponse).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithScorecasts).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(1);
        done();
      });
    });

    it('should build event for certain markets without scorecast', done => {
      service.getEventByMarkets([1], {scorecast: false}).then(() => {
        expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledTimes(1);
        expect(ssUtility.stripResponse).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEvents).toHaveBeenCalledTimes(1);
        expect(buildUtility.buildEventWithScores).toHaveBeenCalledTimes(1);
        done();
      });
    });
  });

  describe('#getExtraPlaceMarkets', () => {
    beforeEach(() => {
      simpleFilters.getFilterParams.and.returnValue({
        simpleFilters: 'classIds=true'
      });
    });

    it('no siteServerEventsCount', fakeAsync(() => {
      const params = { classIds: true };

      service.getExtraPlaceMarkets(['1'], params).then(null, () => {});
      expect(loadByPortions.get).toHaveBeenCalled();
      expect(simpleFilters.getFilterParams).toHaveBeenCalled();
    }));

    it('with siteServerEventsCount', fakeAsync(() => {
      const params = { classIds: true, siteServerEventsCount: 3 };

      service.getExtraPlaceMarkets(['1'], params).then(null, () => {});
      expect(loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function),
        { simpleFilters: 'classIds=true', siteServerEventsCount: 3 }, 'classIds', ['1']);
      expect(simpleFilters.getFilterParams).toHaveBeenCalled();
    }));
  });

  describe('#getExtraPlaceEvents', () => {
    it('getExtraPlaceEvents()', fakeAsync(() => {
      const params = { classIds: true };

      service.getExtraPlaceEvents(params).then(null, () => { });
      tick();
      expect(eventsByClasses.getClassesByParams).toHaveBeenCalled();
      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalled();
    }));
  });

  describe('loadEventsPartiallyByClasses', () => {
    beforeEach(() => {
      simpleFilters.getFilterParams.and.returnValue({
        simpleFilter: 'param=value'
      });
    });

    it('with siteServerEventsCount', fakeAsync(() => {
      const params = { param: true, siteServerEventsCount: 3 } as any;

      service.loadEventsPartiallyByClasses(() => {}, params, ['str'], [1, 2]).then(
        result => {
          expect(service.simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['str']);
          expect(service.loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function),
            { simpleFilter: 'param=value', siteServerEventsCount: 3 }, 'classIds', [1, 2]);
        }
      );
      tick();
    }));

    it('without siteServerEventsCount', fakeAsync(() => {
      const params = { param: true } as any;
      service.loadEventsPartiallyByClasses(() => {}, params, ['str'], [1, 2]).then(
        result => {
          expect(service.simpleFilters.getFilterParams).toHaveBeenCalledWith(params, ['str']);
          expect(service.loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function),
            { simpleFilter: 'param=value' }, 'classIds', [1, 2]);
        }
      );
      tick();
    }));
  });

  it('loadSpecificEventsByIds()', () => {
    simpleFilters.getFilterParams.and.returnValue({
      siteChannels: 'M'
    });
    const result = service.loadSpecificEventsByIds(() => {}, { param: true }, ['str'], [1, 2]);

    expect(service.simpleFilters.getFilterParams).toHaveBeenCalledWith({ param: true }, ['str']);
    expect(service.loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), { siteChannels: 'M' }, 'eventsIds', [1, 2]);
    expect(result.then).toEqual(jasmine.any(Function));
  });

  it('loadResultsOfEvent()', () => {
    simpleFilters.getFilterParams.and.returnValue({ id: 1 });
    service.loadResultsOfEvent({}, { id: 2});

    expect(simpleFilters.getFilterParams).toHaveBeenCalled();
    expect(service.loadByPortions.get).toHaveBeenCalledWith(jasmine.any(Function), { id: 1 }, 'eventsIds', [2]);
  });

  it('getEventsByOutcomeIds', fakeAsync(() => {
    service.isValidFzSelection = true;
    time.getSuspendAtTime.calls.reset();
    loadByPortions.get.calls.reset();
    ssRequestHelper.getEventsByOutcomes.calls.reset();
    simpleFilters.getFilterParams.calls.reset();
    buildUtility.buildEventsWithExternalKeys.calls.reset();
    buildUtility.buildEventsWithRacingForm.calls.reset();
    buildUtility.buildEventsWithOutMarketCounts.calls.reset();

    service.getEventsByOutcomeIds({ outcomesIds: [{}], racingFormOutcome: true }, false);
    tick();

    service.getEventsByOutcomeIds({ outcomesIds: [{}], racingFormOutcome: false }, true);
    tick();

    service.getEventsByOutcomeIds({ outcomesIds: [] }, true);
    tick();

    expect(ssRequestHelper.isValidFzSelection).toBe(true);
    expect(time.getSuspendAtTime).toHaveBeenCalledTimes(3);
    expect(loadByPortions.get).toHaveBeenCalledTimes(2);
    expect(ssRequestHelper.getEventsByOutcomes).toHaveBeenCalledTimes(2);
    expect(simpleFilters.getFilterParams).toHaveBeenCalledTimes(2);
    expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(2);
    expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledTimes(1);
    expect(buildUtility.buildEventsWithOutMarketCounts).toHaveBeenCalledTimes(1);
  }));
});
