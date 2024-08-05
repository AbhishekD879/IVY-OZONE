import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { DesktopBmaMainComponent } from './bma-main.component';
import { commandApi } from '@core/services/communication/command/command-api.constant';

describe('DesktopBmaMainComponent', () => {
  let component: DesktopBmaMainComponent;
  let device;
  let user;
  let windowRef;
  let route;
  let locale;
  let nativeBridge;
  let pubsub;
  let pubsubReg;
  let cms;
  let storageService;
  let afterLoginNotifications;
  let navigationService;
  let authService;
  let location;
  let insomnia;
  let gtm;
  let filtersService;
  let coreTools;
  let domSanitizer;
  let rendererService;
  let domTools;
  let router;
  let dialogService;
  let routingState;
  let dynamicComponentLoader;
  let scrollPositions;
  let asyncScriptLoaderService;
  let awsService;
  let sessionStorage;
  let germanSupportService;
  let command;
  let seoDataService;
  let ezNavVanillaService;
  let fanzoneHelperService;
  let changeDetectorRef;
  let fanzoneStorageService;
  let initNetworkIndicatorService;

  beforeEach(() => {
    scrollPositions = {
      scrollTop: 100
    };
    device = {
      isMobile: true,
      isTablet: false,
      isDesktop: false
    };
    user = {
      status: false,
      set: jasmine.createSpy(),
      getJourneyParams: jasmine.createSpy('getJourneyParams').and.returnValue({}),
      canActivateJourney: jasmine.createSpy('canActivateJourney').and.returnValue(false),
      isRouletteJourney: jasmine.createSpy('isRouletteJourney').and.returnValue(false),
      breakRouletteJourney: jasmine.createSpy('breakRouletteJourney')
    };
    seoDataService = {};
    windowRef = {
      document: {
        body: {
          scrollTop: 100
        },
        documentElement: {
          scrollTop: 100
        },
        querySelector: jasmine.createSpy().and.returnValue(scrollPositions),
        getElementById: jasmine.createSpy()
      },
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearTimeout: jasmine.createSpy(),
        scrollBy: jasmine.createSpy(),
        location: {
          href: 'https://sports.coral.co.uk/'
        },
        document: {
          referrer: ''
        }
      }
    };
    route = {
      queryParams: {
        subscribe: jasmine.createSpy()
      },
      snapshot: {
        queryParams: {}
      }
    };
    locale = {};
    nativeBridge = {
      logout: jasmine.createSpy('logout')
    };
    pubsubReg = {};
    pubsub = {
      publish: jasmine.createSpy().and.callFake( (channel) => pubsubReg[channel] && pubsubReg[channel]() ),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((domain, channel, fn) => { pubsubReg[channel] = fn; }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    cms = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue({
        then: jasmine.createSpy().and.returnValue({
          then: jasmine.createSpy().and.returnValue({
            then: jasmine.createSpy().and.returnValue({})
          })
        }),
        subscribe: of({
          Generals: {
            betSlipAnimation: false
          }
        })
      }),
      extractInitialIcons: jasmine.createSpy().and.returnValue(Promise.resolve()),
      getMenuItems: jasmine.createSpy().and.returnValue(of([])),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate')
    };
    storageService = {
      set: jasmine.createSpy(),
      get: jasmine.createSpy(),
      remove: jasmine.createSpy(),
      setCookie: jasmine.createSpy(),
      getCookie: jasmine.createSpy(),
      removeCookie: jasmine.createSpy()
    };
    afterLoginNotifications = {
      start: jasmine.createSpy()
    };
    authService = {
      mainInit: jasmine.createSpy(),
      getTempToken: jasmine.createSpy('getTempToken')
    };
    location = {
      path: jasmine.createSpy().and.returnValue('path')
    };
    insomnia = {
      init: jasmine.createSpy()
    };
    gtm = {
      push: jasmine.createSpy(),
      pushCachedEvents: jasmine.createSpy(),
      pushLogoutInfo: jasmine.createSpy('pushLogoutInfo')
    };
    filtersService = {
      sportCatIcon: jasmine.createSpy()
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy().and.returnValue(false)
    };
    domSanitizer = {};
    rendererService = {
      renderer: {
        listen: jasmine.createSpy(),
        removeClass: jasmine.createSpy()
      }
    };
    domTools = {
      css: jasmine.createSpy(),
      scrollPageTop: jasmine.createSpy()
    };
    router = {
      events: {
        subscribe: jasmine.createSpy(),
        pipe: jasmine.createSpy().and.returnValue({
          subscribe: jasmine.createSpy()
        })
      },
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      navigate: jasmine.createSpy('navigate')
    };
    dialogService = {
      closeDialogs: jasmine.createSpy('closeDialogs'),
      modalListener: of(null)
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy(),
      getPreviousSegment: jasmine.createSpy(),
      loadRouting: jasmine.createSpy(),
      getCurrentUrl: jasmine.createSpy(),
      getRouteParam: jasmine.createSpy('getRouteParam')
    };
    dynamicComponentLoader = {
      getComponentFactory: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy()
      })
    };
    asyncScriptLoaderService = {
      loadSvgIcons: jasmine.createSpy().and.returnValue(of(null)),
      loadJsFile: jasmine.createSpy().and.returnValue(of(null))
    };
    navigationService = {
      isAbsoluteUri: jasmine.createSpy('isAbsoluteUri'),
      redirect: jasmine.createSpy('redirect')
    };

    awsService = {
      API: {},
      addAction: jasmine.createSpy()
    };

    sessionStorage = jasmine.createSpyObj('storageService', ['set', 'get', 'remove']);

    germanSupportService = {
      redirectToMainPage: jasmine.createSpy()
    };
    changeDetectorRef = {
      changeDetectorRef: jasmine.createSpy()
    }
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get')
    };

    command = {
      API: commandApi,
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve())
    };

    ezNavVanillaService = {
      isDeviceBrowserValidForCasino: jasmine.createSpy('isDeviceBrowserValidForCasino'),
      casinoMyBetsVanillaInit: jasmine.createSpy('casinoMyBetsVanillaInit')
    };

    fanzoneHelperService = {};

    initNetworkIndicatorService = { init: jasmine.createSpy('init') };

    component = new DesktopBmaMainComponent(
      device,
      user,
      windowRef,
      route,
      locale,
      nativeBridge,
      pubsub,
      cms,
      storageService,
      afterLoginNotifications,
      navigationService,
      authService,
      location,
      insomnia,
      gtm,
      filtersService,
      coreTools,
      domSanitizer,
      rendererService,
      domTools,
      router,
      dialogService,
      routingState,
      dynamicComponentLoader,
      asyncScriptLoaderService,
      awsService,
      sessionStorage,
      seoDataService,
      ezNavVanillaService,
      command,
      fanzoneStorageService,
      germanSupportService,
      fanzoneHelperService,
      changeDetectorRef,
      initNetworkIndicatorService
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });
});
