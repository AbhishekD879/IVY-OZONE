import { of as observableOf } from 'rxjs';
import { EventService } from '@sb/services/event/event.service';
import { ISportEvent } from '@core/models/sport-event.model';

describe('#EventService', () => {
  let service;
  let siteServerService;
  let timeService;
  let cacheEventsService;
  let eventFiltersService;
  let liveStreamService;
  let cashOutLabelService;
  let eventsByClasseService;
  let isPropertyAvailableService;
  let eventObj;
  let awsService;
  let cmsService;

  beforeEach(() => {
    eventObj = { id: 1 };
    siteServerService = {
      getEventsByMarkets: jasmine.createSpy('getEventsByMarkets').and.returnValue(Promise.resolve([{}, {}])),
      getEventsByEventsIds: jasmine.createSpy('getEventsByEventsIds'),
      getResultsByClasses: jasmine.createSpy('getResultsByClasses'),
      getCouponsList: jasmine.createSpy('getCouponsList'),
      getJackpotList: jasmine.createSpy('getJackpotList'),
      getEvent: jasmine.createSpy('getEvent'),
      getEventByMarkets: jasmine.createSpy('getEventByMarkets'),
      getInPlayEventsWithOutOutcomes: jasmine.createSpy('getInPlayEventsWithOutOutcomes'),
      getEventsByClasses: jasmine.createSpy('getEventsByClasses'),
      getCouponEventsByCouponId: jasmine.createSpy('getCouponEventsByCouponId'),
      getNextEventsByType: jasmine.createSpy('getNextEventsByType').and.returnValue(Promise.resolve([])),
      getInPlayEventsByClassesOnlyStream: jasmine.createSpy('getInPlayEventsByClassesOnlyStream'),
      getEventsByCategory: jasmine.createSpy('getEventsByCategory'),
      getEventsByTypeId: jasmine.createSpy('getEventsByTypeId'),
      getEventsByTypeWithMarketCounts: jasmine.createSpy('getEventsByTypeWithMarketCounts'),
      getExtraPlaceEvents: jasmine.createSpy('getExtraPlaceEvents').and.returnValue(Promise.resolve(null)),
      addAvailability: jasmine.createSpy('addAvailability').and.returnValue(Promise.resolve([])),
      getNamesOfMarketsCollection: jasmine.createSpy('getExtraPlaceEvents'),
      loadScoresAndClock: jasmine.createSpy('loadScoresAndClock'),
      getNextEvents: jasmine.createSpy('getNextEvents').and.returnValue(Promise.resolve(
        [{ typeFlagCodes: 'UK', categoryCode: 'HORSE_RACING' },
          { typeFlagCodes: 'INT', categoryCode: 'HORSE_RACING' },
          { typeFlagCodes: 'UK', categoryCode: 'GH' }])),
    };
    timeService = {
      apiDataCacheInterval: {
        event: 200
      },
      getCurrentTime: jasmine.createSpy('getCurrentTime').and.returnValue(400),
      getSuspendAtTime: jasmine.createSpy()
    };
    cacheEventsService = {
      storedData: {
        event: {
          1: {
            updated: 100,
            data: {
              id: 1
            }
          },
          2: {
            updated: 1540985035842,
            data: {
              id: 1
            }
          },
          cached: {
            updated: 1540985035842,
            data: {}
          },
          data: {
            id: 1
          }
        }
      },
      stored: jasmine.createSpy('stored'),
      store: jasmine.createSpy('store'),
      async: jasmine.createSpy('async'),
      addToIndex: jasmine.createSpy('addToIndex'),
      storeNewOutcomes: jasmine.createSpy('storeNewOutcomes'),
      setOutcomesFetched: jasmine.createSpy('setOutcomesFetched')
    };
    eventFiltersService = {
      applyFilters: jasmine.createSpy('applyFilters').and.returnValue(() => {})
    };
    liveStreamService = {
      checkCondition: jasmine.createSpy('checkCondition'),
      addLiveStreamAvailability: jasmine.createSpy('addLiveStreamAvailability').and.returnValue(() => {}),
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue(() => {})
    };
    cashOutLabelService = {
      checkCondition: jasmine.createSpy('checkCondition')
    };
    eventsByClasseService = {
      getClasses: jasmine.createSpy('getClasses').and.returnValue(Promise.resolve(['603', '492'])),
      getClassesByParams: jasmine.createSpy('getClassesByParams').and.returnValue(Promise.resolve(['603', '492']))
    };
    isPropertyAvailableService = {
      isPropertyAvailable: jasmine.createSpy('isPropertyAvailable')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction'),
    };
    cmsService = {
      isEDPLogsEnabled: jasmine.createSpy('isEDPLogsEnabled').and.returnValue(observableOf({})),
      getVirtualSportstoPromise: jasmine.createSpy('getVirtualSportstoPromise').and.returnValue(Promise.resolve([
        {
          "id": "5ef02767c9e77c0001f6e35d",
          "title": "Victoria Park",
          "tracks": [
              {
                  "id": "5f156fe1c9e77c0001814a02",
                  "title": "Surrey Downs",
                  "classId": "36006",
              },
          ]
      }
    ]))
    };

    service = new EventService(
      cacheEventsService,
      siteServerService,
      timeService,
      eventFiltersService,
      liveStreamService,
      cashOutLabelService,
      eventsByClasseService,
      isPropertyAvailableService,
      awsService,
      cmsService
    );
  });

  it('#constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#inPlayEventsOnlyStream', () => {
    it('call should return a function', () => {
      expect(service.inPlayEventsOnlyStream('cacheName')).toEqual(jasmine.any(Function));
    });
  });

  describe('#cachedEvents', () => {
    it('should Store events or get new', () => {
      service.cachedEvents(siteServerService.getExtraPlaceEvents)({
        date: 'today', categoryId: '129'
      }, 'extraPlaceEventsHR');

      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR', 'today', '129');
    });

    it('should Store events or get new', () => {
      cacheEventsService.stored.and.returnValue('events');
      service.cachedEvents(siteServerService.getExtraPlaceEvents)({
        date: 'today', categoryId: '129'
      });

      expect(cacheEventsService.async).toHaveBeenCalledWith('events');
    });
  });

  describe('#cachedCouponEvents', () => {
    it('should Store events or get new cachedCouponEvents', () => {
      service.cachedCouponEvents(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR')({
        couponId: 'couponId'
      });

      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR', 'couponId');
    });

    it('should Store events or get new cachedCouponEvents', () => {
      cacheEventsService.stored.and.returnValue('events');
      service.cachedCouponEvents(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR')({
        couponId: 'couponId'
      });

      expect(cacheEventsService.async).toHaveBeenCalledWith('events');
    });
  });

  describe('#cachedEventsByFn', () => {
    it('should Store events or get new without params', () => {
      service.cachedEventsByFn(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR', 'categoryId')({});

      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR');
    });

    it('should Store events or get new without params', () => {
      cacheEventsService.stored.and.returnValue('events');
      service.cachedEventsByFn(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR', 'categoryId')({});

      expect(cacheEventsService.async).toHaveBeenCalledWith('events');
    });

    it('should Store events or get new with params', () => {
      service.cachedEventsByFn(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR', 'categoryId')({
        categoryId: 'categoryId'
      });

      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR', 'categoryId');
    });

    it('should Store events or get new with params', () => {
      cacheEventsService.stored.and.returnValue('events');
      service.cachedEventsByFn(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR', 'categoryId')({
        categoryId: 'categoryId'
      });

      expect(cacheEventsService.async).toHaveBeenCalledWith('events');
    });
  });

  describe('#defineHRsilksType', () => {
    beforeEach(() => {
      service.isUKorIRE = jasmine.createSpy('isUKorIRE').and.callFake((obj: ISportEvent) => {
        return ['UK', 'INT'].some((country: string) => obj.typeFlagCodes ? obj.typeFlagCodes.indexOf(country) > -1 : false);
      });
    });

    it('should not define HR silks type', () => {
      const mockObj: any = [{ categoryCode: 'FB' }, {}];
      service['defineHRsilksType'](mockObj).then((res) => {
        expect(res[0].isUKorIRE).toBeFalsy();
      });
    });

    it('should define HR silks type', () => {
      const mockObj: any = [{ categoryCode: 'HORSE_RACING', typeFlagCodes: 'UK' }, {}];
      service['defineHRsilksType'](mockObj).then((res) => {
        expect(res[0].isUKorIRE).toBeTruthy();
      });
    });
  });

  describe('#getNextEventsFn', () => {
    it('should call isUKorIRE', () => {
      const errorHandler = jasmine.createSpy('errorHanler');
      service.getNextEventsFn({ categoryId: '21', siteChannels: 'M' }).then(res => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
        expect(siteServerService.getNextEvents).toHaveBeenCalled();
        expect(res[0].isUKorIRE).toBeTruthy();
        expect(res[1].isUKorIRE).toBeFalsy();
        expect(res[2].isUKorIRE).toBeFalsy();
      }, errorHandler);
      expect(errorHandler).not.toHaveBeenCalled();
    });
    it('should handle error', () => {
      const successHandler = jasmine.createSpy('successHandler');
      siteServerService.getNextEvents.and.returnValue(Promise.reject('err message'));
      service.getNextEventsFn({ categoryId: '21', siteChannels: 'M' }).then(successHandler, err => {
        expect(err).toEqual('err message');
      });
      expect(successHandler).not.toHaveBeenCalled();
    });
  });

  describe('#isDataOutdated', () => {
    it('call should return a boolean', () => {
      expect(service.isDataOutdated(cacheEventsService.storedData.event.cached.updated, 1)).toEqual(jasmine.any(Boolean));
    });

    it('call awsService.addAction when Edplogs enabled', () => {
      cmsService.isEDPLogsEnabled = jasmine.createSpy().and.returnValue(observableOf(true));
      service.isDataOutdated(11223, 2);
      expect(awsService.addAction).toHaveBeenCalledWith('EventService=>isDataOutdated=>Start', { eventId: 11223 });
    });

    it('should not call awsService.addAction when Edplogs disabled', () => {
      cmsService.isEDPLogsEnabled = jasmine.createSpy().and.returnValue(observableOf(false));
      service.isDataOutdated(11223, 2);
      expect(awsService.addAction).toHaveBeenCalledTimes(0);
    });

    it('call should return true', () => {
      expect(service['isDataOutdated'](123, 2)).toBeTruthy();
    });

    it('call should return false', () => {
      timeService.getCurrentTime.and.returnValue(400);

      expect(service['isDataOutdated'](1, 200000)).toBeFalsy();
      expect(timeService.getCurrentTime).toHaveBeenCalled();
    });

    it('call should return true', () => {
      timeService.getCurrentTime.and.returnValue(1540985035899);

      expect(service['isDataOutdated'](1, 2)).toBeTruthy();
      expect(timeService.getCurrentTime).toHaveBeenCalled();
    });
    it('call should return true when cacheEventsService storedData event is undefined', () => {
      cacheEventsService.storedData.event = undefined;
      expect(service['isDataOutdated'](1234, 2)).toBeTruthy();
    });
    it('call should return true when cacheEventsService storedData is undefined', () => {
      cacheEventsService.storedData = undefined;
      expect(service['isDataOutdated'](1234, 2)).toBeTruthy();
    });
  });

  describe('#getEvent', () => {
    it('should fetch event from server', () => {
      siteServerService.getEvent.and.returnValue(Promise.resolve([{ }, {}]));
      service.isLiveSimAvailable = jasmine.createSpy('isLiveSimAvailable').and.returnValue(Boolean);
      service.isUKorIRE = jasmine.createSpy('isUKorIRE');

      service.getEvent().then(() => {
        siteServerService.getEvent().then(res => {
          expect(res).not.toEqual([]);
          expect(liveStreamService.isLiveStreamAvailable).toHaveBeenCalled();
          expect(service.isLiveSimAvailable).toHaveBeenCalled();
          expect(service.isUKorIRE).toHaveBeenCalled();
          expect(cacheEventsService.addToIndex).toHaveBeenCalled();
        });
      });
    });
    it('should fetch empty event from server', () => {
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent().then(() => {
        siteServerService.getEvent().then(res => {
          expect(res).toEqual([]);
        });
      });
    });
    it('should fetch event from cache', () => {
      cacheEventsService.storedData.event.data = [{id: 12345}];
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent('12345', {}, true).then(res => 
        expect(res).toEqual(cacheEventsService.storedData.event.data));
    });
    it('should fetch event from cache when marketIds are given', () => {
      siteServerService.getEventByMarkets.and.returnValue(Promise.resolve([{id: 12345, markets: [{id: 1, outcomes: [{id:1}]}]}]));
      cacheEventsService.storedData.event.data = [{id: 12345, markets: [{id: 1, outcomes: [{id: 10}]}]}];
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent('12345', {}, true, true, true, [1, 2]).then(res => 
        expect(res).toEqual(cacheEventsService.storedData.event.data));
    });
    it('should fetch event from server when outcomes are unavailable', () => {
      siteServerService.getEventByMarkets.and.returnValue(Promise.resolve([{id: 12345, markets: [{id: 1, outcomes: [{id:1}]}]}]));
      cacheEventsService.storedData.event.data = [{id: 12345, markets: [{id: 1}]}];
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent('12345', {}, true, true, true, [1, 2]).then(res =>{
        siteServerService.getEventByMarkets(['1', '2']).then(()=>{
          expect(cacheEventsService.storeNewOutcomes).toHaveBeenCalled();
        });
      });
    });
    it('should fetch event from server when outcomes are empty', () => {
      siteServerService.getEventByMarkets.and.returnValue(Promise.resolve([{id: 12345, markets: [{id: 1}]}]));
      cacheEventsService.storedData.event.data = [{id: 12345, markets: [{id: 1, outcomes:[]}]}];
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent('12345', {}, true, true, true, [1, 2]).then(res =>{
        siteServerService.getEventByMarkets().then(()=>{
          expect(cacheEventsService.storeNewOutcomes).not.toHaveBeenCalled();
        });
      });      
    });

    it('should not call storeNewOutcomes when outcomes returned are empty', () => {
      siteServerService.getEventByMarkets.and.returnValue(Promise.resolve([{id: 12345, markets: [{id: 1}]}]));
      cacheEventsService.storedData.event.data = [{id: 12345, markets: [{id: 1, outcomes:[{}]}]}];
      siteServerService.getEvent.and.returnValue(Promise.resolve([]));
      service.getEvent('12345', {}, true, true, true, [1, 2]).then(res =>{
        siteServerService.getEventByMarkets().then(()=>{
          expect(cacheEventsService.storeNewOutcomes).not.toHaveBeenCalled();
        });
      });      
    });

    it('Should catch error when getEventByMarkets is failed', () => {
      siteServerService.getEventByMarkets.and.returnValue(Promise.reject());
      cacheEventsService.storedData.event.data = [{id: 12345, markets: [{id: 1}]}];
      service.getEvent('12345', {}, true, true, true, [1, 2]).then(() => {
        expect(siteServerService.getEventByMarkets).toHaveBeenCalled();
      }).catch(() => {});
    });

    it('Should catch error when getEvent is failed', () => {
      siteServerService.getEvent.and.returnValue(Promise.reject());
      service.getEvent().then(() => {
        expect(siteServerService.getEvent).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#favouritesMatches', () => {
    it('Should ok', () => {
      siteServerService.getEventsByEventsIds.and.returnValue(Promise.resolve([{}, {}]));
      service.favouritesMatches({}).then(() => {
        expect(siteServerService.getEventsByEventsIds).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      siteServerService.getEventsByEventsIds.and.returnValue(Promise.reject());
      service.favouritesMatches({}).then(() => {
        expect(siteServerService.getEventsByEventsIds).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getEventsByClasses', () => {
    it('Should ok', () => {
      siteServerService.getEventsByCategory.and.returnValue(Promise.resolve([{}, {}]));
      service['addAvailability'] = jasmine.createSpy('addAvailability');
      service.getEventsByClasses().then(() => {
        expect(siteServerService.getEventsByCategory).toHaveBeenCalled();
        expect(service.addAvailability).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      siteServerService.getEventsByCategory.and.returnValue(Promise.reject());
      service.getEventsByClasses().then(() => {
        expect(siteServerService.getEventsByCategory).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getEventsByTypeWithMarketCounts', () => {
    it('Should error', () => {
      siteServerService.getEventsByTypeWithMarketCounts.and.returnValue(Promise.reject());
      service.getEventsByTypeWithMarketCounts().then(() => {
        expect(siteServerService.getEventsByTypeWithMarketCounts).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#eventsByTypeIds', () => {
    it('Should error', () => {
      siteServerService.getEventsByTypeId.and.returnValue(Promise.reject());
      service.eventsByTypeIds().then(() => {
        expect(siteServerService.getEventsByTypeId).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#isInPlayEventsOnlyStream', () => {
    it('Should ok', () => {
      siteServerService.getInPlayEventsByClassesOnlyStream.and.returnValue(Promise.resolve([{}, {}]));
      service.isInPlayEventsOnlyStream().then(() => {
        expect(siteServerService.getInPlayEventsByClassesOnlyStream).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      siteServerService.getInPlayEventsByClassesOnlyStream.and.returnValue(Promise.reject());
      service.isInPlayEventsOnlyStream().then(() => {
        expect(siteServerService.getInPlayEventsByClassesOnlyStream).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#resultsByClasses', () => {
    it('Should error', () => {
      siteServerService.getResultsByClasses.and.returnValue(Promise.reject());
      service.resultsByClasses().then(() => {
        expect(siteServerService.getResultsByClasses).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getNextEventsFn', () => {
    let params;

    beforeEach(() => {
      params = {
        typeId: 0
      };
    });

    it('Should ok 1', () => {
      params.typeId = 4;

      service.getNextEventsFn(params).then(([]) => {
        expect(siteServerService.getNextEventsByType).toHaveBeenCalled();
      });
    });

    it('Should ok 2', () => {
      service.getEvents = jasmine.createSpy('getEvents').and.returnValue(Promise.resolve([]));
      eventsByClasseService.getClasses.and.returnValue(Promise.resolve([{}, {}]));
      service.getNextEventsFn(params).then(([]) => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
        expect(service.getEvents).toHaveBeenCalled();
      });
    });

    it('Should ok 2 and isVirtualRacesEnabled', () => {
      params.isVirtualRacesEnabled = true;
      params.virtualRacesIncluded = ['Surrey Downs'];
      service.getEvents = jasmine.createSpy('getEvents').and.returnValue(Promise.resolve([]));
      eventsByClasseService.getClasses.and.returnValue(Promise.resolve([{}, {}]));
      service.getNextEventsFn(params).then(([]) => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
        expect(service.getEvents).toHaveBeenCalled();
      });
    });
    it('Should ok 2 and isVirtualRacesEnabled class name not mataches', () => {
      params.isVirtualRacesEnabled = true;
      params.virtualRacesIncluded = ['Surrey Ups'];
      service.getEvents = jasmine.createSpy('getEvents').and.returnValue(Promise.resolve([]));
      eventsByClasseService.getClasses.and.returnValue(Promise.resolve([{}, {}]));
      service.getNextEventsFn(params).then(([]) => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
        expect(service.getEvents).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      eventsByClasseService.getClassesByParams.and.returnValue(Promise.reject());
      service.getNextEventsFn(params).then(() => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
      }).catch(() => {});
    });
    it('Should error', () => {
      eventsByClasseService.getClasses.and.returnValue(Promise.reject());
      service.getNextEventsFn(params).then(([]) => {
        expect(eventsByClasseService.getClassesByParams).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getFilteredEvents', () => {
    let loader;

    beforeEach(() => {
      loader = jasmine.createSpy('loader');
    });

    it('Should ok', () => {
      loader.and.returnValue(Promise.resolve([])).and.returnValue(Promise.resolve([{}, {}]));

      service.getFilteredEvents(loader).then(() => {
        expect(loader).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      loader.and.returnValue(Promise.reject());

      service.getFilteredEvents(loader).then(() => {
        expect(loader).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#couponsList', () => {
    it('Should error', () => {
      siteServerService.getCouponsList.and.returnValue(Promise.reject());
      service.couponsList().then(() => {
        expect(siteServerService.getCouponsList).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getCouponEventsByCouponId', () => {
    it('Should error', () => {
      siteServerService.getCouponEventsByCouponId.and.returnValue(Promise.reject());
      service.getCouponEventsByCouponId().then(() => {
        expect(siteServerService.getCouponEventsByCouponId).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#isSpecialsAvailable', () => {
    beforeEach(() => {
      service.getEventsByClasses = jasmine.createSpy('getEventsByClasses');
    });

    it('Should ok and return frue', () => {
      service.getEventsByClasses.and.returnValue(Promise.resolve([{}, {}]));
      service.isSpecialsAvailable().then(() => {
        expect(service.getEventsByClasses).toHaveBeenCalled();
      });
    });

    it('Should error', () => {
      service.getEventsByClasses.and.returnValue(Promise.reject());
      service.isSpecialsAvailable().then(() => {
        expect(service.getEventsByClasses).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getFootballJackpotList', () => {
    it('Should ok', () => {
      service.getJackpotListbyMarkets = jasmine.createSpy('getJackpotListbyMarkets').and.returnValue(Promise.resolve([{}, {}]));
      siteServerService.getJackpotList.and.returnValue(Promise.resolve([{}, {}]));
      service.getFootballJackpotList().then(() => {
        expect(siteServerService.getJackpotList).toHaveBeenCalled();
        expect(service.getJackpotListbyMarkets).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      siteServerService.getJackpotList.and.returnValue(Promise.reject());
      service.getFootballJackpotList().then(() => {
        expect(siteServerService.getJackpotList).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getDailyRacingEvents', () => {
    let requestData;

    beforeEach(() => {
      requestData = {
        suspendAtTime: jasmine.createSpy()
      };
    });

    it('Should ok', () => {
      service.addAvailability = jasmine.createSpy('addAvailability');
      siteServerService.getEventsByClasses.and.returnValue(Promise.resolve([{}, {}]));
      service.getDailyRacingEvents(requestData).then(() => {
        expect(siteServerService.getEventsByClasses).toHaveBeenCalled();
        expect(timeService.getSuspendAtTime).toHaveBeenCalled();
        expect(service.addAvailability).toHaveBeenCalled();
      });
    });
    it('Should error', () => {
      siteServerService.getEventsByClasses.and.returnValue(Promise.reject());
      service.getDailyRacingEvents(requestData).then(() => {
        expect(siteServerService.getEventsByClasses).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#inPlayEventsWithOutOutcomes', () => {
    it('Should error', () => {
      siteServerService.getInPlayEventsWithOutOutcomes.and.returnValue(Promise.reject());
      service.inPlayEventsWithOutOutcomes().then(() => {
        expect(siteServerService.getInPlayEventsWithOutOutcomes).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#isLiveStreamAvailable', () => {
    it('call should return a ISportEvent', () => {
      service.isLiveStreamAvailable(eventObj);

      expect(liveStreamService.isLiveStreamAvailable).toHaveBeenCalled();
    });
  });

  describe('#isLiveSimAvailable', () => {
    it('call should return a boolean', () => {
      service.isUKorIRE = jasmine.createSpy('isUKorIRE');

      service.isLiveSimAvailable(eventObj);
      expect(service.isUKorIRE).toHaveBeenCalledWith(eventObj);
    });
  });

  describe('#isUKorIRE', () => {
    it('call should return a boolean', () => {
      expect(service.isUKorIRE({})).toEqual(jasmine.any(Boolean));
    });
  });

  describe('#getJackpotListbyMarkets', () => {
    it('Should return false', () => {
      service.getJackpotListbyMarkets([]).then(() => {
        Promise.resolve(false);
      });
    });

    it('Should return list', () => {
      const data = [{}];

      service.getSortedPools = jasmine.createSpy('isUKorIRE');
      service.getEventsByMarkets = jasmine.createSpy('getEventsByMarkets').and.returnValue(Promise.resolve([]));
      service.getJackpotListbyMarkets(data).then(() => {
        expect(service.getSortedPools).toHaveBeenCalledWith(data);
        expect(service.getEventsByMarkets).toHaveBeenCalled();
      });
    });
  });

  describe('#getEventsByMarkets', () => {
    let sortedPools;

    beforeEach(() => {
      sortedPools = [{
        pool: {}
      }];
    });

    it('Should ok 1', () => {
      service.getEventsByMarkets(sortedPools, 0).then(() => {
        expect(siteServerService.getEventsByMarkets).toHaveBeenCalled();
      });
    });
    it('Should ok 2', () => {
      sortedPools = [
        {
          pool: {
            marketIds: 1
          }
        },
        {
          pool: {
            marketIds: 2
          }
        }
      ];

      service.getEventsByMarkets = jasmine.createSpy('getEventsByMarkets').and.returnValue(Promise.resolve([{}, {}]));
      siteServerService.getEventsByMarkets.and.returnValue(Promise.resolve([{}, {}]));
      service.getEventsByMarkets(sortedPools, 0).then(() => {
        expect(service.getEventsByMarkets).toHaveBeenCalled();
      });
    });

    it('Should ok 3', () => {
      sortedPools = [];

      for (let i = 0; i < 15; i++) {
        sortedPools.push({ pool: {} });
      }

      service.getEventsByMarkets(sortedPools, 0).then(() => {
        expect(siteServerService.getEventsByMarkets).toHaveBeenCalled();
      });
    });

    it('Should error', () => {
      siteServerService.getEventsByMarkets.and.returnValue(Promise.reject());
      service.getEventsByMarkets(sortedPools, 0).then(() => {
        expect(siteServerService.getEventsByMsarkets).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  describe('#getEvents', () => {
    it('Should error', () => {
      siteServerService.getNextEvents.and.returnValue(Promise.reject());
      service.getEvents().then(() => {
        expect(siteServerService.getNextEvents).toHaveBeenCalled();
      }).catch(() => {});
    });
  });

  it('getSortedPools', () => {
    const pools = <any>[
      { pool: { id: 5 } },
      { pool: { id: 4 } }
    ];
    service['getSortedPools'](pools);

    expect(service['getSortedPools'](pools)[1].pool.id).toEqual(5);
  });
});
