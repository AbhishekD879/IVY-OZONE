import { GamingService } from '@core/services/sport/gaming.service';
import { fakeAsync } from '@angular/core/testing';
import { of } from 'rxjs';
import { OUTRIGHTS_CONFIG } from '@app/core/constants/outrights-config.constant';

describe('GamingService', () => {
  let service: GamingService;

  let eventService;
  let templateService;
  let timeService;
  let liveUpdatesWSService;
  let channelService;
  let filtersService;
  let outcomeTemplateHelper;
  let cmsService;
  let commandService;
  let routingHelperService;
  let pubSubService;
  const isMobileOnly: boolean = false

  const couponsEvents = [{
    coupon: {
      id: '4',
      displayOrder: 4,
      name: 'Coupon Cashout'
    }
  }, {
    coupon: {
      id: '1',
      displayOrder: 1,
      name: 'Coupon-1809-Weekend'
    }
  }, {
    coupon: {
      id: '2',
      displayOrder: 3,
      name: 'Goalscorer Coupon'
    }
  }, {
    coupon: {
      id: '3',
      displayOrder: 2,
      name: 'Test Coupon'
    }
  }] as any;

  const sportEvents = [{
    id: '12343',
    typeId: 'type1',
    name: 'Football Event',
    markets: [{
      id: '345345',
      name: 'Total Goals Over/Under',
      templateMarketName: 'market template 1',
      outcomes: [{
        id: '1257',
        name: 'Eibar',
      }]
    }]
  }, {
    typeId: 'type1',
    id: '2423',
    name: 'Real Madrid',
    markets: []
  }] as any;

  const outrightsEvents = [{
    id: '123456',
    typeId: 'type1',
    name: 'Outright Event',
    eventSortCode: 'TNMT',
    markets: [{
      id: '345345',
      name: 'Outright',
      templateMarketName: 'Outright',
      outcomes: [{
        id: '1257',
        name: 'Eibar',
      }]
    }]
  }, {
      id: '1234567',
      typeId: 'type2',
      name: 'Outright Event 2',
      eventSortCode: 'TNMT',
      startTime: '2020-03-08T22:04:00',
      markets: [{
        id: '123',
        name: 'Outright2',
        templateMarketName: 'Outright2',
        outcomes: [{
          id: '12567',
          name: 'Otherone',
        }]
      }]
    }
  ] as any;

  const coupons = [{
    displayOrder: 1,
    id: '1',
    name: 'Coupon-1809-Weekend'
  }, {
    displayOrder: 2,
    id: '3',
    name: 'Test Coupon'
  }, {
    displayOrder: 3,
    enableCouponNewBadge: true,
    id: '2',
    name: 'Goalscorer Coupon'
  }, {
    id: '4',
    displayOrder: 4,
    name: 'Coupon Cashout'
  }] as any;

  beforeEach(() => {
    eventService = {
      getNamesOfMarketsCollection: jasmine.createSpy().and.returnValue(Promise.resolve(sportEvents)),
      getEvent: jasmine.createSpy(),
      couponEventsByCouponId: jasmine.createSpy().and.callFake(() => of([])),
      couponsList: jasmine.createSpy().and.returnValues(Promise.resolve(couponsEvents)),
      getFootballJackpotList: jasmine.createSpy(),
      eventsByClasses: jasmine.createSpy('eventsByClasses').and.returnValue(Promise.resolve(sportEvents)),
    };
    templateService = {
      getMarketWithSortedOutcomes: jasmine.createSpy().and.returnValue(sportEvents[0].markets[0].outcomes),
      getMarketViewType: jasmine.createSpy().and.returnValue('2-3'),
      filterBetInRunMarkets: jasmine.createSpy().and.returnValue(sportEvents[0]),
      getEventCorectedDays: jasmine.createSpy().and.returnValue('today'),
      getEventCorectedDay: jasmine.createSpy().and.returnValue('today'),
      filterMultiplesEvents: jasmine.createSpy('filterMultiplesEvents')
    };
    timeService = {
      createTimeRange: jasmine.createSpy().and.returnValue({ startDate: '2019-03-10T22:00:00.000Z' }),
      getSuspendAtTime: jasmine.createSpy('getSuspendAtTime').and.returnValue('2019-03-11T13:37:30.000Z'),
      reduceByCurrentTime: jasmine.createSpy('reduceByCurrentTime')
    };
    liveUpdatesWSService = {
      subscribe: jasmine.createSpy('subscribeLSWS').and.callFake((channels, module) => module),
      unsubscribe: jasmine.createSpy('unsubscribeLsWs')
    };
    channelService = {
      getLSChannelsForCoupons: jasmine.createSpy('getLSChannelsForCoupons'),
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray'),
      getEventsChildsLiveChannels: jasmine.createSpy('getEventsChildsLiveChannels').and.returnValue([])
    };
    filtersService = {
      objectPromise: jasmine.createSpy().and.returnValue(Promise.resolve(sportEvents)),
      orderBy: () => sportEvents
    };
    outcomeTemplateHelper = {
      setOutcomeMeaningMinorCode: jasmine.createSpy('setOutcomeMeaningMinorCode')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        FootballCouponsNewBadge: {
          couponName: 'Goalscorer Coupon',
          enableCouponNewBadge: true
        }
      } as any))
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        EVENT_COUNT_UPDATE: 'EVENT_COUNT_UPDATE'
      }
    };

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      execute: jasmine.createSpy('execute'),
      API: {
        GET_YC_TAB: 'GET_YC_TAB',
        GET_5ASIDE_TAB: 'GET_5ASIDE_TAB'
      }
    };

    service = new GamingService(
      eventService,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      outcomeTemplateHelper,
      cmsService,
      commandService,
      routingHelperService,
      pubSubService
    );

    service.config = {
      name: 'Football',
      request: {
        categoryId: '16'
      }
    } as any;
  });

  it('should create service', () => {
    expect(service).toBeTruthy();
  });

  describe('@couponEventsRequestParams', () => {
    it('it should create request params for Coupon Events', () => {
      service.config = {
        request: {
          categoryId: '16',
          siteChannels: 'M',
          date: 'today'
        }
      };
      const result = service.couponEventsRequestParams('442');
      expect(result).toEqual({
        categoryId: '16',
        siteChannels: 'M',
        isNotStarted: true,
        startTime: '2019-03-10T22:00:00.000Z',
        suspendAtTime: '2019-03-11T13:37:30.000Z',
        childCount: true
      } as any);
    });
    it('it should create request params for Coupon Events with type id filter', () => {
      service.config = {
        request: {
          categoryId: '16',
          siteChannels: 'M',
          date: 'today'
        }
      };
      const result = service.couponEventsRequestParams('442');
      expect(result).toEqual({
        categoryId: '16',
        siteChannels: 'M',
        isNotStarted: true,
        startTime: '2019-03-10T22:00:00.000Z',
        suspendAtTime: '2019-03-11T13:37:30.000Z',
        childCount: true
      }as any, '10');
    });

    it('it should  return typeIds', () => {
      service.config = {
        request: {
          categoryId: '16',
          siteChannels: 'M',
          marketsCount: true,
          date: 'today'
        }
      };
      const resultIds = {
        typeIdCodes: '442,25230,25231,25232,696,678,435,440,441,437,434,438,971,975,967,' +
          '472,468,734,728,735,500,501,504,929,927,930,928,823,1024'
      };
      const result = service.couponEventsRequestParams('193');
      expect(result).toEqual({
        categoryId: '16',
        siteChannels: 'M',
        isNotStarted: true,
        startTime: '2019-03-10T22:00:00.000Z',
        suspendAtTime: '2019-03-11T13:37:30.000Z',
        childCount: true,
        typeIdCodes: '442,25230,25231,25232,696,678,435,440,441,437,434,438,971,975,967,' +
          '472,468,734,728,735,500,501,504,929,927,930,928,823,1024'
      } as any, resultIds);
    });
  });

  describe('@couponEventsByCouponId', () => {
    it('should set correctedOutcomeMeaningMinorCode to outcomes', fakeAsync(() => {
      spyOn(service['filtersService'], 'orderBy');
      eventService.couponEventsByCouponId.and.returnValue(Promise.resolve(sportEvents));
      service.couponEventsByCouponId({} as any).then(() => {
        expect(outcomeTemplateHelper.setOutcomeMeaningMinorCode).toHaveBeenCalled();
        expect(filtersService.orderBy).toHaveBeenCalled();
      });
    }));
  });

  describe('competitionsInitClassIds', () => {
    it('should return observable', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      const result: any = service.competitionsInitClassIds();
      result.subscribe(res => {
        expect(res).toEqual({});
      });
    }));

    it('should return promise', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      const result: any = service.competitionsInitClassIds();
      result.subscribe(res => {
        expect(res).toEqual({});
      });
    }));
  });

  describe('todayEventsByClasses', () => {
    it('should return', fakeAsync(() => {
      service['eventFactory'].eventsByClasses = jasmine.createSpy().and.callFake((p1) => {
        return Promise.resolve([p1]);
      });
      service.config = {
        request: 'req'
      } as any;
      service.todayEventsByClasses().then((result) => {
        expect(result).toEqual(['req'] as any);
      });
    }));
  });


  describe('jackpot and results', () => {
    it('should return obj promise', fakeAsync(() => {
      service['eventFactory'].getFootballJackpotList = jasmine.createSpy().and.callFake(() => {
        return Promise.resolve({});
      });
      service.jackpot().then((result) => {
        expect(result).toEqual({} as any);
      });
    }));

    it('should return promise resolve', fakeAsync(() => {
      service.results().then((result) => {
        expect(result).toEqual([]);
      });
    }));
  });

  describe('#createNewInstance', () => {
    it('should check createNewInstance instance', () => {
      expect(service.createNewInstance() instanceof GamingService).toBeTruthy();
    });
  });

  describe('addToCollections', () => {
    it('collection market should be empty', () => {
      const collections: any = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'Tab name 1',
        marketName: 'Marker1'
      }];
      const market: any = {
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        new: true
      };
      service['addToCollections'](market, collections);
      expect(service['addToCollections']).toBeTruthy();
    });
  });

  describe('getCollectionsTabs', () => {

    it('should check createNewInstance instance', () => {
      const EDP_MARKETS: any = [{
        sortOrder: 1,
        name: 'Marker1',
        lastItem: false,
      }, {
        sortOrder: 2,
        name: 'Marker2',
        lastItem: true,
      }];
      const collections: any = [{
        displayOrder: 2,
        id: 'tab-id1',
        markets: [],
        name: 'Tab name 1',
        marketName: 'Marker1'
      }, {
        displayOrder: 1,
        id: 'tab-id2',
        markets: [],
        name: 'Tab name 2',
        marketName: 'Marker2'
      }];
      const eventsListMock: any = [
        {
          typeId: 664,
          markets: [
            {
              name: 'draw no bet'
            }
          ]
        }
      ];
      spyOn(service,'getSortingFromCms');
      service.getCollectionsTabs(collections, eventsListMock, EDP_MARKETS, isMobileOnly);
      expect(service.getSortingFromCms).toHaveBeenCalledWith([], EDP_MARKETS, eventsListMock, isMobileOnly);
    });
  });

  describe('subscribeForUpdates', () => {
    it(`should subscribe on subscribeForUpdates`, () => {
      const channel = ['sEVENT1'];
      channelService.getLSChannelsFromArray.and.returnValue(channel);
      service.subscribeLPForUpdates(sportEvents);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(sportEvents);
      expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
        channel,
        module: 'sb'
      });
    });
  });

  it('should unSubscribeLPForUpdates', () => {
    service.unSubscribeLPForUpdates();
    expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'sb');
  });

  describe('#getSortingFromCms', () => {
    it('should return sorted tabs', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        markets: [],
        name: 'Tab name 1',
        marketName: 'Marker1'
      }, {
          displayOrder: 1,
          id: 'tab-id2',
          markets: [],
          name: 'Tab name 2',
          marketName: 'Marker2'
        }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, isMobileOnly as any);

      expect(result).toEqual([
        { id: 'tab-Marker1', marketName: 'Marker1', label: 'Tab name 1',
        url: '/event/123123/Marker1', isFiveASideNewIconAvailable: undefined, index: 2 },
        { id: 'tab-Marker2', marketName: 'Marker2', label: 'Tab name 2',
        url: '/event/123123/Marker2', isFiveASideNewIconAvailable: undefined, index: 2 }
      ]);
    });


    it('should return sorted tabs for mobile when EDP markets are empty', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        markets: [],
        name: 'All Markets',
        marketName: 'Marker1'
      }, {
          displayOrder: 1,
          id: 'tab-id2',
          markets: [],
          name: 'All Markets',
          marketName: 'Marker2'
        }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, true);


      expect(result).toEqual([
        { id: 'tab-Marker1', marketName: 'Marker1', label: 'Markets', isFiveASideNewIconAvailable: undefined, url: '/event/123123/Marker1', index: 2, pills: [  ]  },
        {  id: 'tab-Marker2', marketName: 'Marker2', label: 'All Markets', isFiveASideNewIconAvailable: undefined, url: '/event/123123/Marker2', index: 2  }
      ]);
    });

    it('should return sorted tabs with EDP_MARKETS ', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'Marker1',
        lastItem: false,
        markets: []
      }, {
        sortOrder: 2,
        name: 'Marker2',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'Tab name 1',
        marketName: 'Marker1'
      }, {
        displayOrder: 1,
        id: 'tab-id2',
        name: 'Tab name 2',
        marketName: 'Marker2'
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, isMobileOnly as any);

      expect(result).toEqual([
        { id: 'tab-Marker1', marketName: 'Marker1', label: 'Tab name 1',
          url: '/event/123123/Marker1', isFiveASideNewIconAvailable: undefined, index: 2 },
        { id: 'tab-Marker2', marketName: 'Marker2', label: 'Tab name 2',
          url: '/event/123123/Marker2', isFiveASideNewIconAvailable: undefined, index: 2 }
      ]);
    });

    it('should return sorted tabs with EDP_MARKETS mobile', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'All Markets',
        lastItem: false,
        markets: []
      }, {
        sortOrder: 2,
        name: 'All Markets',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'All Markets',
        marketName: 'Marker1'
      }, {
        displayOrder: 1,
        id: 'tab-id2',
        name: 'Specials',
        marketName: 'Marker2'
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, true);

      expect(result).toEqual([
        {id: 'tab-Marker1', marketName: 'Marker1', label: 'Markets', isFiveASideNewIconAvailable: undefined, url: '/event/123123/Marker1', index: 0, pills: [ ]  },
        { id: 'tab-Marker2', marketName: 'Marker2', label: 'Specials',
          url: '/event/123123/Marker2', isFiveASideNewIconAvailable: undefined, index: 2 }
      ]);
    });

    it('should return sorted tabs with collectionIndex ', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'Tab name 1',
        lastItem: false,
        markets: []
      }, {
        sortOrder: 2,
        name: 'Marker2',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'Tab name 1'
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, isMobileOnly as any);

      expect(result).toEqual([
        { id: 'tab-tab-name-1', index: 0, isFiveASideNewIconAvailable: undefined, label: 'Tab name 1',
          marketName: 'tab-name-1', url: '/event/123123/tab-name-1' }
      ]);
    });

    it('should return sorted tabs with collectionIndex for EDP for mobile', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'Tab name 1',
        lastItem: false,
        markets: []
      }, {
        sortOrder: 2,
        name: 'Marker2',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 1,
        id: 'tab-all-markets',
        name: 'All Markets',
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, true);
      
      expect(result).toEqual([
        {
          id: "tab-all-markets",
          isFiveASideNewIconAvailable: undefined,
          marketName: "all-markets",
          label: "Markets",
          url: "/event/123123/all-markets",
          index: 2,
          pills: [
              {
                  marketName: "all-markets",
                  active: false,
                  label: "All Markets",
                  index: 2
              }
          ]
      }
      ]);
    });

    it('should return sorted tabs with collectionIndex for mobile', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'Marker1',
        lastItem: false,
        markets: []
      }, {
        sortOrder: 2,
        name: 'Marker2',
        lastItem: false,
        markets: []
      },
      {
        sortOrder: 3,
        name: 'Marker3',
        lastItem: true,
        markets: []
      }
    ];
      const collections = [{
        displayOrder: 1,
        id: 'tab-id1',
        name: 'Marker1'
      },
      {
        displayOrder: 2,
        id: 'tab-id1',
        name: 'All Markets'
      },
    {
      displayOrder: 3,
      id: 'tab-id2',
      name: 'Marker4'
    },
    {
      dispalyOrder: 4,
      name: 'Marker3',
      id: 'tab-id3',
    }
  ];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, true);

      expect(result).toEqual([
        {
          id: "tab-all-markets",
          isFiveASideNewIconAvailable: undefined,
          marketName: "all-markets",
          label: "Markets",
          url: "/event/123123/all-markets",
          index: 4,
          pills: [
            {
              marketName: "marker1",
              active: false,
              label: "Marker1",
              index: 0
          },
          {
              marketName: "all-markets",
              active: false,
              label: "All Markets",
              index: 4
          },
          {
              marketName: "marker4",
              active: false,
              label: "Marker4",
              index: 4
          },
          {
              marketName: "marker3",
              active: false,
              label: "Marker3",
              index: 5
          }
          ]
      }
      ]);
    });

    it('should return sorted tabs with arrayLength + 1 ', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'Tab name 1',
        lastItem: true,
        markets: []
      }, {
        sortOrder: 2,
        name: 'Tab name 2',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'Tab name 1'
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, isMobileOnly as any);

      expect(result).toEqual([
        { id: 'tab-tab-name-1', index: 3, isFiveASideNewIconAvailable: undefined, label: 'Tab name 1',
          marketName: 'tab-name-1', url: '/event/123123/tab-name-1' }
      ]);
    });

    it('should return sorted tabs with arrayLength + 1 for mobile', () => {
      routingHelperService.formEdpUrl.and.returnValue('event/123123');
      const EDP_MARKETS = [{
        sortOrder: 1,
        name: 'All Markets',
        lastItem: true,
        markets: []
      }, {
        sortOrder: 2,
        name: 'All Markets',
        lastItem: true,
        markets: []
      }];
      const collections = [{
        displayOrder: 2,
        id: 'tab-id1',
        name: 'All Markets'
      },
      {
        displayOrder: 2,
        id: 'tab-id1',
        name: 'Specials'
      }];
      const result = service.getSortingFromCms(collections as any, EDP_MARKETS as any, {} as any, true);

      expect(result).toEqual([
        { id: 'tab-all-markets', marketName: 'all-markets', label: 'Markets', isFiveASideNewIconAvailable: undefined, url: '/event/123123/all-markets', index: 3, pills: [ Object({ marketName: 'specials', active: false, label: 'Specials', index: 2 }), 
        Object({ marketName: 'all-markets', active: false, label: 'All Markets', index: 3 }) ] }
      ]);
    });
  });

  describe('extendMarketsCollections', () => {
    it('should join collections with same name, handle no markets property ', () => {
      const collections = {
        collection: [{
          marketName: 'build-your-bet',
          name: 'Build Your Bet'
        }, {
          name: 'Goals',
          markets: []
        }, {
          name: 'Main Markets',
          markets: [{ id: '3' }, { id: '4' }]
        }, {
          name: 'Main Markets'
        }]
      } as any;
      const result = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }] as any;

      const extendResult = service.extendMarketsCollections(collections, {});
      expect(extendResult).toEqual(result);
    });

    it('should join collections with same name, handle no markets property different order', () => {
      const collections = {
        collection: [{
          marketName: 'build-your-bet',
          name: 'Build Your Bet'
        }, {
          name: 'Goals',
          markets: []
        }, {
          name: 'Main Markets'
        }, {
          name: 'Main Markets',
          markets: [{ id: '3' }, { id: '4' }]
        }]
      } as any;
      const result = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }] as any;

      const extendResult = service.extendMarketsCollections(collections, {});
      expect(extendResult).toEqual(result);
    });

    it('should join collections with same name and NOT filter Markets Collections without markets', () => {
      const collections = {
        collection: [{
          marketName: 'build-your-bet',
          name: 'Build Your Bet'
        }, {
          name: 'Goals',
          markets: []
        }, {
          name: 'Main Markets',
          markets: [{ id: '3' }, { id: '4' }]
        }, {
          name: 'Main Markets',
          markets: [{ id: '5' }]
        }]
      } as any;
      const result = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }, { id: '5' }]
      }] as any;
      expect(service.extendMarketsCollections(collections, {})).toEqual(result);
    });

    it('should join collections when isEnabledYCTab = true and  isFiveASideAvailable = true', () => {
      commandService.execute.and.returnValue({
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      });
      const collections = {
        event: [],
        collection: [{
          marketName: 'build-your-bet',
          name: 'Build Your Bet'
        }, {
          name: 'Goals',
          markets: []
        }, {
          name: 'Main Markets',
          markets: [{ id: '3' }, { id: '4' }]
        }, {
          name: 'Main Markets',
          markets: [{ id: '5' }]
        }]
      } as any;
      const result = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet',
        markets: [],
        isFiveASideNewIconAvailable: undefined
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }, { id: '5' }]
      }] as any;
      expect(service.extendMarketsCollections(collections, {
        isEnabledYCTab: true,
        isFiveASideAvailable: true,
        isActive: true
      })).toEqual(result);
    });

    it('should join collections when isEnabledYCTab = false and  isFiveASideAvailable = false', () => {
      commandService.execute.and.returnValue({
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      });
      const collections = {
        event: [],
        collection: [{
          marketName: 'build-your-bet',
          name: 'Build Your Bet'
        }, {
          name: 'Goals',
          markets: []
        }, {
          name: 'Main Markets',
          markets: [{ id: '3' }, { id: '4' }]
        }, {
          name: 'Main Markets',
          markets: [{ id: '5' }]
        }]
      } as any;
      const result = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }, { id: '5' }]
      }] as any;
      expect(service.extendMarketsCollections(collections, {
        isEnabledYCTab: false,
        isFiveASideAvailable: false
      })).toEqual(result);
    });

    it('should sort collections by displayOrder', () => {
      const collections = {
        collection: [{
          name: 'Build Your Bet',
          displayOrder: '1'
        }, {
          name: 'Goals',
          displayOrder: '3'
        }, {
          name: 'Player Markets',
          displayOrder: '1'
        }, {
          name: 'Half Markets',
          displayOrder: '2'
        }]
      } as any;

      const result = [{
        name: 'Build Your Bet',
        displayOrder: '1'
      }, {
        name: 'Player Markets',
        displayOrder: '1'
      }, {
        name: 'Half Markets',
        displayOrder: '2'
      }, {
        name: 'Goals',
        displayOrder: '3'
      }];

      expect(service.extendMarketsCollections(collections, {
        isEnabledYCTab: false,
        isFiveASideAvailable: false
      })).toEqual(result);
    });
  });

  describe('updateCollectionsWithLiveMarket', () => {
    const sportName: string = '';

    it('should not updateCollections ', () => {
      const liveMarket: any = {};
      const collections: any = [];
      const allMarkets: any = [];

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeFalsy();
    });

    it('should updateCollections and Add to Collection', () => {
      const liveMarket: any = {
        collectionIds: '1,',
        id: '222',
        outcomes: [
          {}
        ]
      };

      const collections: any = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        id: '1',
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }, {
        name: 'All Markets',
        markets: [{ id: '5' }]
      }];

      const allMarkets: any = sportEvents[0].markets;

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeTruthy();
      expect(collections[2].markets.length).toEqual(3);
    });

    it('should updateCollections and Add to Collection with Other Market', () => {
      const liveMarket: any = {
        collectionIds: '1,',
        id: '222',
        outcomes: [
          {}
        ]
      };

      const collections: any = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Other Market',
        markets: []
      }, {
        id: '1',
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }, {
        name: 'All Markets',
        markets: [{ id: '5' }]
      }];
      const allMarkets: any = sportEvents[0].markets;

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeTruthy();
      expect(collections[1].markets.length).toEqual(0);
    });

    it('should updateCollections and replace existing market', () => {
      const liveMarket: any = {
        collectionIds: '1,',
        id: '3',
        updatedParam: 'updatedParam',
        outcomes: [
          {}
        ]
      };

      const collections: any = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        id: '1',
        name: 'Main Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }, {
        name: 'All Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }];

      const allMarkets: any = sportEvents[0].markets;

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeTruthy();
      expect(collections[2].markets[0]).toEqual(liveMarket);
    });

    it('should updateCollections and replace collectionsList', () => {
      const liveMarket: any = {
        collectionIds: '1,',
        id: '3',
        updatedParam: 'updatedParam',
        outcomes: [
          {}
        ]
      };

      const collections: any = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        id: '33',
        name: 'Other Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }, {
        name: 'All Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }];

      const allMarkets: any = sportEvents[0].markets;

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeTruthy();
      expect(collections[2].markets[0]).toEqual(liveMarket);
    });

    it('should updateCollections and do not replace collectionsList', () => {
      const liveMarket: any = {
        collectionIds: '1,',
        id: '3',
        updatedParam: 'updatedParam',
        outcomes: [
          {}
        ]
      };

      const collections: any = [{
        marketName: 'build-your-bet',
        name: 'Build Your Bet'
      }, {
        name: 'Goals',
        markets: []
      }, {
        name: 'All Markets',
        markets: [{ id: '3' }, { id: '4' }]
      }];

      const allMarkets = sportEvents[0].markets;

      expect(service.updateCollectionsWithLiveMarket(liveMarket, collections, allMarkets, sportName)).toBeTruthy();
      expect(collections[2].markets[0]).not.toEqual(liveMarket);
      expect(collections[1].markets).toEqual([]);
    });
  });

  describe('arrangeEventsBySection', () => {
    it('shouldn\'t group events by date', () => {
      const groupedEvents = service.arrangeEventsBySection([...sportEvents, ...outrightsEvents], false);
      expect(((groupedEvents[0].groupedByDate) as any).length).toEqual(0);
    });

    it('should group events by date and set marketsAvailability property', () => {
      filtersService.objectPromise.and.returnValues(sportEvents, outrightsEvents);
      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValues(sportEvents, outrightsEvents);
      const groupedEvents = service.arrangeEventsBySection([...sportEvents, ...outrightsEvents], true);
      expect(groupedEvents[0].groupedByDate[0]).toBeTruthy();
      expect(groupedEvents[0].groupedByDate[0].events.length).toEqual(2);
      expect(groupedEvents[0].groupedByDate[0].title).toEqual('today');
      expect(groupedEvents[0].groupedByDate[0].marketsAvailability['total goals over/under']).toBeTruthy();
      expect(groupedEvents[0].groupedByDate[0].marketsAvailability['market template 1']).toBeTruthy();
    });

    it(`should sort eventsArray`, () => {
      spyOn(service['filtersService'], 'orderBy');

      service.arrangeEventsBySection(sportEvents, true);

      expect(service['filtersService'].orderBy).toHaveBeenCalledWith(sportEvents, [
        'startTime',
        'markets[0].outcomes[0].name',
        'displayOrder',
        'name'
      ]);
    });

    it('should group events by date and set ', () => {
      const sportsEv = sportEvents;
      sportsEv[0].markets[0].templateMarketName = '';
      sportsEv[0].markets[0].name = '';
      spyOn(filtersService, 'orderBy').and.returnValues(sportsEv, outrightsEvents);
      filtersService.objectPromise.and.returnValues(sportEvents, outrightsEvents);
      const groupedEvents = service.arrangeEventsBySection([...sportEvents, ...outrightsEvents], true);
      expect(groupedEvents[0].groupedByDate[0]).toBeTruthy();
    });
  });

  describe('#couponsList', () => {
    it('should load coupons', (done: DoneFn) => {
      filtersService['orderBy'] = jasmine.createSpy().and.returnValue(Promise.resolve(coupons));
      service.config = {
        request: {
          siteChannels: 'M',
          categoryId: '16'
        },
        tabs: {
          coupons: {
            date: 'today'
          }
        }
      };
      service.couponsList().then(data => {
        expect(timeService.createTimeRange).toHaveBeenCalledWith('today');
        expect(timeService.getSuspendAtTime).toHaveBeenCalled();
        expect(filtersService.orderBy).toHaveBeenCalledWith([{
          id: '4',
          displayOrder: 4,
          name: 'Coupon Cashout'
        }, {
          displayOrder: 1,
          id: '1',
          name: 'Coupon-1809-Weekend'
        }, {
          displayOrder: 3,
          enableCouponNewBadge: true,
          id: '2',
          name: 'Goalscorer Coupon'
        }, {
          displayOrder: 2,
          id: '3',
          name: 'Test Coupon'
        }], [ 'displayOrder', 'name' ]);
        expect(eventService.couponsList).toHaveBeenCalledTimes(1);
        expect(data).toEqual(coupons);
        done();
      });
    });
  });

  it('should re-init marketsAvailability properties', () => {
    const eventsListMock: any = [
      {
        typeId: 664,
        markets: [
          {
            templateMarketName: 'draw no bet'
          }
        ]
      },
      {
        typeId: 432,
        markets: [
          {
            templateMarketName: 'draw no bet'
          }
        ]
      }
    ];
    const sectionsMock: any = [
      {
        typeId: 664,
        groupedByDate: [
          {
            title: 'today',
            marketsAvailability: {
              'match betting': true
            }
          }
        ]
      }
    ];

    service.setMarketsAvailability(eventsListMock, sectionsMock);

    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['match betting']).toBeUndefined();
    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['draw no bet']).toBeTruthy();
  });

  it('should re-init marketsAvailability properties with market name', () => {
    const eventsListMock: any = [
      {
        typeId: 664,
        markets: [
          {
            name: 'draw no bet'
          }
        ]
      }
    ];
    const sectionsMock: any = [
      {
        typeId: 664,
        groupedByDate: [
          {
            title: 'today',
            marketsAvailability: {
              'match betting': true
            }
          }
        ]
      }
    ];

    service.setMarketsAvailability(eventsListMock, sectionsMock);

    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['match betting']).toBeUndefined();
    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['draw no bet']).toBeTruthy();
  });

  it('should re-init marketsAvailability for groups', () => {
    const eventsListMock: any = [
      {
        typeId: 664,
        markets: [
          {
            name: 'draw no bet'
          }
        ]
      }
    ];
    const sectionsMock: any = [
      {
        typeId: 664,
        groupedByDate: [
          {
            title: 'tomorrow',
            marketsAvailability: {
              'match betting': true
            }
          }
        ]
      }
    ];

    service.setMarketsAvailability(eventsListMock, sectionsMock);

    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['match betting']).toBeUndefined();
    expect(sectionsMock[0].groupedByDate[0].marketsAvailability['draw no bet']).toBeUndefined();
  });

  describe('updateCollections', () => {
    it('should update collections and handle empty collections when run updateCollections', () => {
      const marketsCollectionsArrayMock: any = [
        undefined,
        {
          markets: [{
            id: '1',
            testParam: 'testParam'
          }]
        }
      ];
      const market: any = {
        id: '1',
        testParam: 'updatedTestParam'
      };

      service['updateCollections'](market, marketsCollectionsArrayMock);

      expect(marketsCollectionsArrayMock[1].markets[0].testParam).toEqual('updatedTestParam');
    });

    it('Collections.market should be market testParam', () => {
      const marketsCollectionsArrayMock: any = [
        undefined,
        {
          markets: [{
            id: '1',
            testParam: 'testParam'
          }]
        }
      ];
      const market: any = {
        id: '0',
        testParam: 'updatedTestParam'
      };

      service['updateCollections'](market, marketsCollectionsArrayMock);

      expect(marketsCollectionsArrayMock[1].markets[0].testParam).toEqual('testParam');
    });

  });

  it('should filter out future events', () => {
    const sportEventsData = [
      { startTime: 1568894400000 },
      { startTime: 1568980800000 },
      { startTime: 1569056400000 },
      { startTime: 1569142800000 }
    ] as any;

    timeService.reduceByCurrentTime.and.returnValues(1568847600000, 1568934000000, 1569009600000, 1569096000000);
    templateService.getEventCorectedDays.and.returnValues('Today', 'Tomorrow', 'Tomorrow', '21 Sep');

    const result = service.filterOutFutureEvents(sportEventsData);
    expect(timeService.reduceByCurrentTime).toHaveBeenCalledTimes(4);
    expect(templateService.getEventCorectedDays).toHaveBeenCalledTimes(4);
    expect(result).toContain({ startTime: 1568894400000 } as any);
    expect(result).toContain({ startTime: 1568980800000 } as any);
    expect(result).toContain({ startTime: 1569056400000 } as any);
    expect(result).not.toContain({ startTime: 1569142800000 } as any);
  });

  describe('subscribeEventChildsUpdates', () => {
    it('should retrieve event childs channels and subscribe to liveServeMS', () => {
      const events = [{ id: '123', liveServChannels: 'sEVENT,' }] as any;
      const typeId = 442;

      service.subscribeEventChildsUpdates(events, typeId);

      expect(channelService.getEventsChildsLiveChannels).toHaveBeenCalledWith(events);
      expect(liveUpdatesWSService.subscribe).toHaveBeenCalledWith([], `matches-${typeId}`);
    });
  });

  describe('isAnyMarketByPattern', () => {
    it('should return true if at least one market matched the pattern', () => {
      const markets = [{
        id: '1',
        testParam: 'testParam',
        name: 'market score'
      }];
      const pattern = new RegExp('^market\\sscore$', 'i');
      const result = service.isAnyMarketByPattern(markets, pattern);

      expect(result).toEqual(true);
    });

    it('should return false if no market matched the pattern', () => {
      const markets = [{
        id: '1',
        testParam: 'testParam',
        name: 'market score'
      }];
      const pattern = new RegExp('^sscore\\sscore$', 'i');

      expect(service.isAnyMarketByPattern(markets, pattern)).toBeFalsy();
    });
  });

  describe('unsubscribeEventChildsUpdates', () => {
    it('should unsubscribe from liveServeMS', () => {
      const key = 'matches-type-111';

      service.unsubscribeEventChildsUpdates(key);

      expect(liveUpdatesWSService.unsubscribe).toHaveBeenCalledWith(key);
    });
  });

  it('todayEventsByClasses should call for events by classes', () => {
    service.todayEventsByClasses();

    expect(eventService.eventsByClasses).toHaveBeenCalledWith(service.config.request);
  });

  it('competitionsInitClassIds should call for init class ids', () => {
    service.competitionsInitClassIds();

    expect(cmsService.getSystemConfig).toHaveBeenCalled();
  });

  describe('#outrigths', () => {
    it('should get eventSortCode', () => {
      service.config = {
        request: {
          eventSortCode: null
        }
      };


      service.getEventSortCode = jasmine.createSpy('getEventSortCode').and.returnValue(OUTRIGHTS_CONFIG.sportSortCode);

      service.outrights();

      expect(service.getEventSortCode).toHaveBeenCalled();
    });
  });

  describe('#getEventSortCode', () => {
    it('should return outright sort codes', () => {
      service.sportConfig = {
        config: {
          isOutrightSport: true
        }
      } as any;

      const result = service.getEventSortCode();
      expect(result).toEqual(OUTRIGHTS_CONFIG.outrightsSportSortCode);
    });

    it('should return outright match sort codes', () => {
      service.sportConfig = {
        config: {
          isOutrightSport: false
        }
      } as any;

      const result = service.getEventSortCode();
      expect(result).toEqual(OUTRIGHTS_CONFIG.sportSortCode);
    });
  });

  it('jackpot should call for football jackpot list', () => {
    service.jackpot();

    expect(eventService.getFootballJackpotList).toHaveBeenCalled();
  });

  describe('#isFootball', () => {
    it('should return true', () => {
      service.sportConfig = {
        config: {
          request: {
            categoryId: '16'
          }
        }
      };

      const result = service.isFootball();

      expect(result).toEqual(true);
    });
    it('should return false', () => {
      service.sportConfig = {
        config: {
          request: {
            categoryId: '1'
          }
        }
      };

      const result = service.isFootball();

      expect(result).toEqual(false);
    });
  });

  it('competitionsInitClassIds', () => {
    service.competitionsInitClassIds();

    expect(cmsService.getSystemConfig).toHaveBeenCalled();
  });
});

