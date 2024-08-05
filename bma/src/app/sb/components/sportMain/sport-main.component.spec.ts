import { of as observableOf, throwError, Subject, of, BehaviorSubject } from 'rxjs';
import { SportMainComponent } from '@sb/components/sportMain/sport-main.component';
import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';
import { SYC_DATA } from './mockData/sport-main.component.mock';

describe('SportMainComponent', () => {
  let component: SportMainComponent;
  let getRouteSegmentCase = 1;
  let cmsService;
  let timeService;
  let getSportInstanceService;
  let routingState;
  let pubSubService;
  let location;
  let storage;
  let user;
  let router;
  let route;
  let device;
  let sportTabsService;
  let sportConfig;
  let sportConfigContainer;
  let routeSnapshot;
  let coreToolsService;
  let slpSpinnerStateService;
  let routeChangeListener;
  let unsavedEmaHandler;
  let navigationService;
  let windowRefService;
  let dialogService;
  let gtmService;
  const sycData = SYC_DATA;

  beforeEach(() => {
    sportConfig = {
      config: {
        defaultTab: 'matches',
        request: {
          categoryId: '15'
        },
        tier: 1,
        name: 'football',
      },
      filters: {
        VIEW_BY_FILTERS: {},
        LIVE_VIEW_BY_FILTERS: {}
      },
      order: {
        BY_LEAGUE_ORDER: {},
        BY_LEAGUE_EVENTS_ORDER: {},
        BY_TIME_ORDER: {}
      },
      tabs: [{
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        url: '/sport/football/live',
        hidden: true,
        name: 'live',
        displayInConnect: true
      }, {
        id: 'tab-matches',
        label: 'sb.tabsNameInPlay',
        url: '/sport/football/matches',
        hidden: false,
        name: 'matches',
        displayInConnect: true
      }, {
        id: 'tab-competitions',
        label: 'sb.tabsNameCompetitions',
        url: '/sport/football/competitions',
        hidden: false,
        name: 'competitions',
        displayInConnect: true
      }]
    };

    sportConfigContainer = {
      sportConfig: sportConfig,
      getConfig: jasmine.createSpy('getConfig'),
      config: {
        tier: 1
      }
    };

    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(of({ tabs: [] }))
    } as any;
    timeService = {} as any;
    getSportInstanceService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf(sportConfigContainer))
    } as any;
    routingState = {
      getRouteParam: jasmine.createSpy('getRouteParam'),
      getRouteSegment: jasmine.createSpy('getRouteSegment').and.callFake(() => {
        switch (getRouteSegmentCase) {
          case 1:
            return 'sport';
          case 2:
            return 'olympicsSport';
          case 3:
            return 'edp';
        }
      }),
    } as any;
    pubSubService = {
      cbMap: {},
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, handler) => {
        if (method === 'EMA_UNSAVED_ON_EDP') {
          unsavedEmaHandler = handler;
        } else {
          pubSubService.cbMap[method] = handler;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        SPORT_DEFAULT_PAGE: 'SPORT_DEFAULT_PAGE',
        EMA_OPEN_CANCEL_DIALOG: 'EMA_OPEN_CANCEL_DIALOG',
        EMA_UNSAVED_ON_EDP: 'EMA_UNSAVED_ON_EDP',
        SESSION_LOGIN: 'SESSION_LOGIN',
        FANZONE_SYCDATA: 'FANZONE_SYCDATA'
      }
    } as any;
    location = {
      path: jasmine.createSpy('path').and.returnValue('https://test.url')
    } as any;
    storage = {
      remove: jasmine.createSpy('remove'),
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    } as any;
    user = {} as any;
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => {
          routeChangeListener = cb;
        })
      },
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;
    routeSnapshot = {
      data: {},
      url: [{ path: 'sport' }],
      paramMap: {
        get: jasmine.createSpy('get').and.returnValue('football')
      },
      params: {
        sport: 'football'
      }
    } as any;
    route = {
      params: observableOf({
        id: '1',
        sport: 'tennis'
      }),
      snapshot: routeSnapshot
    } as any;
    sportTabsService = {
      storeSportTabs: jasmine.createSpy('storeSportTabs')
    } as any;
    device = {
      isDesktop: false
    } as any;

    coreToolsService = {
      deepClone: jasmine.createSpy('deepClone').and.returnValue(sportConfig.tabs)
    };

    slpSpinnerStateService = {
      clearSpinnerState: jasmine.createSpy('clearSpinnerState'),
      createSpinnerStream: jasmine.createSpy('createSpinnerStream')
    };
    navigationService = jasmine.createSpyObj('navigationService', ['handleHomeRedirect', 'changeEmittedFromChild', 'emitChangeSource']);
    navigationService.changeEmittedFromChild.subscribe =
      jasmine.createSpy('navigationService.changeEmittedFromChild').and.returnValue(true);

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        }), location: {
          href: 'location_href'
        },
      },
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          classList: {
            add: jasmine.createSpy().and.returnValue('fav-icon-active'),
            remove: jasmine.createSpy().and.returnValue('fav-icon-inactive')
          }
        })
      }
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    gtmService = {push: jasmine.createSpy('push')}

    component = new SportMainComponent(cmsService, timeService,
      getSportInstanceService, routingState, pubSubService, location, storage,
      user, router, route, device, sportTabsService, coreToolsService, slpSpinnerStateService,
      navigationService, windowRefService,dialogService,gtmService);

    component.goToDefaultPage = jasmine.createSpy().and.callFake(cb => {
      cb();
    });

    component['slpSpinnerStateService'].slpSpinnerStateObservable$ = new Subject();
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('should redirect if incorrect event id', () => {
    route.params = observableOf({
      id: '/test',
      sport: 'tennis'
    });
    component.ngOnInit();
    expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
  });

  describe('applySportConfiguration', () => {
    it('check sport name for aem baenners when applying sport configuration', () => {
      component.sportBanner = 'prevName';

      component['applySportConfiguration'](sportConfigContainer);

      expect(component.sportBanner).toEqual('football');
    });

    it('check sport name for aem baenners when applying sport configuration', () => {
      component.sportBanner = 'prevName';
      sportConfigContainer.sportConfig.config.name = null;

      component['applySportConfiguration'](sportConfigContainer);

      expect(component.sportBanner).toEqual('prevName');
    });

    it('should call filterTabs', () => {
      sportConfigContainer.sportConfig.config.defaultTab = 'test';
      component['filterTabs'] = jasmine.createSpy('filterTabs');
      component['applySportConfiguration'](sportConfigContainer);
      component['goToDefaultPage']();
      expect(pubSubService.publish).toHaveBeenCalledWith('SPORT_DEFAULT_PAGE');
    });
  });

  describe('#getIsEnhancedMultiplesEnabled', () => {
    it('isEnhancedMultiplesEnabled true', () => {
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeTruthy();
      });
      expect(cmsService.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });

    it('isEnhancedMultiplesEnabled false', () => {
      cmsService.getToggleStatus = jasmine.createSpy().and.returnValue(of(false));
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeFalsy();
      });
      expect(cmsService.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });
  });
  it('changeMatchToggle', () => {
    component.changeMatch = false;
    component.changeMatchToggle();
    expect(component.changeMatch).toBeTruthy();
  });
  it('handleSportEvent with quickSwitchHandler', () => {
    const output = {
      output: 'quickSwitchHandler',
      value: 'someFilter'
    };
    spyOn(component, 'quickSwitchEnabled');
    component.handleSportEvent(output as any);
    expect(component.quickSwitchEnabled).toHaveBeenCalledWith(output.value as any);
  });
  it('handleSportEvent with typeId', () => {
    const output = {
      output: 'typeId',
      value: 'typeId'
    };
    component.handleSportEvent(output as any);
    expect(component.typeId).toBe(output.value);
  });
  it('handleQuickSwitchEvent with closeQuickSwitchPanel emitter', () => {
    const output = {
      output: 'closeQuickSwitchPanel',
      value: true
    };
    component.changeMatch = true;
    component.handleQuickSwitchEvent(output as any);
    expect(component.changeMatch).toBeFalse();
  });
  it('quickSwitchEnabled', () => {
    const flag = '';
    component.quickSwitchEnabled(flag as any);
    expect(component.isQuickSwitchEnabled).toEqual(flag as any)
  })

  describe('#selectTabSport', () => {
    beforeEach(() => {
      component.sportTabs = [{
        id: 'tab-matches',
        label: 'new matches',
        url: '/sport/football/matches',
        name: 'matches',
        displayInConnect: true,
        enabled: true,
        index: 0
      }];
    });
    it('should call selectTabSport method for default tab', () => {
      pubSubService.subscribe.and.callFake((file, methods, callback) => {
        callback();
      });
      component['defaultTab'] = 'matches';
      component['isDefaultUrl'] = jasmine.createSpy('isDefaultUrl').and.returnValue(true);
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      component['selectTabSport']();

      expect(component['setSportTab']).toHaveBeenCalledWith('matches');
    });

    it('should call selectTabSport method for dispay', () => {
      pubSubService.subscribe.and.callFake((file, methods, callback) => {
        callback();
      });
      component['isDefaultUrl'] = jasmine.createSpy('isDefaultUrl').and.returnValue(false);
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      routingState.getRouteParam.and.returnValue('matches');
      component['selectTabSport']();

      expect(component['setSportTab']).toHaveBeenCalledWith('matches');
    });

   
    

    it('should call selectTabSport method when no display and default tab', () => {
      pubSubService.subscribe.and.callFake((file, methods, callback) => {
        callback();
      });

      routingState.getRouteParam.and.returnValue(null);
      component['isDefaultUrl'] = jasmine.createSpy('isDefaultUrl').and.returnValue(false);
      component['setSportTab'] = jasmine.createSpy('setSportTab');

      component['selectTabSport']();

      expect(component['setSportTab']).not.toHaveBeenCalled();
    });

    it('should call selectTabSport method when tab is not active', fakeAsync(() => {
      component['processUrl'] = jasmine.createSpy('processUrl');
      routingState.getRouteParam.and.returnValue('competitions');
      component['selectTabSport']();

      tick();

      expect(component['processUrl']).not.toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['matches'], { relativeTo: jasmine.any(Object) });
    }));

    it('should call selectTabSport method when tab is active', () => {
      component['processUrl'] = jasmine.createSpy('processUrl');
      routingState.getRouteParam.and.returnValue('matches');
      component['selectTabSport']();

      expect(component['processUrl']).toHaveBeenCalledWith('matches');
    });

    it('should redirect to matches tab', fakeAsync(() => {

      component['defaultTab'] = 'matches';
      component.sportTabs = [{
        id: 'tab-matches',
        label: 'new matches',
        url: '/sport/football/matches',
        name: 'matches',
        displayInConnect: true,
        enabled: true,
        index: 0
      },
      {
        id: 'tab-specials',
        label: 'new specials',
        url: '/sport/specials',
        name: 'specials',
        displayInConnect: true,
        enabled: true,
        hidden: true,
        index: 0
      }];
      component['processUrl'] = jasmine.createSpy('processUrl');
      routingState.getRouteParam.and.returnValue('specials');
      component['selectTabSport']();

      tick();

      expect(component['processUrl']).not.toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['matches'], { relativeTo: jasmine.any(Object) });
    }));
  });

  describe('@processUrl', () => {
    it('should navigate if tab is exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual({ id: 'tab-matches' });
    });

    it('should check if it is default url and navigate if tab does not exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['router'] = {url: `/sport/football`} as any;
      component['sportName'] = 'football';
      component.initialStorageTab = 'matches';
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual({ id: 'tab-matches' });
      expect(component['defaultTab']).toBe('matches');
    });

    it('should check if it is default url and navigate if tab exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['router'] = {url: `/sport/football`} as any;
      component['sportName'] = 'football';
      component.initialStorageTab = 'matches';
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      component['getSportTab'] = jasmine.createSpy('getSportTab').and.returnValue('matches');
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual({ id: 'tab-matches' });
      expect(component['defaultTab']).toBe('matches');
    });

    it('should check if it is default url, router url is base url and navigate if tab exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['router'] = {url: `/sport/football`} as any;
      component['baseUrl'] = `/sport/football`;
      component['sportName'] = 'football';
      component.initialStorageTab = 'matches';
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      component['getSportTab'] = jasmine.createSpy('getSportTab').and.returnValue('matches');
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual({ id: 'tab-matches' });
      expect(component['defaultTab']).toBe('matches');
    });

    it('should call setSportTab when defaultUrl is null and display is set', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['defaultTab'] = 'matches';
      component['isDefaultUrl'] = jasmine.createSpy('isDefaultUrl').and.returnValue(true);
      component['shouldNavigatedToTab'] = jasmine.createSpy('shouldNavigatedToTab').and.returnValue(false);
      component['setSportTab'] = jasmine.createSpy('setSportTab');
      component['processUrl']('');

      expect(component.sportActiveTab).toEqual({ id: 'tab-matches' });
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('should NOT navigate if tab is NOT exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['defaultTab'] = undefined;
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual(undefined);
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('should NOT navigate if tab is NOT exist', () => {
      routingState.getRouteSegment.and.returnValue('sport');
      component['defaultTab'] = undefined;
      component['processUrl']('matches');

      expect(component.sportActiveTab).toEqual(undefined);
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });

  describe('#setGtmData', () => {  
    it('calling GTM service', () => {
      component['tabName'] = 'open bets';
      component.gtmDataOnSelectedTabLoads();
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
  });

  describe('isHomeUrl', () => {
    it('should return true for sport segment', () => {
      getRouteSegmentCase = 1;
      const isHomeUrl = component.isHomeUrl();
      expect(routingState.getRouteSegment).toHaveBeenCalledWith('segment', routeSnapshot);
      expect(isHomeUrl).toEqual(true);
    });
    it('should return true for olympic sport segment', () => {
      getRouteSegmentCase = 2;
      const isHomeUrl = component.isHomeUrl();
      expect(routingState.getRouteSegment).toHaveBeenCalledWith('segment', routeSnapshot);
      expect(isHomeUrl).toEqual(true);
    });
    it('should return true for not sport and olympic sport segment', () => {
      getRouteSegmentCase = 3;
      const isHomeUrl = component.isHomeUrl();
      expect(routingState.getRouteSegment).toHaveBeenCalledWith('segment', routeSnapshot);
      expect(isHomeUrl).toEqual(false);
    });
  });

  describe('shouldNavigatedToTab', () => {
    it('should return true for home page and not vertical', () => {
      getRouteSegmentCase = 1;
      expect(component['shouldNavigatedToTab']()).toEqual(true);
    });
  });

  describe('#filterTabs', () => {
    it('should filter tabs when matches available', () => {
      const result = component['filterTabs']([{
        id: 'tab-matches',
        label: 'matches',
        url: '/sport/football/matches',
        hidden: false,
        name: 'matches',
        displayInConnect: true
      }]);

      expect(result).toEqual([{
        id: 'tab-matches',
        label: 'matches',
        hidden: false,
        url: '/sport/football/matches',
        name: 'matches',
        displayInConnect: true
      }]);
      expect(component['defaultTab']).toEqual('matches');
    });

    it('should filter tabs when matches is not available', () => {
      const result = component['filterTabs']([{
        id: 'tab-competitions',
        label: 'competitions',
        url: '/sport/football/competitions',
        name: 'competitions',
        displayInConnect: true
      }]);

      expect(result).toEqual([{
        id: 'tab-competitions',
        label: 'competitions',
        url: '/sport/football/competitions',
        name: 'competitions',
        displayInConnect: true
      }]);
      expect(component['defaultTab']).toEqual('competitions');
    });

    it('should filter tabs when no tabs from cms', () => {
      component['filterTabs']([]);

      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
      expect(component['defaultTab']).not.toBeDefined();
    });

    it('should add live tab to tabs for desktop', () => {
      device.isDesktop = true;

      const result = component['filterTabs']([{
        id: 'tab-matches',
        label: 'sb.tabsNameMatches',
        url: '/sport/football/matches',
        name: 'matches',
        displayInConnect: true
      },
      {
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        url: '/sport/football/live',
        name: 'live'
      }]);

      expect(result.length).toEqual(2);
    });
  });

  describe('redirect to /', () => {
    it('should redirect to / if incorrect sport name', () => {
      getSportInstanceService.getSport.and.returnValue(throwError(''));
      component.ngOnInit();
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });

    it('should redirect to / if incorrect sport name', () => {
      getSportInstanceService.getSport.and.returnValue(observableOf({}));
      component.ngOnInit();
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });
  });

  it('should call favIconDown', () => {
    component.favIconDown();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('fav-icon');
  })

  it('should call favIconUp', () => {
    component.favIconUp();
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('fav-icon');
  })

  describe('ngOnInit', () => {
    beforeEach(() => {
      route.params = new Subject();
    });

    it('should not reload component if sport name and event id is the same as stored sport name', () => {
      const sportName = 'tennis';
      const eventId = '123';

      routingState.getRouteParam.and.callFake(key => key === 'sport' ? sportName : eventId);
      component.ngOnInit();

      route.params.next({ sport: sportName, id: eventId });

      expect(getSportInstanceService.getSport).toHaveBeenCalledTimes(1);
    });

    it('should not reload component if sport name is the different as stored sport name', () => {
      const sportName = 'tennis';
      const eventId = '123';

      routingState.getRouteParam.and.callFake(key => key === 'sport' ? 'football' : eventId);
      component.ngOnInit();

      route.params.next({ sport: sportName, id: eventId });

      expect(getSportInstanceService.getSport).toHaveBeenCalledTimes(1);
    });

    it('should not reload component if event id is the different as stored event id', () => {
      const sportName = 'tennis';
      const eventId = '123';

      routingState.getRouteParam.and.callFake(key => key === 'sport' ? sportName : '124');
      component.ngOnInit();

      route.params.next({ sport: sportName, id: eventId });

      expect(getSportInstanceService.getSport).toHaveBeenCalledTimes(1);
    });

    it('should not reload component if event id is not present', () => {
      const sportName = 'tennis';

      routingState.getRouteParam.and.callFake(key => key === 'sport' ? sportName : 'tennis');

      component = new SportMainComponent(cmsService, timeService,
        getSportInstanceService, routingState, pubSubService, location, storage,
        user, router, route, device, sportTabsService, coreToolsService, slpSpinnerStateService,
        navigationService, windowRefService,dialogService,gtmService);

      component.ngOnInit();

      route.params.next({ sport: sportName, id: null });

      expect(getSportInstanceService.getSport).toHaveBeenCalledTimes(1);
    });

    it('should handle EMA_UNSAVED_ON_EDP event', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('sportMain', pubSubService.API.EMA_UNSAVED_ON_EDP, jasmine.any(Function));
    });

    it('routeChangeListener', () => {
      component.ngOnInit();
      routeChangeListener(new NavigationEnd(0, 'test', 'test'));
      expect(routingState.getRouteParam).toHaveBeenCalledWith('display', component['route'].snapshot);
      expect(routingState.getRouteParam).toHaveBeenCalledWith('display', component['route'].snapshot);
    });
    it('routeChangeListener when display is undefined', () => {
      component['display'] = undefined;
      component.ngOnInit();
      routeChangeListener(new NavigationEnd(0, 'test', 'test'));
      expect(component.isChildComponentLoaded).toBe(false);
    });
    it('routeChangeListener when display is matches', () => {
      routingState.getRouteParam.and.returnValue('matches');
      component['display'] = 'matches';
      component.ngOnInit();
      routeChangeListener(new NavigationEnd(0, 'matches', 'matches'));
      expect(routingState.getRouteParam).toHaveBeenCalledWith('display', component['route'].snapshot);
      expect(component.isChildComponentLoaded).toBe(true);
    });
    it('routeChangeListener when display is competitions', () => {
      routingState.getRouteParam.and.returnValue('competitions');
      component['display'] = 'competitions';
      component.ngOnInit();
      routeChangeListener(new NavigationEnd(0, 'competitions', 'competitions'));
      expect(routingState.getRouteParam).toHaveBeenCalledWith('display', component['route'].snapshot);
      expect(component.isChildComponentLoaded).toBe(false);
    });
    it('routeChangeListener when display is not matches and competitions', () => {
      routingState.getRouteParam.and.returnValue('special');
      component['display'] = 'special';
      component.ngOnInit();
      routeChangeListener(new NavigationEnd(0, 'special', 'special'));
      expect(routingState.getRouteParam).toHaveBeenCalledWith('display', component['route'].snapshot);
      expect(component.isChildComponentLoaded).toBe(true);
    });

    it('routeChangeListener sportPath', () => {
      component.ngOnInit();
      routingState.getRouteParam.and.returnValue('test');
      component['sportPath'] = 'test';
      component['processUrl'] = jasmine.createSpy('processUrl');
      routeChangeListener(new NavigationEnd(0, 'test', 'test'));
      expect(component['processUrl']).toHaveBeenCalled();
    });

    it('routeChangeListener !NavigationEnd', () => {
      component.ngOnInit();
      routeChangeListener({});
      expect(routingState.getRouteParam).not.toHaveBeenCalledTimes(4);
    });

    it('should call filter Tabs method', () => {
      component.ngOnInit();
      routingState.getRouteParam.and.returnValue(null);
      component['filterTabs'] = jasmine.createSpy('filterTabs');
      routeChangeListener(new NavigationEnd(0, 'test', 'test'));      
      expect(component['filterTabs'] ).toHaveBeenCalled();
    });

    it('unsavedEmaHandler', () => {
      component.ngOnInit();
      unsavedEmaHandler(true);
      expect(component['editMyAccaUnsavedOnEdp']).toEqual(true);
    });
  });

  describe('#ngOnDestroy', () => {
    it('should ngOnDestroy', () => {
      navigationService.emitChangeSource = new BehaviorSubject(null);
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sportMain');
      expect(slpSpinnerStateService.clearSpinnerState).toHaveBeenCalled();
    });

    it('should ngOnDestroy and usubscribe', () => {
      navigationService.emitChangeSource = new BehaviorSubject(null);
      component['routeParamsListener'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['routeChangeListener'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['navigationServiceSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['routeParamsListener'].unsubscribe).toHaveBeenCalled();
      expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['navigationServiceSubscription'].unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sportMain');
      expect(slpSpinnerStateService.clearSpinnerState).toHaveBeenCalled();
    });
  });

  describe('check for isChildComponentLoaded', () => {
    it('should set isChildComponentLoaded to true if navigationService return true', () => {
      navigationService.changeEmittedFromChild.subscribe = jasmine.createSpy('subscribe').
        and.callFake(cb => cb && cb(true));
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(true);
    });
    it('should set isChildComponentLoaded to false if navigationService return false', () => {
      navigationService.changeEmittedFromChild.subscribe = jasmine.createSpy('subscribe').
        and.callFake(cb => cb && cb(false));
      component.ngOnInit();
      expect(component.isChildComponentLoaded).toBe(false);
    });
  });

  describe('#getSportUri', () => {
    it('should return sport uri for mobile', () => {
      const sportUrl = 'sport/';
      const actualResult = component['getSportUri'](sportUrl);

      expect(actualResult).toEqual(`${sportUrl}football`);
    });

    it('should return sport uri for desktop', () => {
      device.isDesktop = true;
      const sportUrl = 'sport/';
      const actualResult = component['getSportUri'](sportUrl);

      expect(actualResult).toEqual(`${sportUrl}football/matches/today`);
    });
  });

  describe('#checkTabs', () => {
    it('should redirect to home page, when no tabs', () => {
      component['checkTabs']([]);
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });
    it('should redirect to home page, when all tabs are hidden', () => {
      component['checkTabs']([{ label: 'matches', hidden: true }, { label: 'competitions', hidden: true }]);
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });
  });

  describe('loadSportData', () => {
    beforeEach(() => {
      component['initModel'] = jasmine.createSpy('initModel');
      component['applySportConfiguration'] = jasmine.createSpy('applySportConfiguration');
      component['selectTabSport'] = jasmine.createSpy('selectTabSport');
      component['hideSpinner'] = jasmine.createSpy('hideSpinner');
      component['showSpinner'] = jasmine.createSpy('showSpinner');
    });

    it('should get sport config instance', () => {
      component['loadSportData']();

      expect(getSportInstanceService.getSport).toHaveBeenCalledWith('football', false);
      expect(component['initModel']).toHaveBeenCalled();
      expect(component['applySportConfiguration']).toHaveBeenCalledWith(sportConfigContainer);
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.showSpinner).not.toHaveBeenCalled();
    });

    it('should redirect to / if incorrect sport name', () => {
      getSportInstanceService.getSport.and.returnValue(throwError(''));
      component['loadSportData']();
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });

    it('should redirect to / if incorrect sport name', () => {
      getSportInstanceService.getSport.and.returnValue(observableOf({}));
      component['loadSportData']();
      expect(navigationService.handleHomeRedirect).toHaveBeenCalledWith('slp');
    });
  });

  describe('initLazyHandler', () => {
    it(`should set True for isLazyComponentLoaded`, () => {
      component.isLazyComponentLoaded = false;

      component.initLazyHandler();
      expect(component.isLazyComponentLoaded).toBeTruthy();
    });
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

  describe('setSportTab', () => {
    it('setSportTab', () => {
      user.status = true;
      user.username = 'qa';
      component['shouldSaveTab'] = true;
      component['baseUrl'] = 'test';
      component['setSportTab']('tab1');
      expect(storage.set).toHaveBeenCalledWith('test-tab-qa', 'tab1');
    });

    it('setSportTab', () => {
      user.username = 'qa';
      component['setSportTab']('tab1');
      expect(storage.set).not.toHaveBeenCalled();
    });
  });

  it('processUrl (!shouldNavigatedToTab)', () => {
    component['sportName'] = 'football';
    component['defaultTab'] = 'test';
    getRouteSegmentCase = 3;
    component['processUrl']('test');
    expect(component['sportActiveTab']).toEqual({ id: 'tab-test' });
  });

  it('getSportTab', () => {
    storage.get.and.returnValue('tab2');
    component['shouldSaveTab'] = true;
    user.status = true;
    user.username = 'qa';
    component['baseUrl'] = 'test';
    component.sportTabs = <any>[
      {
        name: 'tab1',
        hidden: true
      },
      {
        name: 'tab2',
        hidden: false
      }
    ];

    expect(component['getSportTab']()).toEqual('tab2');
  });

  it('processUrl Should call golf_matches', () => {
    component['sportName'] = 'football';
    component['defaultTab'] = 'test';
    getRouteSegmentCase = 3;
    routeSnapshot['_routerState'] = {url: 'golf_matches'};
    component['processUrl']('test');
    expect(component['sportActiveTab']).toEqual({ id: 'tab-test' });
  });

  it('processUrl Should call matches', () => {
    component['sportName'] = 'golf';
    component['defaultTab'] = 'test';
    getRouteSegmentCase = 3;
    routeSnapshot['_routerState'] = {url: 'matches'};
    component['processUrl']('test', 'event' as any) as any;
    expect(component['sportActiveTab']).toEqual({ id: 'tab-test' });
  });
});
