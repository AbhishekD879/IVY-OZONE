import { LiveStreamWidgetService } from './live-stream-widget.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('LDLiveStreamWidgetService', () => {
  let service: LiveStreamWidgetService;

  let pubSubService, cacheEventsService, wsUpdateEventService,
    commentsService, inplayHelperService, filtersService;
  const competitionEvents = [
    {
      typeName: null,
      markets: [{
        id: 1
      }],
      displayOrder: 2,
      id: 5,
      comments: [{}],
    },
    {
      typeName: null,
      markets: [{
        id: 2
      }],
      displayOrder: 1,
      id: 6,
      comments: [{}]
    },
    {
      typeName: null,
      markets: [],
      displayOrder: 2,
      id: 7,
      comments: [{}]
    }];

  beforeEach(() => {
    filtersService = {
      orderBy: jasmine.createSpy('orderBy').and.callFake((data) => data)
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    cacheEventsService = {
      storedData: {
        index: {
          data: [
            {
              id: 10
            }
          ]
        }
      }
    };
    wsUpdateEventService = {
      subscribe: () => { },
    };
    commentsService = {
      testMSInitParse: jasmine.createSpy('testMSInitParse')
    };
    inplayHelperService = {
      getSportData: jasmine.createSpy('getSportData'),
      get: jasmine.createSpy('inplayHelperService').and.returnValue(of(competitionEvents)),
      subscribeForLiveUpdates: jasmine.createSpy('subscribeForLiveUpdates').and.returnValue([1])
    };

    service = new LiveStreamWidgetService(
      pubSubService,
      cacheEventsService,
      wsUpdateEventService,
      commentsService,
      inplayHelperService,
      filtersService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getData', () => {
    beforeEach(() => {
      service['addLiveUpdatesHandler'] = jasmine.createSpy('addLiveUpdatesHandler');
      service['getEventsByCompetition'] = jasmine.createSpy('getEventsByCompetition').and.returnValue(of([]));
    });

    it('should set isLiveUpdatesHandlerAdded to true, call getEventsByCompetition and addLiveUpdatesHandler methods', () => {
      inplayHelperService.getSportData = jasmine.createSpy('getSportData').and.returnValue(of({
        eventsByTypeName: [{
          id: 1
        }]
      }));

      service['isLiveUpdatesHandlerAdded'] = false;

      service.getData(1, 'test', [1, 2]).subscribe(() => {
        expect(service['addLiveUpdatesHandler']).toHaveBeenCalled();
        expect(service['isLiveUpdatesHandlerAdded']).toBe(true);
        expect(service['getEventsByCompetition']).toHaveBeenCalled();
      });
    });

    it('should NOT call addLiveUpdatesHandler method and call getEventsByCompetition', () => {
      inplayHelperService.getSportData = jasmine.createSpy('getSportData').and.returnValue(of({
        eventsByTypeName: [{
          id: 1
        }]
      }));
      service['isLiveUpdatesHandlerAdded'] = true;

      service.getData(1, 'test', [1, 2]).subscribe(() => {
        expect(service['addLiveUpdatesHandler']).not.toHaveBeenCalled();
        expect(service['isLiveUpdatesHandlerAdded']).toBe(true);
        expect(service['getEventsByCompetition']).toHaveBeenCalled();
      });
    });

    it('should NOT call addLiveUpdatesHandler, getEventsByCompetition and return null observable', () => {
      inplayHelperService.getSportData = jasmine.createSpy('getSportData').and.returnValue(of([]));
      service['isLiveUpdatesHandlerAdded'] = true;

      service.getData(1, 'test', [1, 2]).subscribe((res) => {
        expect(service['addLiveUpdatesHandler']).not.toHaveBeenCalled();
        expect(service['isLiveUpdatesHandlerAdded']).toBe(true);
        expect(service['getEventsByCompetition']).not.toHaveBeenCalled();
        expect(res).toEqual(null);
      });
    });
  });

  describe('#getEventsByCompetition', () => {
    let sportData, requestConfig, newestSportEvent;

    beforeEach(() => {
      sportData = {
        eventsByTypeName: [
          {
            typeId: 1,
            typeSectionTitleAllSports: 'test1',
            eventsIds: [2]
          }
        ]
      } as any;

      requestConfig = {
        requestParams: {
          typeId: null
        },
        socket: {
          competition: 'competitionTest'
        }
      } as any;

      newestSportEvent = [{
        typeName: 'test1',
        markets: [{
          id: 1
        }]
      }];

      service['updateCommentsDataFormat'] = jasmine.createSpy('updateCommentsDataFormat');
      service['storeEventsToCache'] = jasmine.createSpy('storeEventsToCache');
    });

    it('should create competitionsLoadingObservables and call all proper methods', () => {
      const competitionEventsCustom = [
        {
          typeName: null,
          markets: [{
            id: 1
          }],
          streamProviders: 'test'
        },
        {
          typeName: null,
          markets: [{
            id: 2
          }],
          streamProviders: 'test'
        }];

      inplayHelperService.get = jasmine.createSpy('inplayHelperService').and.returnValue(of(competitionEventsCustom));
      service['extractNewestSportEvent'] = jasmine.createSpy('extractNewestSportEvent').and.returnValue(newestSportEvent);

      service.getEventsByCompetition(sportData, 'test', requestConfig, [1]).subscribe(() => {
        expect(service['extractNewestSportEvent']).toHaveBeenCalled();
        expect(service['storeEventsToCache']).toHaveBeenCalled();
        expect(inplayHelperService.subscribeForLiveUpdates).toHaveBeenCalled();
        expect(service['updateCommentsDataFormat']).toHaveBeenCalled();
      });
    });

    it('should return null', () => {
      service.getEventsByCompetition(sportData, 'test', requestConfig, [1, 2]).subscribe((event) => {
        expect(event).toEqual(null);
      });
    });

    it('should create competitionsLoadingObservables and call all proper methods expect storeEventsToCache', () => {
      const competitionEventsCustom = [
        {
          typeName: null,
          markets: [{
            id: 1
          }],
          streamProviders: 'test'
        },
        {
          typeName: null,
          markets: [{
            id: 2
          }],
          streamProviders: 'test'
        }];

      inplayHelperService.get = jasmine.createSpy('inplayHelperService').and.returnValue(of(competitionEventsCustom));
      service['extractNewestSportEvent'] = jasmine.createSpy('extractNewestSportEvent').and.returnValue([]);

      service.getEventsByCompetition(sportData, 'test', requestConfig, [1]).subscribe(() => {
        expect(service['extractNewestSportEvent']).toHaveBeenCalled();
        expect(service['storeEventsToCache']).not.toHaveBeenCalled();
        expect(inplayHelperService.subscribeForLiveUpdates).toHaveBeenCalled();
        expect(service['updateCommentsDataFormat']).toHaveBeenCalled();
      });
    });

    it('should omit events without streamProviders', () => {
      inplayHelperService.get = jasmine.createSpy('inplayHelperService').and.returnValue(of([]));
      service['extractNewestSportEvent'] = jasmine.createSpy('extractNewestSportEvent').and.returnValue(of([]));
      service.getEventsByCompetition(sportData, 'test', requestConfig, [1]).subscribe(() => {
        expect(service['extractNewestSportEvent']).toHaveBeenCalledWith([], [1]);
      });
    });
  });

  describe('#extractNewestSportEvent', () => {
    it('should return empty array', () => {
      const arr = service['extractNewestSportEvent']([]);
      expect(arr.length).toBe(0);
    });
    it('should return filtered array of events', () => {
      const arr = service['extractNewestSportEvent'](competitionEvents as any);

      expect(filtersService.orderBy).toHaveBeenCalledWith(competitionEvents, ['startTime', 'displayOrder', 'name']);

      expect(arr[0].id).toBe(5);
    });
    it('should return filtered array and remove excluded events with specified ID', () => {
      const arr = service['extractNewestSportEvent'](competitionEvents as any, [5]);
      expect(arr[0].id).toBe(6);
    });
  });


  describe('#updateCommentsDataFormat', () => {
    it('should call updater method', () => {
      service['updateCommentsDataFormat'](competitionEvents[0] as any, 'test');
      expect(commentsService.testMSInitParse).toHaveBeenCalled();
    });
    it('shouldnt call updater method', () => {
      service['updateCommentsDataFormat'](competitionEvents[0] as any, 'test2');
      expect(commentsService.testMSInitParse).not.toHaveBeenCalled();
    });
  });
});
