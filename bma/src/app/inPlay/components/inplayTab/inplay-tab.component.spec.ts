import { of as observableOf, of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { InplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';

describe('InplayTabComponent', () => {
  let component: InplayTabComponent,
    inPlayConnectionService,
    inplayMainService,
    cmsService,
    inplayStorageService,
    inplaySubscriptionManagerService,
    pubsubService,
    deleteFromCashHandler,
    awsService,
    changeDetectorRef,
    activatedRoute;

  const ribbonMock = {
    data: [{
      categoryId: 123,
      liveEventCount: 1,
      upcomingEventCount: 2
    }]
  };

  beforeEach(fakeAsync(() => {
    inPlayConnectionService = {
      connectComponent: jasmine.createSpy().and.returnValue(observableOf(true)),
      disconnectComponent: jasmine.createSpy(),
      status: {
        reconnectFailed: true
      }
    };
    inplayMainService = {
      getEventsCounter: jasmine.createSpy(),
      initSportsCache: jasmine.createSpy(),
      unsubscribeForUpdates: jasmine.createSpy(),
      getStructureData: jasmine.createSpy().and.returnValue(observableOf({})),
      getTopLevelTypeParameter: jasmine.createSpy(),
      getSportData: jasmine.createSpy().and.returnValue(observableOf({})),
      clearDeletedEventFromType: jasmine.createSpy(),
      clearDeletedEventFromSport: jasmine.createSpy(),
      getUnformattedEventsCounter: jasmine.createSpy(),
      updateEventsCounter: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf(ribbonMock)),
      getEventCountersByCategory: jasmine.createSpy('getEventCountersByCategory').and.returnValue({} as any)
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        InPlayCompetitionsExpanded: {
          competitionsCount: 10
        }
      })),
      getMarketSwitcherFlagValue: jasmine.createSpy().and.returnValue(observableOf(true))
    };
    inplayStorageService = {
      destroySportsCache: jasmine.createSpy()
    };
    inplaySubscriptionManagerService = {
      unsubscribeForSportCompetitionChanges: jasmine.createSpy(),
      unsubscribeForLiveUpdates: jasmine.createSpy(),
      subscribe4RibbonUpdates: jasmine.createSpy()
    };
    pubsubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((fileName: string, method: string | string[], callback: Function) => {
        if (method === 'DELETE_EVENT_FROM_CACHE') {
          deleteFromCashHandler = callback;
        } else {
          callback();
        }
      }),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish')
    };
    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    awsService = {
      addAction: jasmine.createSpy()
    };

    activatedRoute = {
      snapshot: {
          paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
          }
      },
      params: of({
          sport: 'golf',
          id: '18'
      })
  };

    component = new InplayTabComponent(inPlayConnectionService, inplayMainService, cmsService,
      inplayStorageService, inplaySubscriptionManagerService, pubsubService, changeDetectorRef, awsService, activatedRoute);
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayTabComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#ngOnInit', fakeAsync(() => {
    component['pubsubService'].subscribe = jasmine.createSpy('subscribe')
      .and.callFake((fileName: string, method: string | string[], callback: Function) => {
        if (method === pubSubApi.EVENT_COUNT_UPDATE || method === pubSubApi.RELOAD_IN_PLAY) {
          // not to call callback for event count update on init
        } else {
          callback();
        }
      });

    component.addEventListeners = jasmine.createSpy();
    component.singleSport = true;
    component.id = 16;
    component.ngOnInit();
    expect(inPlayConnectionService.connectComponent).toHaveBeenCalled();
    expect(component.appReady).toBeTruthy();
    expect(inplayMainService.initSportsCache).toHaveBeenCalled();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(component.expandedLeaguesCount).toEqual(10);
    tick();
    expect(component.addEventListeners).toHaveBeenCalled();
    expect(component.dataReady).toBeDefined();
    expect(component.allEventsCount).not.toBeDefined();
    expect(component.allUpcomingEventsCount).not.toBeDefined();
    component.id = 123;
    component.ngOnInit();
    tick();
    expect(component.allEventsCount).toEqual(1);
    expect(component.allUpcomingEventsCount).toEqual(2);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  }));

  it('should update Event counters from Ribbon on live Update', () => {
    component['inplayMainService'].getUnformattedEventsCounter = jasmine.createSpy('getUnformattedEventsCounter').and.returnValue({
      livenow: ribbonMock.data[0].liveEventCount,
      upcoming: ribbonMock.data[0].upcomingEventCount
    });

    component['pubsubService'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, event, fn) => {
      if (event === pubSubApi.EVENT_COUNT_UPDATE) {
        fn(ribbonMock);

        expect(component.allEventsCount).toEqual(ribbonMock.data[0].liveEventCount);
        expect(component.allUpcomingEventsCount).toEqual(ribbonMock.data[0].upcomingEventCount);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      }
    });

    component.ngOnInit();
  });

  it('should update Event counters from Ribbon on live Update when no counter data', () => {
    component['inplayMainService'].getUnformattedEventsCounter = jasmine.createSpy('getUnformattedEventsCounter').and.returnValue(null);

    component['pubsubService'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, event, fn) => {
      if (event === pubSubApi.EVENT_COUNT_UPDATE) {
        fn(ribbonMock);

        expect(component.allEventsCount).toEqual(0);
        expect(component.allUpcomingEventsCount).toEqual(0);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      }
    });

    component.ngOnInit();
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(inplayStorageService.destroySportsCache).toHaveBeenCalled();
    expect(inplayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inPlayConnectionService.disconnectComponent).toHaveBeenCalled();
  });

  it('#trackById', () => {
    expect(component.trackById(1, 'someFilter')).toEqual('1_someFilter');
  });

  describe('#addEventListeners', () => {
    beforeEach(() => {
      component['reloadComponent'] = jasmine.createSpy();
    });
    it('should listen reload components', () => {
      component.addEventListeners();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
    });
    it('for single sport', () => {
      component.singleSport = true;
      component.id = 123;
      component.addEventListeners();
      deleteFromCashHandler();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function));
      expect(component.viewByFilters).toBeDefined();
      expect(inplayMainService.clearDeletedEventFromType).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('for multiple sports', fakeAsync(() => {
      component.addEventListeners();
      deleteFromCashHandler();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay',  pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function));
      tick();
      expect(inplayMainService.clearDeletedEventFromSport).toHaveBeenCalled();
    }));

    describe('SOCKET_RECONNECT_ERROR', () => {
      const channel = `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`;

      beforeEach(() => {
        pubsubService.subscribe.and.callFake((sbs, chn,  fn) => {
          if (channel === chn) {
            fn();
          }
        });
      });

      it('should subscribe', () => {
        component.addEventListeners();

        expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', channel, jasmine.any(Function));
      });

      it('should track error for single sport', () => {
        component.singleSport = true;
        component.addEventListeners();

        expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>wsError');
      });

      it('should not track error for multiple sport', () => {
        component.singleSport = false;
        component.addEventListeners();

        expect(awsService.addAction).not.toHaveBeenCalled();
      });
    });
  });

  describe('#updateSportData', () => {
    it('should call updateSingleSportData', () => {
      component['updateSingleSportData'] = jasmine.createSpy();
      component.singleSport = true;
      component.id = 123;
      component.updateSportData(['someFilter']);
      expect(component['updateSingleSportData']).toHaveBeenCalled();
    });

    it('multiple sports flow with error', () => {
      component.ssError = false;
      spyOn(component as any, 'applyStructureData').and.callThrough();
      component.updateSportData(['someFilter'], {
        additionalParams: 'someParams',
        useCache: true
      } as any).subscribe();
      expect(inplayMainService.getStructureData).toHaveBeenCalledWith(true);
      expect(component['applyStructureData']).toHaveBeenCalled();
      expect(component.ssError).toBe(true);
    });

    it('multiple sports flow without errors', () => {
      component.ssError = true;
      const mock = {
        creationTime: 123
      };
      component['inplayMainService'].getStructureData = jasmine.createSpy('inplayMainService').and.returnValue(observableOf(mock));
      spyOn(component as any, 'applyStructureData').and.callThrough();
      component.updateSportData(['someFilter'], {
        additionalParams: 'someParams',
        useCache: true
      } as any).subscribe();
      expect(inplayMainService.getStructureData).toHaveBeenCalledWith(true);
      expect(component['applyStructureData']).toHaveBeenCalled();
      expect(component.ssError).toBe(false);
    });

    it('single sport flow', () => {
      component['applyStructureData'] = jasmine.createSpy();
      component.singleSport = true;
      component.id = 16;

      component.updateSportData(['someFilter'], {
        additionalParams: 'someParams',
        useCache: true
      } as any).subscribe();
      expect(inplayMainService.getStructureData).not.toHaveBeenCalled();
      expect(component['applyStructureData']).not.toHaveBeenCalled();
    });
  });

  describe('#isLiveNowFilter', () => {
    it('should be true', () => {
      component.viewByFilters = ['someFilter'];
      expect(component['isLiveNowFilter']('someFilter')).toBeTruthy();
    });
    it('should be false', () => {
      component.viewByFilters = ['someFilter'];
      expect(component['isLiveNowFilter']('someOtherFilter')).toBeFalsy();
    });
  });

  it('#applySingleSportData', () => {
    component.data = {
      someData: {}
    } as any;
    component['applySingleSportData']({
      someData: 'someData'
    } as any, 'someFilter');
    expect(component.ssError).toBeDefined();
    expect(component.firstLoad).toBeFalsy();
  });

  describe('#updateSingleSportData', () => {
    beforeEach(() => {
      component['applySingleSportData'] = jasmine.createSpy();
      component.data = {};
    });
    it('when segment is present', () => {
      component.data['someSegment'] = {
        eventsIds: [],
        categoryId: [],
        topLevelType: 'someType',
        marketSelector: 'someSelector'
      } as any;
      component['updateSingleSportData'](false, {} as any, 'someSegment').subscribe();
      expect(inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges).toHaveBeenCalled();
      expect(inplaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalled();
      expect(inplayMainService.getSportData).toHaveBeenCalled();
      expect(component['applySingleSportData']).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith('INPLAY_DATA_RELOADED');
    });
    it('when segment is not present', () => {
      component['updateSingleSportData'](false, {} as any, 'someSegment').subscribe();
      expect(inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges).not.toHaveBeenCalled();
      expect(inplaySubscriptionManagerService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
      expect(inplayMainService.getSportData).toHaveBeenCalled();
      expect(component['applySingleSportData']).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith('INPLAY_DATA_RELOADED');
    });

    it('updateSingleSportData when topLevel is LIVE_EVENT', () => {
      const mock = {
        topLevelType: 'LIVE_EVENT',
        eventCount: 5
      };
      const requestParams = {} as any;
      component.id = 123;
      component.allEventsCount = 10;

      component['inplayMainService'].getSportData = jasmine.createSpy('inplayMainService').and.returnValue(observableOf(mock));
      component['updateSingleSportData'](false, requestParams, 'livenow').subscribe(() => {
        expect(mock.eventCount).toEqual(component.allEventsCount);
      });
      expect( component['inplayMainService'].getSportData).toHaveBeenCalledWith(requestParams, false, true, true, false, undefined);
    });

    it('updateSingleSportData when topLevel is UPCOMING_EVENT', () => {
      const mock = {
        topLevelType: 'UPCOMING_EVENT',
        eventCount: 5
      };
      const requestParams = {} as any;
      component.id = 123;
      component.allUpcomingEventsCount = 10;

      component['inplayMainService'].getSportData = jasmine.createSpy('inplayMainService').and.returnValue(observableOf(mock));
      component['updateSingleSportData'](false, requestParams, 'upcoming').subscribe(() => {
        expect(mock.eventCount).toEqual(component.allUpcomingEventsCount);
      });
      expect(component['inplayMainService'].getSportData).toHaveBeenCalledWith(requestParams, false, false, true, false, undefined);
    });

    it('updateSingleSportData when topLevel is neighter UPCOMING_EVENT no LIVE_EVENT', () => {
      const mock = {
        topLevelType: 'test',
        eventCount: 5
      };
      component.id = 123;
      component.allEventsCount = 10;

      component['inplayMainService'].getSportData = jasmine.createSpy('inplayMainService').and.returnValue(observableOf(mock));
      component['updateSingleSportData'](false, {} as any, 'livenow').subscribe(() => {
        expect(mock.eventCount).toEqual(5);
      });
    });
  });

  describe('trackErrorMessage', () => {
    it('should not track error not ssError', () => {
      component.ssError = false;
      component['trackErrorMessage']();

      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should not track error if ssError', () => {
      component.ssError = true;
      component['trackErrorMessage']();

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });
  });

  it('should check tracking error message after applying received data from MS', () => {
    spyOn<any>(component, 'trackErrorMessage');
    component['applyStructureData'](null);

    expect(component['trackErrorMessage']).toHaveBeenCalled();
  });

  it('should check tracking error message after apply single sport data', () => {
    spyOn<any>(component, 'trackErrorMessage');
    component['applySingleSportData'](null, 'LIVE_EVENT');

    expect(component['trackErrorMessage']).toHaveBeenCalled();
  });

  it('reload handler should subscribe to sport data updating', () => {
    spyOn(component, 'updateSportData').and.returnValue(observableOf({} as any));
    const options = {useCache: true} as any;
    component.onDataReload('foo', options);

    expect(component.updateSportData).toHaveBeenCalledWith(['foo'], options);
    expect(component.dataReady).toBe(true);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  describe('reloadComponent', () => {
    it('should call ngOnDestroy and ngOnInit', () => {
      spyOn<any>(component, 'ngOnDestroy');
      spyOn<any>(component, 'ngOnInit');
      component['reloadComponent']();

      expect(component.dataReady).toBe(false);
      expect(component.ssError).toBe(false);
      expect(component.appReady).toBe(false);
      expect(component['ngOnDestroy']).toHaveBeenCalled();
      expect(component['ngOnInit']).toHaveBeenCalled();
    });
  });

  describe('isSportEventsAvailable', () => {
    it('should return true', () => {
      const data = {
        eventsByTypeName: [1, 2, 3]
      };
      expect(!!component['isSportEventsAvailable'](data)).toBe(true);
    });

    it('should return false', () => {
      let data = {};
      expect(!!component['isSportEventsAvailable'](data)).toBe(false);

      data = {
        eventsByTypeName: []
      };
      expect(!!component['isSportEventsAvailable'](data)).toBe(false);
    });
  });

  describe('#getEventType', () => {
    it('should return single if it is a single sport', () => {
      component.singleSport = true;
      const response = component['getEventType']();
      expect(response).toBe('SINGLE');
    });
    it('should return multiple if it is not a single sport', () => {
      component.singleSport = false;
      const response = component['getEventType']();
      expect(response).toBe('MULTIPLE');
    });
  });
});
