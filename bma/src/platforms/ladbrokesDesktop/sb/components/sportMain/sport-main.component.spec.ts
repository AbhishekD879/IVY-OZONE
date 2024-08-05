import { of as observableOf, Subject } from 'rxjs';
import { SportMainComponent } from './sport-main.component';

describe('SportMainComponent', () => {
  let component: SportMainComponent;
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
  let routeSnapshot;
  let coreToolsService;
  let slpSpinnerStateService;
  let germanSupportService;
  let navigationService;
  let windowRefService;
  let dialogService;
  let freeRideHelperService;
  const gtmService = {} as any;

  beforeEach(() => {
    sportConfig = {
      config: {
        defaultTab: 'matches',
        request: {
          categoryId: '15'
        },
        tier: 1
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
        name: 'live',
        displayInConnect: true
      }, {
        id: 'tab-matches',
        label: 'sb.tabsNameInPlay',
        url: '/sport/football/matches',
        name: 'matches',
        displayInConnect: true
      }, {
        id: 'tab-competitions',
        label: 'sb.tabsNameCompetitions',
        url: '/sport/football/competitions',
        name: 'competitions',
        displayInConnect: true
      }]
    };

    cmsService = {
      getSportTabsConfig: jasmine.createSpy('getSportTabsConfig').and.returnValue(observableOf([
        {
          name: 'competitions',
          displayName: 'new competitions'
        },
        {
          name: 'matches',
          displayName: 'new matches'
        }
      ])),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(observableOf({})),
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(observableOf({tabs: []}))
    } as any;
    timeService = {} as any;
    getSportInstanceService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({
        sportConfig,
        getConfig: jasmine.createSpy('getConfig'),
        config: {
          tier: 1
        }
      }))
    } as any;
    routingState = {
      getRouteParam: jasmine.createSpy('getRouteParam'),
      getRouteSegment: jasmine.createSpy('getRouteSegment')
    } as any;
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SPORT_DEFAULT_PAGE: 'SPORT_DEFAULT_PAGE'
      }
    } as any;
    location = {
      path: jasmine.createSpy('path').and.returnValue('https://test.url')
    } as any;
    storage = {
      remove: jasmine.createSpy('remove'),
      get: jasmine.createSpy('get')
    } as any;
    user = {} as any;
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe')
      },
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;
    routeSnapshot = {
      data: {},
      url: [{ path: 'sport' }],
      paramMap: {
        get: jasmine.createSpy('get').and.returnValue(observableOf({}))
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

    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser')
    };
    navigationService = jasmine.createSpyObj('navigationService', ['handleHomeRedirect', 'changeEmittedFromChild']);
    navigationService.changeEmittedFromChild.subscribe =
      jasmine.createSpy('navigationService.changeEmittedFromChild').and.returnValue(true);

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        })
      }
    };

    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };

    const bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    } as any;

    component = new SportMainComponent(cmsService, timeService,
      getSportInstanceService, routingState, pubSubService, location, storage,
      user, router, route, device, germanSupportService,
      sportTabsService, coreToolsService, slpSpinnerStateService,
      navigationService, freeRideHelperService, windowRefService,dialogService,gtmService, bonusSuppressionService);

    component.sport = {
      extendRequestConfig: jasmine.createSpy('extendRequestConfig').and.returnValue(jasmine.any(Function)),
      config: {
        request: {}
      }
    } as any;
    component.goToDefaultPage = jasmine.createSpy().and.callFake(cb => {
      cb();
    });

    component['slpSpinnerStateService'].slpSpinnerStateObservable$ = new Subject();
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  describe('ngOnInit', () => {
    it('should subscribe and initSportTabs on "SESSION_LOGIN", "SUCCESSFUL_LOGIN"', () => {
      component['filterTabs'] = jasmine.createSpy();
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (Array.isArray(b) && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
          cb();
        }
      });

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.channelName,
        [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGIN],
        jasmine.any(Function));
      expect(component['filterTabs']).toHaveBeenCalled();
    });
  });

  describe('#filterTabs', () => {
    it('should filter tabs when matches available', () => {
      component.sportName = 'football';
      component['sportPath'] = 'football';
      germanSupportService.isGermanUser.and.returnValue(true);
      const result = component['filterTabs']([{
        id: 'tab-jackpot',
        label: 'jackpot',
        url: '/sport/football/jackpot',
        hidden: false,
        name: 'jackpot',
        displayInConnect: true
      }]);

      expect(result).toContain({
        id: 'tab-jackpot',
        label: 'jackpot',
        url: '/sport/football/jackpot',
        hidden: true,
        name: 'jackpot',
        displayInConnect: true
      });
    });

    it('should filter tabs when matches available', () => {
      component.sportName = 'football';
      component['sportPath'] = 'football';
      const result = component['filterTabs']([{
        id: 'tab-matches',
        label: 'matches',
        url: '/sport/football',
        hidden: true,
        name: 'matches',
        displayInConnect: true
      }]);

      expect(result).toContain({
        id: 'tab-matches',
        label: 'matches',
        hidden: false,
        url: '/sport/football/matches/today',
        name: 'matches',
        displayInConnect: true
      });

      expect(result).toContain({
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        hidden: false,
        url: '/sport/football/live',
        name: 'live',
        sortOrder: 1
      });
      expect(component['defaultTab']).toEqual('matches');
    });

    it('should filter tabs when live available', () => {
      const result = component['filterTabs']([{
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        hidden: true,
        url: '/sport/football/live',
        name: 'live',
        displayInConnect: true
      }]);

      expect(result).toEqual([{
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        hidden: false,
        url: '/sport/football/live',
        name: 'live',
        displayInConnect: true
      }]);
    });

    it('should filter tabs when live for golf', () => {
      component.sportId = '18'
      component['filterTabs']([{
        id: 'tab-live',
        label: 'sb.tabsNameInPlay',
        hidden: true,
        url: '/sport/football/live',
        name: 'live',
        displayInConnect: true
      }]);

      expect(component['defaultTab']).toBeUndefined();
    });
  });

  describe('#setDefaultTab', () => {
    it('setDefaultTab', ()=> {
      const sportTabs = [{name: 'matches' , hidden: false}]
      component['setDefaultTab'](sportTabs as any);
      expect(component['defaultTab']).toBe('matches')
    })
    it('setDefaultTab with out sportTabs', ()=> {
      const sportTabs = [{name: 'matches' , hidden: true}]
      component['setDefaultTab'](sportTabs as any);
      expect(component['defaultTab']).toBeUndefined();
    })
  });
});
