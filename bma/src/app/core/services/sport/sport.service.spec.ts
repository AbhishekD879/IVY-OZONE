import { SportService } from '@core/services/sport/sport.service';
import { ISportServiceConfig } from '@core/models/sport-service-config.model';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SportService', () => {
  let service: SportService;

  let eventService;
  let templateService;
  let timeService;
  let liveUpdatesWSService;
  let channelService;
  let filtersService;
  let pubSubService;

  let sportEvents;
  let sportEventsWithHandicapMarkets;
  let tabs1;
  let tabs2;

  beforeEach(() => {
    sportEvents = [{
      id: '12343',
      name: 'Football Event',
      markets: [{
        id: '345345',
        name: 'Total Goals Over/Under',
        outcomes: [{
          id: '1257',
          name: 'Eibar',
        }]
      }]
    }, {
      id: '2423',
      name: 'Real Madrid',
      markets: []
    }] as any;

    sportEventsWithHandicapMarkets = [
      {
        id: '12343',
        name: 'Football Event',
        markets: [{
          id: '345345',
          name: 'Total Goals Over/Under',
          rawHandicapValue : '1.5',
          outcomes: [{
            id: '1257',
            name: 'Eibar',
          }]
        }]
      }
    ] as any;

    tabs1 = [
      {id: 'tab-all-markets'},
      {id: 'tab-main-markets'}
    ] as any;
    tabs2 = [
      {id: 'tab-all-markets'},
      {id: 'tab-main'}
    ] as any;

    eventService = {
      getNamesOfMarketsCollection: jasmine.createSpy().and.returnValue(Promise.resolve(sportEvents)),
      getEvent: jasmine.createSpy(),
      isAnyLiveStreamAvailable: jasmine.createSpy().and.returnValue(true),
      isAnyCashoutAvailable: jasmine.createSpy().and.returnValue(true)
    };
    templateService = {
      getMarketWithSortedOutcomes: jasmine.createSpy().and.returnValue(sportEvents[0].markets[0].outcomes),
      getMarketViewType: jasmine.createSpy().and.returnValue('2-3'),
      filterBetInRunMarkets: jasmine.createSpy().and.returnValue(sportEvents[0])
    };
    timeService = {
      getSuspendAtTime: () => 1234213
    };
    liveUpdatesWSService = {};
    channelService = jasmine.createSpyObj(['getLSChannelsForCoupons', 'getLSChannels']);
    filtersService = {
      objectPromise: jasmine.createSpy().and.returnValue(Promise.resolve(sportEvents))
    };

    pubSubService = {
      publish: jasmine.createSpy('publish')
    };

    service = new SportService(
      eventService,
      templateService,
      timeService,
      liveUpdatesWSService,
      channelService,
      filtersService,
      pubSubService
    );

    service.config = {
      name: 'Football',
      request: {
        categoryId: '16'
      }
    } as any;
  });

  it('should subscribe Coupons For Updates', () => {
    const events = [] as any;
    const channel = ['sEVENT1', 'sEVENT2'];
    channelService.getLSChannelsForCoupons.and.returnValue(channel);

    service.subscribeCouponsForUpdates(events, 'football-coupons');

    expect(channelService.getLSChannelsForCoupons).toHaveBeenCalledWith(events);
    expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
      channel,
      module: 'coupon-football-coupons'
    });
  });

  it('should unsubscribe from Coupons Updates', () => {
    service.unSubscribeCouponsForUpdates('football-coupons');
    expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'coupon-football-coupons');
  });

  describe('@getByTab', () => {
    it('should use correct eventMethods', () => {
      service['todayEventsByClasses'] = jasmine.createSpy('todayEventsByClasses');
      service.config = {
        eventMethods: {
          today: 'todayEventsByClasses',
          coupons: 'coupons',
          outrights: 'outrights'
        }
      };
      service['getByTab']('today');
      expect(service['todayEventsByClasses']).toHaveBeenCalled();
    });
  });

  describe('subscribeEDPForUpdates', () => {
    it('should publish channel', () => {
      const channel = ['sEVENT1', 'sEVENT2'];
      const subscribeForScores = true;
      const eventMethods = {
        today: 'todayEventsByClasses',
        coupons: 'coupons',
        outrights: 'outrights'
      } as any;

      channelService.getLSChannels.and.returnValue(channel);
      service.subscribeEDPForUpdates(eventMethods, true);

      expect(channelService.getLSChannels).toHaveBeenCalledWith(eventMethods, true, subscribeForScores);
      expect(pubSubService['publish']).toHaveBeenCalledWith('SUBSCRIBE_LS', {
        channel,
        module: 'edp'
      });
    });

    it('should pubsub publish to have been called', () => {
      const eventMethods = {
        today: 'todayEventsByClasses',
      } as any;

      service.subscribeEDPForUpdates(eventMethods);

      expect(pubSubService['publish']).toHaveBeenCalled();
    });

    it('unSubscribeEDPForUpdates publish to have been called', () => {
      service.unSubscribeEDPForUpdates();

      expect(pubSubService['publish']).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'edp');
    });
  });

  describe('getConfig and getSports', () => {

    it('getConfig should return config', () => {
      const config = {
        eventMethods: {
          today: 'todayEventsByClasses',
          coupons: 'coupons',
          outrights: 'outrights'
        }
      };
      service.config = config;

      const result = service.getConfig();

      expect(result).toBe(config);
    });

    it('getSport should return this', () => {
      const result = service.getSport();
      expect(result).toEqual(service);
    });

  });

  describe('isDisplayAndFilterCorrect', () => {

    it('isDisplayAndFilterCorrect should be filtered config', () => {
      const tabs = [{
          id: 'gray-hounds'
        },
        {
          id: 'gaelic-football'
        }] as any;

      const result = service.isDisplayAndFilterCorrect(tabs, 'football', ['filters'], 'selected');

      expect(result).toBe(false);
    });

    it('isDisplayAndFilterCorrect should not filtered config', () => {
      const tabs = [{
          id: 'gray-hounds'
        },
        {
          id: 'gaelic-football'
        }] as any;

      const result = service.isDisplayAndFilterCorrect(tabs, 'football');

      expect(result).toBe(true);
    });

  });

  describe('getLiveStreamGroups', () => {
    it('should return liveStreamAvailable for FR flag', () => {
      const className = [{
        UK: {
          name: 'test',
          typeDisplayOrder: 11,
          cashoutAvail: true
        },
        FR: {
          name: 'test2',
          typeDisplayOrder: 11,
          cashoutAvail: false
        }},
      ] as any;
      const groupedRacing = {
        ['key']: {
        flag: 0,
        data: [{
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId',
          categoryName: 'categoryName',
          displayOrder: 11,
          name: 'test'
        }]
        }
      } as any;
      jasmine.createSpy(eventService.isAnyLiveStreamAvailable).and.returnValue(true);

      const result = service['getLiveStreamGroups'](className, groupedRacing);

      expect(result[0].UK).toEqual({
        name: 'test',
        typeDisplayOrder: 11,
        cashoutAvail: true,
        liveStreamAvailable: true
      } as any);
    });

    it('should check else path without classType', () => {
      const className = [{
        UK: {
          name: 'test',
          typeDisplayOrder: 11,
          cashoutAvail: true
        },
        FR: {
          name: 'test2',
          typeDisplayOrder: 11,
          cashoutAvail: false
        }},
      ] as any;
      const groupedRacing = {} as any;
      jasmine.createSpy(eventService.isAnyLiveStreamAvailable).and.returnValue(true);

      const result = service['getLiveStreamGroups'](className, groupedRacing);

      expect(result[0].FR).toEqual({
        cashoutAvail: false,
        name: 'test2',
        typeDisplayOrder: 11
      } as any);
    });

    it('should return liveStreamAvailable for FR flag', () => {
      const className = [{
        UK: {
          name: 'test',
          typeDisplayOrder: 11,
          cashoutAvail: true
        },
        FR: {
          name: 'UkTestName',
          typeDisplayOrder: 22,
          cashoutAvail: false
        }},
      ] as any;
      const groupedRacing = {
        ['key']: {
        flag: 0,
        data: [{
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId',
          categoryName: 'categoryName',
          displayOrder: 11,
          name: 'name',
          typeName: 'UkTestName'
        }]
        }
      } as any;
      jasmine.createSpy(eventService.isAnyLiveStreamAvailable).and.returnValue(true);

      const result = service['getLiveStreamGroups'](className, groupedRacing);

      expect(result[0].FR).toEqual({
        name: 'UkTestName',
        typeDisplayOrder: 22,
        cashoutAvail: false,
        liveStreamAvailable: true
      } as any);
    });


    it('should check  if else path', () => {
      const className = [{
        UK: {
          name: 'test',
        },
        FR: {
          name: 'test2'
        }},
      ] as any;
      const groupedRacing = {
        ['key']: {
          flag: 'flag',
          data: [{
            cashoutAvail: 'cashoutAvail'
          }]
        }
      } as any;

      const result = service['getCashoutAvailGroups'](className, groupedRacing);

      expect(result[0].UK).toEqual({name: 'test'} as any);
    });
  });

  describe('getCashoutAvailGroups', () => {

    it('should return liveStreamAvailable for FR flag', () => {
      const className = [{
        UK: {
          name: 'test',
          typeDisplayOrder: 11,
          cashoutAvail: true
        },
        FR: {
          name: 'test2',
          typeDisplayOrder: 11,
          cashoutAvail: false
        }},
      ] as any;
      const groupedRacing = {
        ['key']: {
        flag: 0,
        data: [{
          cashoutAvail: 'cashoutAvail',
          categoryCode: 'categoryCode',
          categoryId: 'categoryId',
          categoryName: 'categoryName',
          displayOrder: 11,
          typeDisplayOrder: 'typeDisplayOrder',
          name: 'test'
        }]
        }
      } as any;
      jasmine.createSpy(eventService.isAnyCashoutAvailable).and.returnValue(true);

      const result = service['getCashoutAvailGroups'](className, groupedRacing);

      expect(result[0].UK).toEqual({
        name: 'test',
        typeDisplayOrder: Infinity,
        cashoutAvail: true
      } as any);
    });

    it('should check else path', () => {
      const className = [{
        UK: {
          name: 'test',
        },
        FR: {
          name: 'test2'
        }},
      ] as any;
      const groupedRacing = {
        ['key']: {
        flag: 'flag',
        data: [{
          cashoutAvail: 'cashoutAvail'
        }]
        }
      } as any;

      const result = service['getCashoutAvailGroups'](className, groupedRacing);

      expect(result[0].UK).toEqual({name: 'test'} as any);
    });

  });

  describe('filterEmptyMarkets', () => {
    it('filterEmptyMarkets return promise resolve', () => {
      const events = [{
        markets: [
          {
            outcomes: 'outcomes'
          },
          {
            outcomes: 'testName'
          }
        ],
        date: 'specials',
        suspendAtTime: 1234213
      }];
      const result: any = service['filterEmptyMarkets'](events as any);
      expect(result[0].suspendAtTime).toEqual(1234213);
    });
    it('filters undisplayed markets and returns event', ()=>{
      const events = [{
        markets: [
          {
            isDisplayed: false,
            outcomes: 'outcomes'
          },
          {
            isDisplayed: true,
            outcomes: 'testName'
          }
        ],
        date: 'specials',
        suspendAtTime: 1234213
      }];
      const result: any = service['filterEmptyMarkets'](events as any, true);
      expect(result[0].markets.length).toEqual(1);
    });
  });

  it('getEvent: get event', () => {
    service['getEvent']('123', false, false);
    expect(eventService.getEvent).toHaveBeenCalledWith('123', {}, true, false, false);

    service.config.eventRequest = { data: [] };
    service['getEvent']('456', true, true);
    expect(eventService.getEvent).toHaveBeenCalledWith('456', { data: [] }, true, true, true);
  });

  it('checkEventMarkets: check events market', () => {
    service['checkEventMarkets'](sportEvents);
    expect(templateService.filterBetInRunMarkets).toHaveBeenCalledWith(sportEvents);
    expect(service['checkEventMarkets']([])).toEqual([]);
  });

  it('should check default tab correctness', () => {
    expect(service['isMarketTabCorrect'](tabs1, 'main-markets')).toBeTruthy();
    expect(service['isMarketTabCorrect'](tabs2, 'main-markets')).toBeTruthy();
  });

  it('#setConfig should set config and readonlyRequestConfig', () => {
    const config = {
      request : {
        categoryId: '161'
      }
    } as ISportServiceConfig;

    const result = service.setConfig(config);

    expect(result).toEqual(service);
    expect(service.config).toEqual( {
      request : {
        categoryId: '161'
      }
    });
    expect(service.readonlyRequestConfig).toEqual({categoryId: '161'});
  });

  it('#setConfig should not set config and readonlyRequestConfig', () => {
    const config = null;
    const result = service.setConfig(config);

    expect(result).toEqual(service);
    expect(service.config).toEqual({
      name: 'Football',
      request: {
        categoryId: '16'
      }
    });
    expect(service.readonlyRequestConfig).toBeUndefined();
  });

  describe('extendRequestConfig', () => {
    it('should extend upcoming tab request with "antepost" date condition if it is not tier 1 or 2 sports', () => {
      service.config = {};
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('upcoming');
      expect(extendedRequest).toEqual(({
        date: 'antepost',
        suspendAtTime: 1234213
      }) as any);
    });

    it('should extend upcoming tab request with "testDate"', () => {
      service.config = {};
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('testDate');
      expect(extendedRequest).toEqual(({
        date: 'testDate',
        suspendAtTime: 1234213
      }) as any);
    });

    it('should extend upcoming tab request with "pre48h" date condition if it is tier 1 sports', () => {
      service.config = {
        tier: 1
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('upcoming');
      expect(extendedRequest).toEqual(({
        date: 'pre48h',
        suspendAtTime: 1234213
      }) as any);
    });
    it('should extend upcoming tab request with "pre48h" date condition if it is tier 2 sports', () => {
      service.config = {
        tier: 2
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('upcoming');
      expect(extendedRequest).toEqual(({
        date: 'pre48h',
        suspendAtTime: 1234213
      }) as any);
    });
    it('should extend upcoming tab request with "antepost" date condition if it is tier 3 sports', () => {
      service.config = {
        tier: 3
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('upcoming');
      expect(extendedRequest).toEqual(({
        date: 'antepost',
        suspendAtTime: 1234213
      }) as any);
    });
    it('should extend today tab request with today date condition', () => {
      service.config = {};
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('today');
      expect(extendedRequest).toEqual(({
        date: 'today',
        suspendAtTime: 1234213
      }) as any);
    });
    it('should extend today tab request with today date condition', () => {
      service.config = {
        tabs: {
          today: {}
        }
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('today');
      expect(extendedRequest).toEqual(({
        date: 'today',
        suspendAtTime: 1234213
      }) as any);
    });
    it('should extend outrights tab request', () => {
      service.config = {
        tabs: {
          outrights: {}
        }
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('outrights');
      expect(extendedRequest).toEqual(({
        date: 'outrights',
        suspendAtTime: 1234213,
        limitOutcomesCount: 1,
        limitMarketCount: 1
      }) as any);
    });
    it('should extend specials tab request', () => {
      service.config = {
        tabs: {
          outrights: {}
        }
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('specials');
      expect(extendedRequest).toEqual(({
        date: 'specials',
        suspendAtTime: 1234213,
        limitOutcomesCount: 2
      }) as any);
    });
    it('should extend antepost tab request', () => {
      service.config = {
        tabs: {
          outrights: {}
        }
      };
      service.readonlyRequestConfig = {};
      const extendedRequest = service.extendRequestConfig('antepost');
      expect(extendedRequest).toEqual(({
        date: 'antepost',
        suspendAtTime: 1234213
      }) as any);
    });

    it('should extend upcoming tab request with "antepost" date condition if it is not tier 1 or 2 sports', () => {
      service.config = {};
      service.readonlyRequestConfig = {categoryId : '18'};
      const extendedRequest = service.extendRequestConfig('upcoming');
      expect(extendedRequest).toEqual(({
        categoryId: "18",
        date: 'allEvents',
        suspendAtTime: 1234213,
      }) as any);
      const extendedRequestMatchesTab = service.extendRequestConfig('matchesTab');
      expect(extendedRequestMatchesTab).toEqual(({
        categoryId: "18",
        date: 'matchesTab',
        suspendAtTime: 1234213,
        isNotStarted: true
      }) as any);
      const extendedRequestAllEvents = service.extendRequestConfig('allEvents');
    });
  });

  it('should return scoreboard config', () => {
    service.config.scoreboardConfig = {};
    expect(service.getScoreboardConfig()).toBe(service.config.scoreboardConfig);
  });

  describe('initMarketsByCollection', () => {
    it('initMarketsByCollection: init market by collection and sort outcomes', () => {
      const reqEvents = [{
        id: '12343',
        name: 'Football Event',
        markets: [{
          id: '345345',
          name: 'Total Goals Over/Under',
          collectionIds: '12343, 123, test ',
          outcomes: [{
            id: '1257',
            name: 'Eibar',
          }]
        }]
      }, {
        id: '2423',
        name: 'Real Madrid',
        markets: []
      }] as any;
      const namesOfMarketsCollection = [{id: '12343', name: 'Main Markets'}];

      service['initMarketsByCollection'](reqEvents, namesOfMarketsCollection, service.config, true);
      expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalled();
    });


    it('initMarketsByCollection: should check else path', () => {
      const reqEvents = [{
        id: '12343',
        name: 'Football Event',
        markets: [{
          id: '345345',
          name: 'Total Goals Over/Under',
          collectionIds: '12343, 123, test ',
          outcomes: [{
            id: '1257',
            name: 'Eibar',
          }]
        }]
      }, {
        id: '2423',
        name: 'Real Madrid',
        markets: []
      }] as any;
      const namesOfMarketsCollection = [{id: '12343', name: 'Main Markets', markets: ['1']}] as any;

      service['initMarketsByCollection'](reqEvents, namesOfMarketsCollection, service.config, true);
      expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalled();
    });
  });

  describe('getById', () => {
    it('get event by id', fakeAsync(() => {
      service['getEvent'] = jasmine.createSpy('service.getEvent').and.returnValue((Promise.resolve([])));
      service['initMarketsByCollection'] = jasmine.createSpy('service.getEvent').and.returnValue([]);

      service.getById('123', true, true, false).subscribe((data) => {
        expect(data).toBeDefined();
        expect(service['getEvent']).toHaveBeenCalledWith('123', true, false);
        expect(eventService.getNamesOfMarketsCollection).toHaveBeenCalledWith(16);
      });
      tick();

      service.getById('456', false, false, false).subscribe((data) => {
        expect(data).toBeDefined();
        expect(service['getEvent']).toHaveBeenCalledWith('456', false, false);
        expect(eventService.getNamesOfMarketsCollection).toHaveBeenCalledWith(16);
      });
      tick();
    }));

    it('catching errors from getNamesOfMarketsCollection', fakeAsync(() => {
      service['getEvent'] = jasmine.createSpy('service.getEvent').and.returnValue((Promise.resolve([])));
      service['initMarketsByCollection'] = jasmine.createSpy('service.getEvent').and.returnValue([]);
      eventService.getNamesOfMarketsCollection.and.returnValue(Promise.reject('error'));

      service.getById('456', false, false).subscribe(() => {}, (err) => {
        expect(err).toBe('error');
      });
      tick();
    }));

    it('catching errors from getEvent', fakeAsync(() => {
      service['getEvent'] = jasmine.createSpy('service.getEvent').and.returnValue(Promise.reject('error'));

      service.getById('456', false, false).subscribe(() => {}, (err) => {
        expect(err).toBe('error');
      });
      tick();
    }));
  });

  it('initMarketsByCollection: get market by collection and sort outcomes', () => {
    service['initMarketsByCollection'](sportEvents, sportEvents, service.config);
    expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalled();
  });

  it('initMarketsByCollection: get market by collection and do not sort outcomes', () => {
    service['initMarketsByCollection'](sportEvents, sportEvents, service.config, false);
    expect(templateService.getMarketWithSortedOutcomes).not.toHaveBeenCalled();
  });

  it('initMarketsByCollection: get market by collection with empty events', () => {
    expect(service['initMarketsByCollection']([], [], service.config, false)).toEqual([]);
  });

  it('initMarketsByCollection: should set viewType for market', () => {
    const namesOfMarketsCollection = [{id: '12343', name: 'Main Markets', markets: ['1']}] as any;

    service['initMarketsByCollection'](sportEvents, namesOfMarketsCollection, service.config);
    expect(templateService.getMarketViewType).toHaveBeenCalledWith(sportEvents[0].markets[0], 'Football');
    expect(sportEvents[0].markets[0].viewType).toEqual('2-3');
  });

  it('initMarketsByCollection: should set viewType for Handicap market market', () => {
    service['initMarketsByCollection'](sportEventsWithHandicapMarkets, sportEvents, service.config);
    expect(sportEventsWithHandicapMarkets[0].markets[0].viewType).toEqual('2-3');
    expect(templateService.getMarketViewType).toHaveBeenCalledWith(sportEventsWithHandicapMarkets[0].markets[0], null);
    expect(templateService.getMarketWithSortedOutcomes).toHaveBeenCalledWith(sportEventsWithHandicapMarkets[0].markets[0], null);
  });

  it('initMarketsByCollection: should not set viewType for market without outcomes', () => {
    const sportEventsWithoutOutcomes = [{
      id: '12343',
      name: 'Football Event',
      markets: [{
        id: '345345',
        name: 'Total Goals Over/Under',
        outcomes: []
      }]
    }, {
      id: '2423',
      name: 'Real Madrid',
      markets: []
    }] as any;

    service['initMarketsByCollection'](sportEventsWithoutOutcomes, sportEvents, service.config);
    expect(templateService.getMarketViewType).toHaveBeenCalled();
    expect(templateService.getMarketWithSortedOutcomes).not.toHaveBeenCalled();
  });

  it('initMarketsByCollection: should not set viewType for market without outcomes array', () => {
    const sportEventsWithoutOutcomes = [{
      id: '12343',
      name: 'Football Event',
      markets: [{
        id: '345345',
        name: 'Total Goals Over/Under',
      }]
    }, {
      id: '2423',
      name: 'Real Madrid',
      markets: []
    }] as any;

    service['initMarketsByCollection'](sportEventsWithoutOutcomes, sportEvents, service.config);
    expect(templateService.getMarketViewType).toHaveBeenCalled();
    expect(templateService.getMarketWithSortedOutcomes).not.toHaveBeenCalled();
  });
});
