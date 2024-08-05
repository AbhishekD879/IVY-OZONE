import { fakeAsync, tick } from '@angular/core/testing';
import { QuickNavigationComponent } from '@racing/components/quickNavigation/quick-navigation.component';
import { of } from 'rxjs';
import { filteredEventsDataMock } from '../racingEventMain/racing-event-main.component.mock';

describe('QuickNavigationComponent', () => {
  let component: QuickNavigationComponent;
  let routingHelperService, sortByOptionsService, router, filterService, rendererService, storage, locale,pubSubService;
  let event,horseRacingService,greyhoundService,command,eventService,windowRef, elementRef, deviceService, sessionStorageService;
  const meetingsTitleMock = {
    ENHRCS: 'ENHRCS',
    INT: 'INT',
    UK: 'UK',
    VR: 'VR',
    US: 'USA',
    ZA: 'ZA',
    AE: 'AE',
    CL: 'CL',
    IN: 'IN',
    AU: 'AU',
    FR: 'FR',
    ALL: 'ALL'
  };

  beforeEach(() => {
    event = {
      cashoutAvail: 'cashoutAvail',
      categoryCode: 'categoryCode',
      categoryId: 'categoryId',
      categoryName: 'categoryName',
      displayOrder: 12,
      drilldownTagNames: 'drilldownTagNames',
      eventIsLive: false,
      eventSortCode: 'eventSortCode',
      eventStatusCode: 'eventStatusCode',
      name: 'name',
      id: 123,
      isExtraPlaceOffer: false,
      markets: [{
        "id": "556861702",
        "eventId": "22223415",
        "templateMarketId": "1014304",
        "templateMarketName": "Outright",
        "marketMeaningMajorCode": "-",
        "marketMeaningMinorCode": "--",
        "name": "Ante Post",
        "isLpAvailable": "true",
        "isEachWayAvailable": "true",
        "eachWayFactorNum": "1",
        "eachWayFactorDen": "4",
        "eachWayPlaces": "4",
        "displayOrder": 0,
        "marketStatusCode": "A",
        "isActive": "true",
        "siteChannels": "P,Q,C,I,M,",
        "liveServChannels": "sEVMKT0556861702,",
        "liveServChildrenChannels": "SEVMKT0556861702,",
        "priceTypeCodes": "LP,",
        "isAvailable": "true",
        "maxAccumulators": "25",
        "minAccumulators": "1",
        "cashoutAvail": "N",
        "termsWithBet": "Y",
        "outcomes": [],
        "terms": "Each Way: 1/4 odds - places 1-2-3-4",
        "label": "Ante Post",
        "isAntepost": null,
        "path": "ante-post",
        "isSmartBoosts": false
    }]
    } as any;

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      events: {
        subscribe: jasmine.createSpy().and.callFake((cb) => {
          cb({
            navigationTrigger: 'popstate'
          })
        }),
      }
    };

    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };

    sortByOptionsService = {
      set: jasmine.createSpy('set'),
    };
    filterService = {};
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy(),
        removeClass: jasmine.createSpy(),
        setStyle: jasmine.createSpy()
      }
    };

    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('Test')
    };

    storage = {
      get: jasmine.createSpy('storage.get')
    };

    horseRacingService = {
      getTypeNamesEvents: jasmine.createSpy('getTypeNamesEvents').and.returnValue(Promise.resolve({filteredEventsDataMock}))
    };

    greyhoundService = {
      getTypeNamesEvents: jasmine.createSpy('getTypeNamesEvents').and.returnValue(Promise.resolve({filteredEventsDataMock}))
    };

    command = {
      API: {
        HR_ENHANCED_MULTIPLES_EVENTS: 'HR_ENHANCED_MULTIPLES_EVENTS'
      }
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {MEETING_OVERLAY_FLAG: 'MEETING_OVERLAY_FLAG'},
      subscribe: jasmine.createSpy('subscribe').and
      .callFake((file, method, cb) => {
       cb({
        'flag': false,
        'id': "test",
         })
      }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    eventService = {
      hrEventSubscription:{
      next: jasmine.createSpy('next').and.returnValue(of(true))
      }
    };

    windowRef = {      
      nativeWindow: {
        location: {
         href: 'https://test:56788'
        },
        setInterval: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearInterval: jasmine.createSpy(),
        setTimeout: jasmine.createSpy('setTimeout'),
      },
      innerHeight: 500,
      document: {querySelector: jasmine.createSpy().and.returnValue({
        getBoundingClientRect: jasmine.createSpy().and.returnValue({bottom:150.1223})
      })}
    };

    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    deviceService = { isDesktop: false };
    sessionStorageService = {
      set: jasmine.createSpy('set')
    };
    component = new QuickNavigationComponent(
      filterService, routingHelperService, sortByOptionsService, router, rendererService, storage, locale,pubSubService,
      horseRacingService, greyhoundService, command,eventService,windowRef, elementRef, deviceService, sessionStorageService
    );
    component.items = [];
  });

  it('should create QuickNavigationComponent instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {

    it('filter virtulas', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ];

      storage.get.and.returnValue({UIR: 'UK', IR: 'INT'});
      component.ngOnInit();

      expect(component.items).toEqual([
        {flag: 'UK', data: []},
        {flag: 'INT', data: []}
      ]);
    });

    it('filter international', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'US', data: []},
        {flag: 'FR', data: []},
        {flag: 'VR', data: []}
      ];

      storage.get.and.returnValue({UIR: 'UK', LVR: 'VR'});
      component.ngOnInit();

      expect(component.items).toEqual([
        {flag: 'UK', data: []},
        {flag: 'VR', data: []}
      ]);
    });

    it('filter UK', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ];

      storage.get.and.returnValue({IR: 'INT', LVR: 'VR'});
      component.ngOnInit();

      expect(component.items).toEqual([
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ]);
    });

    it('not filtered', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ];

      storage.get.and.returnValue(null);
      component.ngOnInit();

      expect(component.items).toEqual([
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ]);

      storage.get.and.returnValue({UIR: 'UK', LVR: 'VR', IR: 'INT'});
      component.ngOnInit();

      expect(component.items).toEqual([
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ]);
    });

    it('popstate subscription handler', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ];
      component.closeMenu = jasmine.createSpy();
      storage.get.and.returnValue(null);
      component.showMenu = true;
      component.ngOnInit();
      expect(component.closeMenu).toHaveBeenCalled();
    });

    it('popstate sessionStorageService handler', () => {
      component.meetingsTitle = meetingsTitleMock;
      component.eventEntity = event;
      component.items = [
        {flag: 'UK', data: []},
        {flag: 'INT', data: []},
        {flag: 'VR', data: []}
      ];
      component.isEventAntePost = true;
      component.eventEntity.categoryId = '19';
      storage.get.and.returnValue(null);
      component.showMenu = true;
      component.ngOnInit();
      expect(sessionStorageService.set).toHaveBeenCalled();
    });

    it('isAntepostMarket', () => {
      component.eventEntity = event;
      component.eventEntity.markets[0].isAntepost = 'true';
      expect(component.isAntePostEvent()).toBeTruthy();
  
      component.eventEntity.markets[0].isAntepost = null;
      component.eventEntity.markets[0].label = null;
      expect(component.isAntePostEvent()).toBeFalsy();
  
      component.eventEntity.markets[0].isAntepost = null;
      component.eventEntity.markets[0].label = 'Ante Post';
      expect(component.isAntePostEvent()).toBeTruthy();
    });

    it('isAntepostMarket with categrory as greyhounds id and future tabs', () => {
      component.eventEntity = event;
      component.eventEntity.markets[0].isAntepost = 'false';
      component.eventEntity.correctedDay = 'racing.flat';
      component.eventEntity.markets[0].label = null;
      component.eventEntity.categoryId = '19';
      expect(component.isAntePostEvent()).toBeTruthy();
    });

  });

  describe('#ngOnChanges', () => {
    it('should add class to body', () => {
      component.meetingsTitle = {};
      component['eventEntity'] = {} as any;
      component.eventEntity.categoryId = '21';
      storage.get.and.returnValue({UIR: 'UK', IR: 'INT'});
      const changes: any = {
        showMenu: {
          currentValue: 1
        },
        eventEntity: {
          currentValue: {
            correctedDayValue: 'racing.today'
          }
        }
      };
      component.ngOnChanges(changes);
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component['rendererService']['renderer']['addClass']).toHaveBeenCalled();
    });

    it('should add class to body GH', () => {
      component.meetingsTitle = {};
      component['eventEntity'] = {} as any;
      component.eventEntity.categoryId = '16';
      storage.get.and.returnValue({UIR: 'UK', IR: 'INT'});
      const changes: any = {
        showMenu: {
          currentValue: 1
        },
        eventEntity: {
          currentValue: {
            correctedDayValue: 'racing.today'
          }
        }
      };
      component.ngOnChanges(changes);
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component['rendererService']['renderer']['addClass']).toHaveBeenCalled();
    });

    it('should add class to body', () => {
      component.meetingsTitle = {};
      component['eventEntity'] = {} as any;
      component.eventEntity.categoryId = '21';
      storage.get.and.returnValue({UIR: 'UK', IR: 'INT'});
      const changes: any = {
        showMenu: {
          currentValue: 1
        },
        eventEntity: {
          currentValue: {
            correctedDayValue: 'racing.today'
          }
        }
      };
      component.isMarketAntepost = true;
      component.ngOnChanges(changes);
      expect(component['rendererService']['renderer']['setStyle']).toHaveBeenCalled();
    });

    it('should remove class from body', fakeAsync(() => {
      component.meetingsTitle = {};
      component['eventEntity'] = {} as any;
      component.eventEntity.categoryId = '21';
      storage.get.and.returnValue({UIR: 'UK', IR: 'INT'});
      const changes: any = {
        showMenu: 0
      };
      component.ngOnChanges(changes);
      tick(300);

      expect(component['rendererService']['renderer']['removeClass']).toHaveBeenCalled();
    }));
  });

  it('#closeMenu', () => {
    component.showMeetingsListFn.emit = jasmine.createSpy();

    component.closeMenu();
    expect(component.showMeetingsListFn.emit).toHaveBeenCalled();
  });

  it('#trackById', () => {
    expect(component.trackById(null, { id: 123 })).toBe(123);
  });

  describe('#ngOnDestroy', () => {
    it('#ngOnDestroy routerState', () => {
      component['routerState'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['routerState'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('#selectEvent', () => {
    it('navigateByUrl should be called', () => {
      component.eventEntity = {
        name: 'name2',
        id: 321
      } as any;
      component.selectEvent(event);

      expect(sortByOptionsService.set).toHaveBeenCalledWith('Price');
      expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
    });

    it('closeMenu should be called', () => {
      component.closeMenu = jasmine.createSpy();
      component.eventEntity = {
        name: 'name',
        id: 123
      } as any;
      component.selectEvent(event);

      expect(component.closeMenu).toHaveBeenCalled();
    });

    it('closeMenu should be called', () => {
      component.closeMenu = jasmine.createSpy();
      event.isExtraPlaceOffer = true;
      component.eventEntity = {
        name: 'name',
        id: 123,
        isExtraPlaceOffer: true
      } as any;
      component.selectEvent(event);

      expect(component.closeMenu).toHaveBeenCalled();
    });
    it('closeMenu should be called(Scenario 2)', () => {
      const event2 = {
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId',
        categoryName: 'categoryName',
        displayOrder: 12,
        drilldownTagNames: 'drilldownTagNames',
        eventIsLive: false,
        eventSortCode: 'eventSortCode',
        eventStatusCode: 'eventStatusCode',
        name: 'name',
        id: 456,
        isExtraPlaceOffer: false
      } as any;
      component.closeMenu = jasmine.createSpy();
      event.isExtraPlaceOffer = true;
      component.eventEntity = {
        name: 'name',
        id: 123,
        isExtraPlaceOffer: true
      } as any;
      component.selectEvent(event2);
      expect(component.closeMenu).toHaveBeenCalled();
    });
  });

  describe('#getLink', () => {
    it('should return a link', () => {
      component.items = [
        {
          flag: 'UK',
          data: [
            {
              meeting: 'meeting',
              events: event
            }
          ]
        }
      ];
      const result = component.getLink(event);

      expect(result).toBe('url');
    });
    it('should not return a link', () => {
      component.items = null;
      const result = component.getLink(event);

      expect(result).toBe('');
    });
  });

  describe('#isActiveLink', () => {
    it('isActiveLink should return true', () => {
      component.eventEntity = {
        name: 'name'
      } as any;
      event.isExtraPlaceOffer = false;
      const result = component.isActiveLink(event);

      expect(result).toBeTruthy();
    });

    it('isActiveLink should return false', () => {
      component.eventEntity = {
        name: 'name2'
      } as any;
      event.isExtraPlaceOffer = true;
      const result = component.isActiveLink(event);

      expect(result).toBeFalsy();
    });
  });
});
