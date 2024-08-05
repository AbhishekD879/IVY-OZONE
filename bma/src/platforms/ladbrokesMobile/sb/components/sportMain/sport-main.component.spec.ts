import { of as observableOf } from 'rxjs';
import { SportMainComponent } from './sport-main.component';

describe('LadbrokesSportMainComponent', () => {
  let component: SportMainComponent;
  let freeRideHelperService;

  const sportConfig = {
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

  const cmsService = {
    getSportTabsConfig: jasmine.createSpy('getSportTabsConfig'),
    getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(observableOf({}))
  } as any;
  const timeService = {} as any;
  const getSportInstanceService = {
    getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({}))
  } as any;
  const routingState = {
    getRouteParam: jasmine.createSpy('getRouteParam'),
    getRouteSegment: jasmine.createSpy('getRouteSegment')
  } as any;
  const pubSubService = {
    publish: jasmine.createSpy('publish'),
    API: {
      SESSION_LOGIN: 'SESSION_LOGIN',
      SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
      SPORT_DEFAULT_PAGE: 'SPORT_DEFAULT_PAGE'
    },
    subscribe: jasmine.createSpy()
  } as any;
  const location = {
    path: jasmine.createSpy('path').and.returnValue('https://test.url')
  } as any;
  const storage = {
    remove: jasmine.createSpy('remove'),
    get: jasmine.createSpy('get')
  } as any;
  const user = {} as any;
  const router = {
    events: {
      subscribe: jasmine.createSpy('subscribe')
    },
    navigate: jasmine.createSpy('navigate'),
    navigateByUrl: jasmine.createSpy('navigateByUrl')
  } as any;
  const routeSnapshot = {
    data: {},
    url: [{ path: 'sport' }],
    paramMap: {
      get: jasmine.createSpy('get').and.returnValue(observableOf({}))
    },
    params: {
      sport: 'football'
    }
  } as any;
  const route = {
    params: observableOf({
      id: '1',
      sport: 'tennis'
    }),
    snapshot: routeSnapshot
  } as any;
  const sportTabsService = {
    storeSportTabs: jasmine.createSpy('storeSportTabs')
  } as any;
  const device = {
    isDesktop: false
  } as any;
  const germanSupportService = {
    isGermanUser: jasmine.createSpy('isGermanUser')
  } as any;

  const coreToolsService = {
    deepClone: jasmine.createSpy('deepClone').and.returnValue(sportConfig.tabs)
  } as any;

  const slpSpinnerStateService = {} as any;
  const windowRefService = {
    nativeWindow: {
      setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
        callback();
      })
    }
  } as any;

  let navigationService;
  const dialogService = {
    openDialog: jasmine.createSpy('openDialog')
  }as any ;
  const gtmService = {} as any;

  const bonusSuppressionService = {
    checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
  } as any;

  beforeEach(() => {
    navigationService = jasmine.createSpyObj('navigationService', ['handleHomeRedirect', 'changeEmittedFromChild']);
    navigationService.changeEmittedFromChild.subscribe =
      jasmine.createSpy('navigationService.changeEmittedFromChild').and.returnValue(true);

    component = new SportMainComponent(cmsService, timeService,
      getSportInstanceService, routingState, pubSubService, location, storage,
      user, router, route, device, germanSupportService, sportTabsService, coreToolsService, slpSpinnerStateService,
      freeRideHelperService, navigationService, windowRefService,dialogService,gtmService, bonusSuppressionService);

    component.sport = {
      extendRequestConfig: jasmine.createSpy('extendRequestConfig').and.returnValue(jasmine.any(Function)),
      config: {
        request: {}
      }
    } as any;
    component.goToDefaultPage = jasmine.createSpy().and.callFake(cb => {
      cb();
    });
  });

  describe('ngOnInit', () => {
    it('should subscribe and initSportTabs on "SESSION_LOGIN", "SUCCESSFUL_LOGIN"', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (Array.isArray(b) && (b[0] === 'SUCCESSFUL_LOGIN' || b[0] === 'SESSION_LOGIN')) {
          cb();
        }
      });
      component['filterTabs'] = jasmine.createSpy();

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.channelName,
        [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGIN],
        jasmine.any(Function));
      expect(component['filterTabs']).toHaveBeenCalled();
    });
  });

  describe('#filterTabs', () => {
    it('should filter jackpot tabs when german user', () => {
      component.sportName = 'football';
      germanSupportService.isGermanUser.and.returnValue(true);
      const result = component['filterTabs']([{
        id: 'tab-jackpot',
        label: 'jackpot',
        url: '/sport/football/jackpot',
        hidden: false,
        name: 'jackpot',
        displayInConnect: true
      }]);

      expect(result).toEqual([{
        id: 'tab-jackpot',
        label: 'jackpot',
        url: '/sport/football/jackpot',
        hidden: true,
        name: 'jackpot',
        displayInConnect: true
      }]);
    });
  });
});
