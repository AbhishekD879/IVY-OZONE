import { fakeAsync, tick } from '@angular/core/testing';
import { Observable, of,BehaviorSubject } from 'rxjs';
import { RacingMainComponent } from './racing-main.component';
import { NavigationEnd } from '@angular/router';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { sportEventMock } from '../racingEventMain/racing-event-main.component.mock';

describe('RacingMainComponent', () => {
  let component: RacingMainComponent;

  let activatedRoute, templateService, routingHelperService, routesDataSharingService, gtmService,
    router, horseracingService, greyhoundService, routingState, cmsService, windowRefService, changeDetector,
    pubSubService, navigationService, vEPService;

  let mockedSegment = 'horseracing';
  let unsavedEmaHandler;
  let routeRequestHandler;

  const sConfig = {
    BetFilterHorseRacing: {
      enabled: true
    },
    featuredRaces: {
      enabled: true
    },
    NextRacesToggle: {
      nextRacesComponentEnabled: true
    }
  };

  const horseracingServiceDataMock = {
    getConfig: jasmine.createSpy().and.returnValue({
      name: 'horseracing',
      path: 'horse-racing',
      request: {
        categoryId: '21'
      },
    }
    ),
    getGeneralConfig: jasmine.createSpy().and.returnValue({
      config: {
        request: {
          categoryId: '21'
        },
        sectionTitle:'',
        sportModule: 'Horse Racing'
      },
      tabs: [{
        id: 'races'
      }],
      order: {EVENTS_ORDER: null},

    }),
    configureTabs: jasmine.createSpy().and.returnValue({})
  };

  beforeEach(() => {
    routesDataSharingService = {
      setRacingTabs: jasmine.createSpy('setRacingTabs').and.returnValue({}),
      activeTabId: jasmine.createSpy().and.returnValue(of({})),
      hasSubHeader: jasmine.createSpy().and.returnValue(of({})),
      updatedActiveTabId: jasmine.createSpy()
    };
    horseracingService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(horseracingServiceDataMock),
      isSpecialsAvailable: jasmine.createSpy('isSpecialsAvailable').and.returnValue(of([])),
      groupByFlagCodesAndClassesTypeNames : jasmine.createSpy('groupByFlagCodesAndClassesTypeNames')
    };
    greyhoundService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of([])),
      isSpecialsAvailable: jasmine.createSpy('isSpecialsAvailable').and.returnValue(of([]))
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.callFake(() => mockedSegment)
    };
    activatedRoute = {
      snapshot: {}
    };
    templateService = {
      getIconSport: jasmine.createSpy('getIconSport').and.returnValue(of({ svgId: '', svg: '' }))
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
        if (method === 'TOP_BAR_DATA') {
          callback({
            breadCrumbs: [],
            quickNavigationItems: [],
            sportEventsData: [],
            eventEntity: null,
            meetingsTitle: null
          });
        } else if(method === 'EMA_UNSAVED_ON_EDP'){
          unsavedEmaHandler = callback;
        } else if( method === 'ROUTE_CHANGE_STATUS'){
          routeRequestHandler = callback;
        }
      }),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    router = {
      url: '/horse-racing/featured',
      events: new Observable(observer => {
        const event = new NavigationEnd(0, 'test', 'test1');

        observer.next(event);
        observer.complete();
      }),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(of(false))
    };
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearInterval: jasmine.createSpy(),
        scrollTo: jasmine.createSpy()
      }
    };

    changeDetector = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(sConfig)),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true))
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    vEPService ={
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      getTabs: jasmine.createSpy('getTabs').and.callThrough(),
      findBannerAccordition: jasmine.createSpy('findBannerAccordition').and.callThrough(),
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    }
    navigationService = jasmine.createSpyObj('navigationService', ['changeEmittedFromChild', 'emitChangeSource']);
    navigationService.changeEmittedFromChild.subscribe =
      jasmine.createSpy('navigationService.changeEmittedFromChild').and.returnValue(true);
    component = new RacingMainComponent(activatedRoute, templateService, routingHelperService,
      routesDataSharingService, router, horseracingService, greyhoundService, routingState, cmsService,
      changeDetector, windowRefService, gtmService, pubSubService, navigationService, vEPService);
  });

  it('should hide Error and hide Spinner on Init', fakeAsync(() => {
    component['racingId'] = '19';
    templateService.getIconSport = jasmine.createSpy('getIconSport').and.returnValue(of({
      svgId: '1',
      svg: '<svg></svg>',
    }));
    routesDataSharingService.hasSubHeader = of(true);
    routesDataSharingService.activeTabId = of('races');
    component['initModel'] = jasmine.createSpy('initModel');
    component['applyRacingConfiguration'] = jasmine.createSpy('applyRacingConfiguration');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component['racingInstance'] = {};
    component['racingService'].getSport = jasmine.createSpy('getSport').and.returnValue({} as any);
    component['racingService'].isSpecialsAvailable = jasmine.createSpy('isSpecialsAvailable').and.returnValue(Promise.resolve(true));
    component.ngOnInit();
    tick();

    expect(component.breadcrumbsItems.length).toBe(0);
    expect(component.quickNavigationItems.length).toBe(0);
    expect(component.state.error).toBe(false);
  }));

  it('should not truncate if breadcrumbs name is within given length', fakeAsync(() => {
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
        if (method === 'TOP_BAR_DATA') {
          callback({
            breadCrumbs: [{
              name: 'Prairie Meadows'
            }],
            quickNavigationItems: [],
            eventEntity: null,
            meetingsTitle: null
          } as any);
        }
      }),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
      router, horseracingService, greyhoundService, routingState, cmsService, changeDetector,
      windowRefService, gtmService, pubSubService, navigationService, vEPService);
    component['racingId'] = '19';
    templateService.getIconSport = jasmine.createSpy('getIconSport').and.returnValue(of({
      svgId: '1',
      svg: '<svg></svg>',
    }));
    routesDataSharingService.hasSubHeader = of(true);
    routesDataSharingService.activeTabId = of('races');
    component['initModel'] = jasmine.createSpy('initModel');
    component['applyRacingConfiguration'] = jasmine.createSpy('applyRacingConfiguration');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component['racingInstance'] = {};
    component['racingService'].getSport = jasmine.createSpy('getSport').and.returnValue({} as any);
    component['racingService'].isSpecialsAvailable = jasmine.createSpy('isSpecialsAvailable').and.returnValue(Promise.resolve(true));
    component.ngOnInit();
    tick();

    expect(component.breadcrumbsItems[0].name).toBe('Prairie Meadows');
  }));

  it('should truncate if breadcrumbs name exceeds', fakeAsync(() => {
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
        if (method === 'TOP_BAR_DATA') {
          callback({
            breadCrumbs: [{
              name: 'Indiana Grand Race Course'
            }],
            quickNavigationItems: [],
            sportEventsData: [{...sportEventMock}],
            eventEntity: null,
            meetingsTitle: null
          } as any);
        }
      }),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
      router, horseracingService, greyhoundService, routingState, cmsService, changeDetector,
      windowRefService, gtmService, pubSubService, navigationService, vEPService);
    component['racingId'] = '19';
    templateService.getIconSport = jasmine.createSpy('getIconSport').and.returnValue(of({
      svgId: '1',
      svg: '<svg></svg>',
    }));
    routesDataSharingService.hasSubHeader = of(true);
    routesDataSharingService.activeTabId = of('races');
    component['initModel'] = jasmine.createSpy('initModel');
    component['applyRacingConfiguration'] = jasmine.createSpy('applyRacingConfiguration');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component['racingInstance'] = {};
    component['racingService'].getSport = jasmine.createSpy('getSport').and.returnValue({} as any);
    component['racingService'].isSpecialsAvailable = jasmine.createSpy('isSpecialsAvailable').and.returnValue(Promise.resolve(true));
    component.ngOnInit();
    tick();
    expect(component.sportEventsData.length).toBeGreaterThan(0);
    expect(component['racingService'].groupByFlagCodesAndClassesTypeNames).toHaveBeenCalled();
    expect(component.breadcrumbsItems[0].name).toBe('Indiana Grand Race Course');
  }));

  describe('isDetailPage', () => {
    it(`should return Truthy if currentSegment == 'greyhound.eventMain.market'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('greyhound.eventMain.market');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.eventMain'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.eventMain.market'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain.market');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.eventMain.market.marketType'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain.market.marketType');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'greyhound.eventMain'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('greyhound.eventMain');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.buildYourRaceCard'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.buildYourRaceCard');

      expect(component.isDetailPage).toBeTruthy();
    });

    it(`should return Falsy if currentSegment == ''`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('');

      expect(component.isDetailPage).toBeFalsy();
    });
  });

  describe('isHorseRacingDetailPage', () => {
    it(`should return Truthy if currentSegment == 'horseracing.eventMain'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');

      const response = component['isHorseRacingDetailPage']();
      expect(component.topBarIndex).toBe(1003);
      expect(response).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.eventMain.market'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain.market');

      const response = component['isHorseRacingDetailPage']();
      expect(component.topBarIndex).toBe(1003);
      expect(response).toBeTruthy();
    });

    it(`should return Truthy if currentSegment == 'horseracing.eventMain.market.marketType'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain.market.marketType');

      const response = component['isHorseRacingDetailPage']();
      expect(component.topBarIndex).toBe(1003);
      expect(response).toBeTruthy();
    });

    it(`should return Falsy if currentSegment == ''`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('');

      const response = component['isHorseRacingDetailPage']();
      expect(component.topBarIndex).toBe(7);
      expect(response).toBeFalsy();
    });
  });

  it('should handle EMA_UNSAVED_ON_EDP event', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['RACING_MAIN_COMPONENT'], pubSubService.API.EMA_UNSAVED_ON_EDP, jasmine.any(Function));
  });

  it('unsavedEmaHandler', () => {
    component.ngOnInit();
    unsavedEmaHandler(true);
    expect(component['editMyAccaUnsavedOnEdp']).toEqual(true);
  });

  it('routeRequestHandler', () => {
    component.ngOnInit();
    routeRequestHandler(true);
    expect(component['isRouteRequestSuccess']).toEqual(true);
  });

  describe('canChangeRoute', () => {
    it('should not when editMyAccaUnsavedOnEdp is true', () => {
      component['editMyAccaUnsavedOnEdp'] = false;
      expect(component.canChangeRoute()).toEqual(true);
    });

    it('should when editMyAccaUnsavedOnEdp is false', () => {
      component['editMyAccaUnsavedOnEdp'] = true;
      expect(component.canChangeRoute()).toEqual(false);
    });
  });

  it('onChangeRoute', () => {
    component.onChangeRoute();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  });

  it('showMeetingsList', () => {
    component.showMeetings = false;
    component.sportModule = 'horseracing';
    component.showMeetingsList();

    expect(component.showMeetings).toBeTruthy();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'meetings',
      eventLabel: 'open'
    });
    expect(windowRefService.nativeWindow.scrollTo).toHaveBeenCalledWith(0, 0);

    component.showMeetings = false;
    component.sportModule = '';
    component.showMeetingsList();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'greyhounds',
      eventAction: 'meetings',
      eventLabel: 'open'
    });
  });

  it('initModel during ngonInit', fakeAsync(() => {
    spyOn(component, 'selectTabRacing').and.callThrough();
    component.hideError = jasmine.createSpy('hideError');
    component.hideSpinner = jasmine.createSpy('hideSpinner');

    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['routesDataSharingService'].hasSubHeader = of(false);
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component.racingId = 'testID';
    activatedRoute.snapshot = { params: { display: 'test-today', filter: null  } };
    component.ngOnInit();
    tick();

    expect(component.defaultTab).toEqual('featured');
    expect(component.activeTab).toEqual({ id: 'races' });

    expect(component.config).toEqual(component.racingData[0].getConfig());
    expect(component.isSpecialsPresent).toBeTruthy();
    expect(component.racingName).toEqual('horseracing');
    expect(component.categoryId).toEqual('21');
    expect(component.url).toEqual('/horse-racing/featured');
    expect(component.racingPath).toEqual('horse-racing');
    expect(component.baseUrl).toEqual('/horse-racing');
    expect(component.topBarInnerContent).toEqual(true);
    expect(component.hideError).toHaveBeenCalled();
    expect(component.selectTabRacing).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(component.hideError).toHaveBeenCalled();
  }));

  it('should test initModel when racingData is not an array', () => {
    const racingDataMock = {
      getConfig: jasmine.createSpy('getConfig'),
      getGeneralConfig: jasmine.createSpy().and.returnValue({
        config: {
          request: {
            categoryId: '21'
          },
          sectionTitle:'',
          sportModule: 'Horse Racing'
        },
        tabs: [{
          id: 'races'
        }],
        order: {EVENTS_ORDER: null}
      })
    };
    activatedRoute.snapshot = { params: { display: 'test-today', filter: null } };
    component.racingData = racingDataMock as any;
    component.config = null;
    component.racingName = null;

    component.initModel();

    expect(component.racingPath).toEqual('');
    expect(component.categoryId).toEqual('');
    expect(component.racingInstance).toEqual(racingDataMock);
  });

  it('should test initModel when racingData does not unclude path', () => {
    const racingDataMock = {
      getConfig: jasmine.createSpy('getConfig').and.returnValue({
        path: null,
        request: {}
      }),
      getGeneralConfig: jasmine.createSpy().and.returnValue({
        config: {
          request: {
            categoryId: '21'
          },
          sectionTitle:'',
          sportModule: 'Horse Racing'
        },
        tabs: [{
          id: 'races'
        }],
        order: {EVENTS_ORDER: null}
      })
    };

    component.racingData = racingDataMock as any;
    activatedRoute.snapshot = { params: { display: 'test-today', filter: null  } };
    component.initModel();
    expect(component.racingPath).toEqual('');
  });

  it('#ngOnDestroy', () => {
    navigationService.emitChangeSource = new BehaviorSubject(null);
    component['timeOutListener'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['routeChangeListener'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['racingMainSubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['horseRacingsubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['navigationServiceSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
    expect(component['racingMainSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['horseRacingsubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['navigationServiceSubscription'].unsubscribe).toHaveBeenCalled();
  });

  describe('check for isChildComponentLoaded', () => {
    it('should set isChildComponentLoaded to true if navigationService return true', () => {
      navigationService.changeEmittedFromChild.subscribe = jasmine.createSpy('subscribe').
      and.callFake(cb => cb && cb(true));
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
      if( arg2 === 'RACING_NEXT_RACES_LOADED'){
        fn(true);
      }
      });
      activatedRoute.snapshot = { params: { display: 'test-today', filter: null  } };
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(true);
    });
    it('should set isChildComponentLoaded to false if navigationService return false', () => {
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
        if( arg2 === 'RACING_NEXT_RACES_LOADED'){
          fn(false);
        }
      });
      activatedRoute.snapshot = { params: { display: 'test-today', filter: null  } };
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(false);
    });
    it('should set isChildComponentLoaded to false if navigationService return false', () => {
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
        if( arg2 === 'RACING_NEXT_RACES_LOADED'){
          fn(false);
        }
      });
      activatedRoute.snapshot = { params: { display: 'test-today', filter: null  } };
      router.events =  new Observable(observer => {
          const event = new NavigationEnd(0, 'horse-racing', 'horse-racing');
          event.url = 'horse-racing'
          observer.next(event);
          observer.complete();
        }),
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(false);
    });
    it('should set isChildComponentLoaded to false if navigationService return false', () => {
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
        if( arg2 === 'RACING_NEXT_RACES_LOADED'){
          fn(false);
        }
      });
      activatedRoute.snapshot = { params: { display: 'test-today', filter: null  },
      firstChild: {params: {display: 'gh'}} };
      router.url = 'gh' as any;
      router.events =  new Observable(observer => {
          const event = new NavigationEnd(0, 'horse-racing', 'horse-racing');
          event.url = 'horse-racing'
          observer.next(event);
          observer.complete();
        }),
        // component.route = {snapshot: {firstChild: {params: {display: 'gh'}}}} as any
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(false);
    });
  });

  describe('#selectTabRacing', () => {
    beforeEach(() => {
      component.defaultTab = 'featured-test';
    });
    it('sets active tab', () => {
      spyOn (component, 'getEntryPointsData' as any);
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-featured-test');
    });

    it('sets active tab', () => {
      component.route = {snapshot: {firstChild: {params: {display: 'true'}}}} as any
      spyOn (component, 'getEntryPointsData' as any);
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-true');
    });

    it('sets active tab', () => {
      spyOn (component, 'getEntryPointsData' as any);
      routesDataSharingService.updatedActiveTabId = () => true
      component.defaultTab = false as any;
      component.tabDisplay = null;
      component.isDetailPage = false;
      component.selectTabRacing();
    });

    it('sets active tab', () => {
      spyOnProperty(component, 'tabDisplay').and.returnValue('')
      spyOn (component, 'getEntryPointsData' as any);
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-featured-test');
    });

    it('sets active tab without router url', () => {
      spyOnProperty(component, 'tabDisplay').and.returnValue('')
      spyOn (component, 'getEntryPointsData' as any);
      router = {}
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-featured-test');
    });


    it('sets active tab with routerurl mapping', () => {
      component.route = {snapshot: {firstChild: {params: {display: 'gh'}}}} as any
      router = {url: 'gh'} as any;
      spyOn (component, 'getEntryPointsData' as any);
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-gh');
    });

    it('sets active tab with routerurl mapping', () => {
      component.route = {snapshot: {firstChild: {params: {display: 'gh'}}}} as any
      router['url'] = undefined as any;
      spyOn (component, 'getEntryPointsData' as any);
      component.selectTabRacing();

      expect(component.activeTab.id).toBe('tab-gh');
    });
  });

  describe('getters', () => {
    it('racingService', () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('greyhound.eventMain.market');
      let actualResult = component['racingService'];
      expect(actualResult).toEqual(greyhoundService);

      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing');
      actualResult = component['racingService'];
      expect(actualResult).toEqual(horseracingService);
    });

    describe('getSystemConfig', () => {
      it('isBetFilterLinkAvailable should be true', () => {
        cmsService.getToggleStatus.and.returnValue(of(true));
        routingState.getCurrentSegment.and.returnValue('someSegment');
        component['racingService'].getSport = jasmine.createSpy();
        component['initModel'] = jasmine.createSpy();
        component['applyRacingConfiguration'] = jasmine.createSpy();
        component['selectTabRacing'] = jasmine.createSpy();
        component.getSystemConfig();
        expect(component.offersAndFeaturedRacesTitle ).toEqual('OFFERS AND FEATURED RACES');
        expect(component.nextRacesComponentEnabled).toBeTruthy();
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(component.isBetFilterLinkAvailable).toBeTruthy();
        expect(component.isEnhancedMultiplesEnabled).toBeTruthy();
      });
      it('isBetFilterLinkAvailable should be false', () => {
        sConfig.BetFilterHorseRacing.enabled = false;
        cmsService.getToggleStatus.and.returnValue(of(false));
        routingState.getCurrentSegment.and.returnValue('someSegment');
        component['racingService'].getSport = jasmine.createSpy();
        component['initModel'] = jasmine.createSpy();
        component['applyRacingConfiguration'] = jasmine.createSpy();
        component['selectTabRacing'] = jasmine.createSpy();
        component.getSystemConfig();
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(component.isBetFilterLinkAvailable).toBeFalsy();
        expect(component.isEnhancedMultiplesEnabled).toBeFalsy();
      });
    });

    describe('#tabDisplay', () => {
      it('returns default tab', () => {
        component.defaultTab = 'featured-test';
        const result = component.tabDisplay;

        expect(result).toEqual('featured-test');
      });

      it('returns display param', () => {
        activatedRoute.snapshot.firstChild = { params: { display: 'test-today', filter: null  } };
        const result = component.tabDisplay;

        expect(result).toEqual('test-today');
      });

      it('returns path', () => {
        activatedRoute.snapshot.firstChild = { routeConfig: { path: 'test-next-races' }, params: { display: null, filter: null } };
        const result = component.tabDisplay;

        expect(result).toEqual('test-next-races');
      });
    });
  });
  describe('isRacingLandingPage', () => {
    it('should return true if is redirect for HR LP', () => {
      mockedSegment = 'horseracing';
      expect(component['isRacingLandingPage']()).toEqual(true);
    });
    it('should return true if is redirect for GH LP', () => {
      mockedSegment = 'greyhound';
      expect(component['isRacingLandingPage']()).toEqual(true);
    });
    it('should return false if is not redirect for HR LP', () => {
      mockedSegment = 'horseracing.something';
      expect(component['isRacingLandingPage']()).toEqual(false);
    });
    it('should return false if is not redirect for GH LP', () => {
      mockedSegment = 'greyhound.something';
      expect(component['isRacingLandingPage']()).toEqual(false);
    });
  });
  describe('#getTopBarData', () => {
    it('should fetch breadcrumbs data when dats is present (length > 8)', () => {
      pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'TOP_BAR_DATA') {
            callback({
              breadCrumbs: [{
                name: 'Prairie Meadows'
              }],
              quickNavigationItems: [],
              sportEventsData: [],
              eventEntity: null,
              meetingsTitle: null
            } as any);
          }
        }),
        unsubscribe: jasmine.createSpy(),
        API: pubSubApi
      };
      routingState = {
        getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing.eventMain.market.marketType')
      };
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
        router, horseracingService, greyhoundService, routingState, cmsService, changeDetector,
        windowRefService, gtmService, pubSubService, navigationService,vEPService);
      component['getTopBarData']();
      expect(component.isHRDetailPage).toEqual(true);
      expect(component.isChildComponentLoaded).toEqual(true);
      expect(component.breadcrumbsItems[0].name).toBe('Prairie...');
      expect(component.breadcrumbsItems.length).not.toBe(0);
    });
    it('should fetch breadcrumbs data when dats is present (length < 8)', () => {
      pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'TOP_BAR_DATA') {
            callback({
              breadCrumbs: [{
                name: 'Prairie'
              }],
              quickNavigationItems: [],
              sportEventsData: [],
              eventEntity: null,
              meetingsTitle: null
            } as any);
          }
        }),
        unsubscribe: jasmine.createSpy(),
        API: pubSubApi
      };
      routingState = {
        getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing.eventMain.market.marketType')
      };
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
        router, horseracingService, greyhoundService, routingState, cmsService, changeDetector,
        windowRefService, gtmService, pubSubService, navigationService, vEPService);
      component['getTopBarData']();
      expect(component.isHRDetailPage).toEqual(true);
      expect(component.breadcrumbsItems[0].name).toBe('Prairie');
      expect(component.breadcrumbsItems.length).not.toBe(0);
    });
    it('should not fetch breadcrumbs data when dats is not present', () => {
      pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'TOP_BAR_DATA') {
            callback({
              breadCrumbs: [],
              quickNavigationItems: [],
              sportEventsData: [],
              eventEntity: null,
              meetingsTitle: null
            } as any);
          }
        }),
        unsubscribe: jasmine.createSpy(),
        API: pubSubApi
      };
      routingState = {
        getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('greyhound.eventMain')
      };
      vEPService= {
        targetTab: {subscribe : (cb) => cb()},
        lastBannerEnabled: {subscribe : (cb) => cb()},
        accorditionNumber: {subscribe : (cb) => cb()},
      }
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
        router, horseracingService, greyhoundService, routingState, cmsService, changeDetector,
        windowRefService, gtmService, pubSubService, navigationService, vEPService);
      component['getTopBarData']();
      expect(component.isHRDetailPage).toEqual(true);
      expect(component.breadcrumbsItems).toEqual([]);
    });
  });

  describe('#goToDefaultPage', () => {
    it('when sport is HR and user is on featured tab', () => {
      component.racingName = 'horseracing';
      component.router = {
        url: '/horse-racing',
        navigateByUrl: jasmine.createSpy().and.returnValue('')
      } as any;
      component.racingDefaultPath = '/horse-racing/featured';
      component.goToDefaultPage();
      expect(component.router.navigateByUrl).not.toHaveBeenCalled();
    });
    it('when sport is GH and user is on today tab', () => {
      component.racingName = 'greyhound';
      component.defaultTab = 'today';
      component.router = {
        url: '/greyhound-racing',
        navigateByUrl: jasmine.createSpy().and.returnValue('')
      } as any;
      component.racingDefaultPath = '/greyhound-racing/today';
      component.goToDefaultPage();
      expect(component.router.navigateByUrl).not.toHaveBeenCalled();
    });
    it('when sport is GH and user is on today tab', () => {
      component.racingName = 'greyhound';
      component.defaultTab = 'races';
      component.router = {
        url: '/greyhound-racing',
        navigateByUrl: jasmine.createSpy().and.returnValue('')
      } as any;
      component.racingDefaultPath = '/greyhound-racing/races/next';
      component.goToDefaultPage();
      expect(component.router.navigateByUrl).not.toHaveBeenCalled();
    });
  });

  describe('ngafterviewchecked', () => {
    it('ngAfterViewChecked', () => {
      component.ngAfterViewChecked()
    })
  })

  describe('getEntryPointsData', () => {
    it('getEntryPointsData', fakeAsync(() => {
      component['getEntryPointsData']();
      tick();
    }))

    it('getEntryPointsData', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
        if( arg2 === 'RACING_NEXT_RACES_LOADED'){
          fn(false);
        }
      });
      activatedRoute.snapshot = { params: { display: 'test-today', filter: null  },
      firstChild: {params: {display: 'gh'}} };
      router.url =  undefined as any;
      router.events =  new Observable(observer => {
          const event = new NavigationEnd(0, 'horse-racing', 'horse-racing');
          event.url = 'horse-racing'
          observer.next(event);
          observer.complete();
        }),
      component['getEntryPointsData']();
      tick();
    }))


  })
});
