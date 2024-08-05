import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { InplaySingleSportPageComponent } from '@app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplaySingleSportPageComponent', () => {
  let component: InplaySingleSportPageComponent;
  let cmsService;
  let inplaySubscriptionManagerService;
  let router;
  let inplayConnectionService;
  let pubSubService;
  let route;
  let inplayMainService;
  let deviceService;
  let awsService;
  let changeDetectorRef;
  let sportsConfigService;

  const ribbonItems = [
    {
      targetUriCopy: 'watchlive',
      targetUri: '/in-play/watchlive'
    },
    {
      targetUriCopy: 'allsports',
      targetUri: '/in-play/allsports'
    },
    {
      targetUriCopy: 'football',
      targetUri: '/in-play/football'
    },
    {
      targetUriCopy: 'tennis',
      targetUri: '/in-play/tennis'
    }
  ];

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    route = {
      params: observableOf([{
        InPlayCompetitionsExpanded: {
          competitionsCount: '3'
        },
        sport: 'tennis'
      }]),
      snapshot: { params: {} }
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        InPlayCompetitionsExpanded: {
          competitionsCount: 2
        }
      }))
    };

    inplaySubscriptionManagerService = {
      unsubscribeForSportCompetitionChanges: jasmine.createSpy('unsubscribeForSportCompetitionChanges'),
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    };

    inplayMainService = {
      getUnformattedEventsCounter: jasmine.createSpy('getUnformattedEventsCounter'),
      updateEventsCounter: jasmine.createSpy('updateEventsCounter'),
      addRibbonURLHandler: jasmine.createSpy('addRibbonURLHandler'),
      getTopLevelTypeParameter: jasmine.createSpy('getTopLevelTypeParameter').and.returnValues('LIVE_EVENT', 'UPCOMING_EVENT'),
      getRibbonData: jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'LIVE_EVENT'
          }
        ]
      })),
      getSportId: jasmine.createSpy('getSportId').and.returnValue(observableOf('16')),
      getSportData: jasmine.createSpy('getSportData').and.returnValue(observableOf([{}])),
      clearDeletedEventFromType: jasmine.createSpy('clearDeletedEventFromType'),
      getFirstSport: jasmine.createSpy('getFirstSport').and.returnValue({
        alt: 'alt2',
        categoryId: 16,
        disabled: false,
        hasLiveNow: false,
        hasLiveStream: false,
        targetUriCopy: 'football',
        targetUri: '/in-play/football'
      }),
      unsubscribeForEventsUpdates: jasmine.createSpy('unsubscribeForEventsUpdates'),
      initSportsCache: jasmine.createSpy('initSportsCache'),
      getEventCountersByCategory: jasmine.createSpy('getEventCountersByCategory').and.returnValue({} as any)
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a: string, b: string[] | string, fn: Function) => {
        if (b === 'EVENT_COUNT_UPDATE') {
          fn(ribbonItems);
        } else if (b === 'RELOAD_IN_PLAY') {
          spyOn(component, 'ngOnInit');
          spyOn(component, 'ngOnDestroy');
          fn();
        }
      }),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
    };

    deviceService = {
      isOnline: jasmine.createSpy('isOnline')
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    inplayConnectionService = {
      status: jasmine.createSpy('status'),
      setConnectionErrorState: jasmine.createSpy('setConnectionErrorState'),
      connectComponent: jasmine.createSpy('connectComponent').and.returnValue(observableOf(true))
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({
        sportConfig: {
          config: {
            request: {
              categoryId: '16',
              aggregatedMarkets: ''
            }
          }
        }
      }))
    };

    component = new InplaySingleSportPageComponent(inplayMainService, inplaySubscriptionManagerService,
      pubSubService, inplayConnectionService, route, cmsService, router, deviceService, awsService, changeDetectorRef, sportsConfigService);
  });

  describe('@ngOnInit', () => {
    it('should init component', fakeAsync(() => {
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(component.categoryId).toEqual('16' as any);
      expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should init component when no sportId', fakeAsync(() => {
      inplayMainService.getSportId.and.returnValue(observableOf(null));
      component['setSportData'] = jasmine.createSpy('setSportData');
      component['showContent'] = jasmine.createSpy('showContent');
      component['applyData'] = jasmine.createSpy('applyData');
      component.ngOnInit();
      tick(200);

      expect(component['setSportData']).not.toHaveBeenCalled();
      expect(component['applyData']).not.toHaveBeenCalled();
      expect(component['showContent']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should init component when no cmsConfig', fakeAsync(() => {
      spyOn<any>(component, 'applyData');

      inplayMainService.getSportId.and.returnValue(observableOf('16'));
      cmsService.getSystemConfig.and.returnValue(observableOf(null));
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(component['applyData']).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should init component and route.params should throw error', fakeAsync(() => {
      component['showContent'] = jasmine.createSpy('showContent');
      route.params = throwError('error');
      component.ngOnInit();
      tick(200);
      expect(component.sportSectionData['livenow']).toEqual({} as any);
    }));

    it('should redirect to first sport after undisplay last event from current sport', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((subscriberName: string, channel: string, channelFunction: Function) => {
        component['sportUri'] = 'basketball';
        channelFunction(ribbonItems);
      });
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);
      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/football');
      expect(inplayMainService.getUnformattedEventsCounter).toHaveBeenCalledWith(ribbonItems, '16');
      expect(inplayMainService.updateEventsCounter).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should not redirect to first sport after undisplay event from current sport', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((subscriberName: string, channel: string, channelFunction: Function) => {
        component['sportUri'] = 'tennis';
        channelFunction(ribbonItems);
      });
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(inplayMainService.getUnformattedEventsCounter).toHaveBeenCalledWith(ribbonItems, '16');
      expect(inplayMainService.updateEventsCounter).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should unsubscribe For Events Updates after route change', fakeAsync(() => {
      component.sportSectionData = {
        'livenow': {
          categoryId: '16',
          topLevelType: 'topLevelType',
          marketSelector: 'Over/Under',
          eventsIds: [1, 2]
        } as ISportSegment
      };
      component['viewByFilters'] = ['livenow', 'upcoming'];

      inplayMainService.getSportId.and.returnValue(observableOf(16));
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.unsubscribeForEventsUpdates).toHaveBeenCalledWith({
        categoryId: '16',
        topLevelType: 'topLevelType',
        marketSelector: 'Over/Under',
        eventsIds: [1, 2]
      });
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should Not unsubscribe For Events Updates after route change when sportSectionData is empty', fakeAsync(() => {
      component['viewByFilters'] = ['livenow', 'upcoming'];

      inplayMainService.getSportId.and.returnValue(observableOf(16));
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.unsubscribeForEventsUpdates).not.toHaveBeenCalledWith({});
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should Not unsubscribe For Events Updates after route change when livenow is empty', fakeAsync(() => {
      component.sportSectionData = {
        'livenow': null
      };
      component['viewByFilters'] = ['livenow', 'upcoming'];

      inplayMainService.getSportId.and.returnValue(observableOf(16));
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.unsubscribeForEventsUpdates).not.toHaveBeenCalledWith({});
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('getSportData', fakeAsync(() => {
      component['sportId'] = 16;
      component['viewByFilters'] = ['livenow', 'upcoming'];

      inplayMainService.getSportId.and.returnValue(observableOf(16));
      component['showContent'] = jasmine.createSpy('showContent');
      component.isLiveNowFilter = jasmine.createSpy('isLiveNowFilter').and.returnValues(true, false);
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.getSportId).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(inplayMainService.getSportData).toHaveBeenCalledTimes(2);
      expect(inplayMainService.getSportData.calls.allArgs()).toEqual([[{
        categoryId: 16,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
      }, true, true, true,false, []], [{
        categoryId: 16,
        isLiveNowType: false,
        topLevelType: 'UPCOMING_EVENT',
      }, true, false, false,false,[]]]);
    }));
    it('getSportData isFetch paramater should be true if categoryId is 21', fakeAsync(() => {
      component['sportId'] = 21;
      component['viewByFilters'] = ['livenow', 'upcoming'];

      inplayMainService.getSportId.and.returnValue(observableOf(21));
      component['showContent'] = jasmine.createSpy('showContent');
      component.isLiveNowFilter = jasmine.createSpy('isLiveNowFilter').and.returnValues(true, false);
      component.ngOnInit();
      tick(200);
      expect(inplayMainService.getSportData.calls.allArgs()).toEqual([[{
        categoryId: 21,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
      }, true, true, true, true,[]], [{
        categoryId: 21,
        isLiveNowType: false,
        topLevelType: 'UPCOMING_EVENT',
      }, true, false, false, true,[]]]);
    }));

    it('getSportData when not current sport', fakeAsync(() => {
      inplayMainService.getSportId.and.returnValue(observableOf(null));
      component['showContent'] = jasmine.createSpy('showContent');
      expect(component['sportId']).toBeUndefined();
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.addRibbonURLHandler).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component['sportId']).toEqual(null);
    }));
  });

  it('should use OnPush strategy', () => {
    expect(InplaySingleSportPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('OnDestroy', () => {
    // @ts-ignore
    component.routeListener = { unsubscribe: jasmine.createSpy() };

    component.ngOnDestroy();

    expect(component.routeListener.unsubscribe).toHaveBeenCalledTimes(1);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('inplaySingleSportPage');
  });

  describe('#applyData', () => {
    it('should not goToFilter if ssError be truthy', fakeAsync(() => {
      deviceService.isOnline.and.returnValue(true);
      component.firstLoad = true;
      spyOn<any>(component, 'trackErrorMessage');
      component.applyData({} as { [key: string]: ISportSegment });
      tick(200);
      expect(component.dataReady).toBe(true);
      expect(component['trackErrorMessage']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should not set dataReady if device is offline', fakeAsync(() => {
      deviceService.isOnline.and.returnValue(false);
      component.firstLoad = true;
      spyOn<any>(component, 'trackErrorMessage');
      component.applyData({} as { [key: string]: ISportSegment });
      tick(200);
      expect(component.dataReady).toBe(false);
      expect(component['trackErrorMessage']).toHaveBeenCalled();
    }));
  });

  describe('#updateSportData', () => {
    it('should update sport data', fakeAsync(() => {
      component.firstLoad = true;
      component.updateSportData({
        useCache: false,
        additionalParams: {
          marketSelector: 'Match Beting'
        }
      });
      tick(200);

      expect(inplayMainService.getTopLevelTypeParameter).toHaveBeenCalledWith('livenow');
      expect(inplayMainService.getSportData).toHaveBeenCalledWith({
        categoryId: '16',
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        marketSelector: 'Match Beting'
      }, false, true, true, false, undefined);
    }));

    it('should update sport data and unsubscribe from market selector', fakeAsync(() => {
      component.firstLoad = true;
      component.sportSectionData = {
        livenow: {
          categoryId: '16',
          topLevelType: 'topLevelType',
          marketSelector: 'Over/Under',
          eventsIds: [1, 2]
        }
      } as any;
      component.updateSportData({
        useCache: false,
        additionalParams: {
          marketSelector: 'Match Beting'
        }
      });
      tick(200);

      expect(inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges)
        .toHaveBeenCalledWith('16', 'topLevelType', 'Over/Under');
      expect(inplaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([1, 2]);

    }));
  });

  describe('#trackById', () => {
    it('should track by index and filter', () => {
      expect(component.trackById(1, 'livenow')).toEqual('1_livenow');
    });
  });

  describe('#setSportData', () => {
    it('should Set in-play and upcoming sport data', () => {
      component['setSportData']([{ data: 1 }, { data: 2 }] as any);

      expect(component.sportSectionData).toEqual({
        livenow: { data: 1 },
        upcoming: { data: 2 }
      } as any);
    });

    it('should Set empty array in-play and upcoming sport data when no data for filter', () => {
      component['setSportData']();

      expect(component.sportSectionData).toEqual({
        livenow: undefined,
        upcoming: undefined
      } as any);
    });
  });

  describe('#applyInplaySportData', () => {
    it('should apply sport data', () => {
      spyOn<any>(component, 'trackErrorMessage');
      component['applyInplaySportData']({
        eventsByTypeName: [
          {
            id: '1'
          }
        ]
      } as any);

      expect(component.dataReady).toEqual(true);
      expect(component.sportSectionData['livenow']).toEqual({
        eventsByTypeName: [
          {
            id: '1'
          }
        ]
      } as any);
      expect(component['trackErrorMessage']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should apply sport data when no data were received', () => {
      component['sportId'] = 16;
      component['applyInplaySportData']({} as any);

      expect(component.dataReady).toEqual(true);
      expect(component.sportSectionData).toEqual({
        livenow: {
          categoryId: '16',
          eventsByTypeName: [],
          isTierOneSport: false,
          tier: undefined,
          topLevelType: 'LIVE_EVENT'
        } as any });
      spyOn<any>(component, 'trackErrorMessage');
      component['applyInplaySportData']({} as any);

      expect(component.dataReady).toEqual(true);
      expect(component['trackErrorMessage']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('trackErrorMessage', () => {
    it('should track Site Serve error', () => {
      component['ssError'] = true;
      component['trackErrorMessage']();

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });

    it('should not track error', () => {
      component['ssError'] = false;
      component['trackErrorMessage']();

      expect(awsService.addAction).not.toHaveBeenCalled();
    });
  });

  describe('#updateEventCount', () => {
    it('should modify sport data and equals liveEventCount', () => {
      const inplaySportDataMock = {
        topLevelType: 'LIVE_EVENT',
        eventCount: 10
      };
      component.sportId = 123;
      component['inplayMainService'].getRibbonData = jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'LIVE_EVENT',
            liveEventCount: 1,
            upcomingEventCount: 2
          }
        ]
      }));
      const result = component['updateEventCount'](inplaySportDataMock as any);

      expect(result.eventCount).toEqual(1);
    });

    it('should not modify sport data', () => {
      const inplaySportDataMock = {
        topLevelType: 'LIVE_EVENT',
        eventCount: 10
      };
      component.sportId = 16;
      component['inplayMainService'].getRibbonData = jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'LIVE_EVENT',
            liveEventCount: 1,
            upcomingEventCount: 2
          }
        ]
      }));
      const result = component['updateEventCount'](inplaySportDataMock as any);

      expect(result.eventCount).toEqual(10);
    });

    it('should not modify sport data', () => {
      const inplaySportDataMock = {
        topLevelType: 'LIVE_EVENT',
        eventCount: 10
      };
      component.sportId = 16;
      component['inplayMainService'].getRibbonData = jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'UPCOMING_EVENT',
            liveEventCount: 1,
            upcomingEventCount: 2
          }
        ]
      }));
      const result = component['updateEventCount'](inplaySportDataMock as any);

      expect(result.eventCount).toEqual(10);
    });

    it('should modify sport data and equals upcomingEventCount', () => {
      const inplaySportDataMock = {
        topLevelType: 'UPCOMING_EVENT',
        eventCount: 10
      };
      component.sportId = 123;
      component['inplayMainService'].getRibbonData = jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'UPCOMING_EVENT',
            liveEventCount: 1,
            upcomingEventCount: 2
          }
        ]
      }));
      const result = component['updateEventCount'](inplaySportDataMock as any);

      expect(result.eventCount).toEqual(2);
    });

    it('should not modify sport data ', () => {
      const inplaySportDataMock = {
        topLevelType: 'test',
        eventCount: 10
      };
      component.sportId = 123;
      component['inplayMainService'].getRibbonData = jasmine.createSpy('getRibbonData').and.returnValue(observableOf({
        data: [
          {
            targetUriCopy: 'football',
            categoryId: 123,
            topLevelType: 'UPCOMING_EVENT',
            liveEventCount: 1,
            upcomingEventCount: 2
          }
        ]
      }));
      const result = component['updateEventCount'](inplaySportDataMock as any);

      expect(result.eventCount).toEqual(10);
    });
  });

  describe('#showContent', () => {
    beforeEach(() => {
      let connectTriggred = false;

      pubSubService.subscribe.and.callFake((nameSpace, eventName, callback) => {
        if (eventName === pubSubService.API.DELETE_EVENT_FROM_CACHE && !connectTriggred) {
          connectTriggred = true;
          callback();
        }
      });
    });

    it('should not clearDeletedEventFromType if sportSectionData is not available', () => {
      component.sportSectionData = null;
      component['showContent']();
      expect(inplayMainService.clearDeletedEventFromType).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should clearDeletedEventFromType if sportSectionData is available', () => {
      component.viewByFilters = [
        'someFilter'
      ];
      component.sportSectionData = {
        someFilter: []
      } as any;
      component['addEventListeners'] = jasmine.createSpy('addEventListeners');
      component['hideSpinner'] = jasmine.createSpy('hideSpinner');
      component['showContent']();
      expect(inplayMainService.clearDeletedEventFromType).toHaveBeenCalled();
      expect(component['hideSpinner']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#showNoEventsSection', () => {
    it('should return true', () => {
      component['dataReady'] = true;
      component['ssError'] = true;
      component['sportSectionData'] = {} as any;
      expect(component.showNoEventsSection('filter')).toBe(true);
    });
    it('should return true if empty array', () => {
      component['dataReady'] = true;
      component['ssError'] = true;
      component['sportSectionData'] = {
        filter: {
          eventsByTypeName: []
        }
      } as any;
      expect(component.showNoEventsSection('filter')).toBe(true);
    });
    it('should return false', () => {
      component['dataReady'] = true;
      component['ssError'] = true;
      component['sportSectionData'] = {
        filter: {
          eventsByTypeName: [1, 2]
        }
      } as any;
      expect(component.showNoEventsSection('filter')).toBe(false);
    });
    it('should return false if data not ready', () => {
      component['dataReady'] = false;
      component['ssError'] = true;
      component['sportSectionData'] = {
        filter: {
          eventsByTypeName: [1, 2]
        }
      } as any;
      expect(component.showNoEventsSection('filter')).toBe(false);
    });
  });

  describe('#reloadComponent', () => {
    it('should call setConnectionErrorState', () => {
      component.ngOnInit();
      component.reloadComponent();
      expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('#reloadComponent', () => {
      spyOn(component, 'ngOnDestroy');
      spyOn(component, 'showSpinner');
      spyOn(component, 'ngOnInit');

      component.reloadComponent();

      expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.ngOnInit).toHaveBeenCalled();
    });
  });
  describe('#isLiveNowFilter', () => {
    it('should return true if the viewfilter[i] of the index of categoryId is 21 and index < 2', () => {
      component.categoryId = 21;
      component.isHR = true;
      component.viewByFilters = ['filter', 'testFilter'];
      expect(component.isLiveNowFilter('testFilter', 1)).toBeTruthy();
    });
    it('should return true if the viewfilter[i] of the index of categoryId is 21 and index < 2', () => {
      component.categoryId = 21;
      component.viewByFilters = ['filter', 'testFilter'];
      expect(component.isLiveNowFilter('filter')).toBeTruthy();
    });
    it('should return false if the viewfilter[0] of the index of categoryId is not 21 and index > 2', () => {
      component.categoryId = 21;
      component.viewByFilters = ['filter', 'testFilter'];
      expect(component.isLiveNowFilter('testFilter', 2)).toBeFalsy();
    });
    it('should return true if the viewfilter[0] of the index of categoryId is 21 and index > 2', () => {
      component.categoryId = 21;
      component.viewByFilters = ['filter', 'testFilter'];
      expect(component.isLiveNowFilter('filter', 3)).toBeTruthy();
    });
  });
});
