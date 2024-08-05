import { Observable, of,BehaviorSubject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';
import { RacingMainComponent } from './racing-main.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { sportEventMock } from '@app/racing/components/racingEventMain/racing-event-main.component.mock';

describe('RacingMainComponent', () => {
  let component: RacingMainComponent;
  let routingState,
      templateService,
      activatedRoute,
      routingHelperService,
      routesDataSharingService,
      router,
      horseracingService,
      greyhoundService,
      cmsService,
      userService,
      changeDetector,
      windowRefService,
      freeRideHelperService,
      gtmService,
      navigationService,
      pubSubService,
      routeRequestHandler,
      unsavedEmaHandler,
      bonusSuppressionService,
      vEPService;

  const sConfig = {
    BetFilterHorseRacing: {
      enabled: true
    },
    featuredRaces: {
      enabled: true
    },
    NextRacesToggle: {
      nextRacesComponentEnabled: true,
      nextRacesTabEnabled: false
    }
  };

  beforeEach(() => {
    activatedRoute = {} as any;
    templateService = {
      getIconSport: jasmine.createSpy('getIconSport').and.returnValue(of({}))
    };
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(of(''))
    } as any;
    routesDataSharingService = {
      setRacingTabs: jasmine.createSpy('setRacingTabs')
    } as any;
    router = {
      url: '/horse-racing/featured',
      events: new Observable(observer => {
        const event = new NavigationEnd(0, 'test', 'test');

        observer.next(event);
        observer.complete();
      }),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;
    horseracingService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of([])),
      isSpecialsAvailable: jasmine.createSpy('isSpecialsAvailable').and.returnValue(of([])),
      groupByFlagCodesAndClassesTypeNames : jasmine.createSpy('groupByFlagCodesAndClassesTypeNames')
    } as any;
    greyhoundService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of([])),
      isSpecialsAvailable: jasmine.createSpy('isSpecialsAvailable').and.returnValue(of([]))
    } as any;
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horceracing')
    };
    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(sConfig))
    } as any;
    changeDetector = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy()
    } as any;
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval')
      }
    } as any;

    routingState = {
      getCurrentSegment: jasmine.createSpyObj(['getCurrentSegment']),
      getRouteSegment: jasmine.createSpy('getRouteSegment').and.returnValue('greyhound.display')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
        if (method === 'TOP_BAR_DATA') {
          callback({
            breadCrumbs: [],
            quickNavigationItems: [],
            sportEventsData: [{...sportEventMock as any}],
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

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    } as any;

    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    }

    navigationService = jasmine.createSpyObj('navigationService', ['changeEmittedFromChild', 'emitChangeSource']);
    navigationService.changeEmittedFromChild.subscribe =
      jasmine.createSpy('navigationService.changeEmittedFromChild').and.returnValue(true);
    component = new RacingMainComponent(
      activatedRoute,
      templateService,
      routingHelperService,
      routesDataSharingService,
      router,
      horseracingService,
      greyhoundService,
      routingState,
      cmsService,
      userService,
      changeDetector,
      windowRefService,
      freeRideHelperService,
      gtmService,
      pubSubService,
      navigationService,
      bonusSuppressionService,
      vEPService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');

    component.ngOnInit();
    expect(component.addChangeDetection).toHaveBeenCalled();
    expect(component.breadcrumbsItems.length).toBe(0);
  });

  it('should handle EMA_UNSAVED_ON_EDP event', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['RACING_MAIN_COMPONENT'], pubSubService.API.EMA_UNSAVED_ON_EDP, jasmine.any(Function));
  });

  it('unsavedEmaHandler', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    
    component.ngOnInit();
    unsavedEmaHandler(true);
    expect(component['editMyAccaUnsavedOnEdp']).toEqual(true);
  });

  it('routeRequestHandler', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    
    component.ngOnInit();
    routeRequestHandler(true);
    expect(component['isRouteRequestSuccess']).toEqual(true);
  });

  it('isNextRacesTabEnabled', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component.initModel = jasmine.createSpy().and.returnValue(null);
    component.racingName = 'horseracing';
    component.ngOnInit();
    expect(component.initialTab).toBe('today');
    sConfig.NextRacesToggle.nextRacesTabEnabled = true;
    component.ngOnInit();
    expect(component.initialTab).toBe('races');
  });

  it('defaultTab with racingName as GH', () => {
    component.addChangeDetection = jasmine.createSpy();
    component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
    component['routesDataSharingService'].activeTabId = of('races');
    component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
    component.initModel = jasmine.createSpy().and.returnValue(null);
    component.racingName = 'greyhound';
    component.ngOnInit();
    expect(component.defaultTab).toBe('today');
  });

  describe('#ngoninit breadcrumbs data', () => {
    it('breadcrumbs name is within the length', () => {
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
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
        router, horseracingService, greyhoundService, routingState, cmsService,
        userService, changeDetector, windowRefService, freeRideHelperService, gtmService, pubSubService, navigationService, bonusSuppressionService, vEPService);
      component.addChangeDetection = jasmine.createSpy();
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
      component['routesDataSharingService'].activeTabId = of('races');
      component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');

      component.ngOnInit();
      expect(component.breadcrumbsItems.length).not.toBe(0);
      expect(component.isChildComponentLoaded).toEqual(true);
      expect(component.breadcrumbsItems[0].name).toBe('Prairie');
    });
    it('breadcrumbs name exceeds the length', () => {
      pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'TOP_BAR_DATA') {
            callback({
              breadCrumbs: [{
                name: 'Indiana Grand Race Course'
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
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService,
         routesDataSharingService, router, horseracingService, greyhoundService, routingState, cmsService,
        userService, changeDetector, windowRefService, freeRideHelperService, gtmService, pubSubService, navigationService, bonusSuppressionService, vEPService);

      component.addChangeDetection = jasmine.createSpy();
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
      component['routesDataSharingService'].activeTabId = of('races');
      component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');

      component.ngOnInit();
      expect(component.breadcrumbsItems[0].name).toBe('Indiana...');
    });
    it('breadcrumbs name is Greyhounds today tab', () => {
      pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'TOP_BAR_DATA') {
            callback({
              breadCrumbs: [{
                name: 'Greyhounds'
              }, {
                name: 'Indiana Grand Race Course'
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
      component = new RacingMainComponent(activatedRoute, templateService, routingHelperService, routesDataSharingService,
        router, horseracingService, greyhoundService, routingState, cmsService,
        userService, changeDetector, windowRefService, freeRideHelperService, gtmService, pubSubService, navigationService, bonusSuppressionService, vEPService);
      component.addChangeDetection = jasmine.createSpy();
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
      component['routesDataSharingService'].activeTabId = of('races');
      component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
      component.defaultTab = 'today';
      component.ngOnInit();
      expect(component.breadcrumbsItems[0].name).toBe('Greyhounds');
      expect(component.breadcrumbsItems[0].targetUri).toBe('/greyhound-racing/today');

      component.defaultTab = 'races';
      component.ngOnInit();
      expect(component.breadcrumbsItems[0].targetUri).toBe('/greyhound-racing/races/next');
    });
  });

  describe('isDetailPage', () => {
    it(`should return Truthy if currentSegment == 'greyhound.eventMain.market'`, () => {
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('greyhound.eventMain.market');

      expect(component.isDetailPage).toBeTruthy();
    });
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
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
      component['routesDataSharingService'].activeTabId = of('races');
      component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(true);
    });
    it('should set isChildComponentLoaded to false if navigationService return false', () => {
      navigationService.changeEmittedFromChild.subscribe = jasmine.createSpy('subscribe').
      and.callFake(cb => cb && cb(false));
      pubSubService.subscribe.and.callFake((arg0, arg2, fn) => {
        if( arg2 === 'RACING_NEXT_RACES_LOADED'){
          fn(false);
        }
      });
      component['routingState'].getCurrentSegment = jasmine.createSpy().and.returnValue('horseracing.eventMain');
      component['routesDataSharingService'].activeTabId = of('races');
      component['selectTabRacing'] = jasmine.createSpy('selectTabRacing');
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(false);
    });
  });

  it('#ngOnDestroy', () => {
    navigationService.emitChangeSource = new BehaviorSubject(null);
    component['navigationServiceSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component['routeListener'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
    expect(component['routeListener'].unsubscribe).toHaveBeenCalled();
    expect(component['navigationServiceSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('applyRacingConfiguration', fakeAsync(() => {
    const racingInstance = {
      getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
        config: {
          request: {}
        },
        sectionTitle:'',
        sportModule: 'Horse Racing',
        tabs: [{}]
      }),
      configureTabs: jasmine.createSpy('configureTabs')
    };

    component.applyRacingConfiguration(racingInstance);
    tick();

    expect(racingInstance.getGeneralConfig).toHaveBeenCalled();
    expect(racingInstance.configureTabs).toHaveBeenCalled();
    expect(routesDataSharingService.setRacingTabs).toHaveBeenCalled();
    expect(component['racingDefaultPath']).toBeDefined();
  }));
  it('applyRacingConfiguration with racingName as HR', fakeAsync(() => {
    component.racingName = 'horseracing';
    const racingInstance = {
      getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
        config: {
          request: {}
        },
        sectionTitle:'',
        sportModule: 'Horse Racing',
        tabs: [{}]
      }),
      configureTabs: jasmine.createSpy('configureTabs')
    };

    component.applyRacingConfiguration(racingInstance);
    tick();
    expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('horseracing', 'featured');
  }));
  it('applyRacingConfiguration with racingName as GH', fakeAsync(() => {
    component.racingName = 'greyhound';
    const racingInstance = {
      getGeneralConfig: jasmine.createSpy('getGeneralConfig').and.returnValue({
        config: {
          request: {}
        },
        sectionTitle:'',
        sportModule: 'Greyhound Racing',
        tabs: [{}]
      }),
      configureTabs: jasmine.createSpy('configureTabs')
    };

    component.applyRacingConfiguration(racingInstance);
    tick();
    expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('greyhound', 'races/next');

    component.defaultTab = 'today';
    component.applyRacingConfiguration(racingInstance);
    tick();
    expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('greyhound', 'today');
  }));
  it('#isHomeUrl', () => {
    component.router = {
      url: '/greyhound-racing'
    } as any;
    expect(component.isHomeUrl()).toBeTrue();
  })
});
