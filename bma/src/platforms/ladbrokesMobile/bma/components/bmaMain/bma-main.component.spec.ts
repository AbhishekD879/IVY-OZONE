import { of } from 'rxjs';
import { LadbrokesBmaMainComponent } from './bma-main.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { FANZONECONFIG } from '@ladbrokesMobile/bma/components/bmaMain/mockdata/bma-main.component.mock';

describe('LadbrokesBmaMainComponent', () => {
  let component: LadbrokesBmaMainComponent;
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
  let fanzoneStorageService;
  let initNetworkIndicatorService;
  const fanzoneConfig = FANZONECONFIG;
  
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
    seoDataService = {
      organisationPageSeo: jasmine.createSpy('organisationPageSeo')
    };
    nativeBridge = {
      logout: jasmine.createSpy('logout')
    };
    fanzoneStorageService = {
      set: jasmine.createSpy('fanzoneStorageService.set'),
      get: jasmine.createSpy('fanzoneStorageService.get')
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
        pipe: () => of(),
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
      getFanzone: jasmine.createSpy('getFanzone').and.returnValue(of(fanzoneConfig)),
      extractInitialIcons: jasmine.createSpy('extractInitialIcons').and.callFake(() => {
        return { subscribe: jasmine.createSpy() };
      }),
      getMenuItems: jasmine.createSpy().and.returnValue(of([])),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
      getQuizPopupSetting: jasmine.createSpy().and.returnValue(of({})),
      isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true))
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
      sportCatIcon: jasmine.createSpy('sportCatIcon').and.returnValue('sportCatIcon')
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
      }),
      loadModule: jasmine.createSpy('loadModule')
    };
    asyncScriptLoaderService = {
      getSvgSprite: jasmine.createSpy('getSvgSprite').and.returnValue(of('')),
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
      redirectToMainPage: jasmine.createSpy(),
      toggleItemsList: jasmine.createSpy(),
      isRestrictedSport: jasmine.createSpy('isRestrictedSport').and.returnValue(false)
    };

    command = {
      API: commandApi,
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve())
    };

    ezNavVanillaService = {
      isDeviceBrowserValidForCasino: jasmine.createSpy('isDeviceBrowserValidForCasino'),
      casinoMyBetsVanillaInit: jasmine.createSpy('casinoMyBetsVanillaInit')
    };

    fanzoneHelperService = {
      PublishFanzoneData: jasmine.createSpy(),
      getSelectedFzUpdate  : jasmine.createSpy().and.returnValue(of(FANZONECONFIG))
    }

    initNetworkIndicatorService = { init: jasmine.createSpy('init') };

    component = new LadbrokesBmaMainComponent(
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
      fanzoneStorageService,
      command,
      germanSupportService,
      fanzoneHelperService,
      initNetworkIndicatorService
    );
  });

  describe('ngOnInit', () => {
    it('should init hash change listener', () => {
      component['checkRemoteLink'] = jasmine.createSpy('component.checkRemoteLink');
      component['subscribeToRouterEvents'] = jasmine.createSpy('subscribeToRouterEvents');
      rendererService.renderer.listen.and.callFake( (a, b, cb) => {
        cb();
      });
      component.ngOnInit();
      expect(component['checkRemoteLink']).toHaveBeenCalled();
    });
    // it('Should subscribe to SEGMENTED_FE_REFRESH', () => {
    //   device.isMobile = true;
    //   component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
    //     .and.callFake((fileName: string, method: string | string[], callback: Function) => {
    //       if (method === pubsub.API.SEGMENTED_FE_REFRESH) {
    //         callback();
    //         expect(component['getMenuItems']).toHaveBeenCalled();
    //       }
    //     });
    //   component.ngOnInit();
    // });
    // it('Should subscribe to NONSEGMENTED_FE_REFRESH', () => {
    //   component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
    //     .and.callFake((fileName: string, method: string | string[], callback: Function) => {
    //       if (method === pubsub.API.NONSEGMENTED_FE_REFRESH) {
    //         callback();
    //         expect(component['getMenuItems']).toHaveBeenCalled();
    //       }
    //     });
    //   component.ngOnInit();
    // });
  });

  it('should call needed methods in constructor', () => {
    expect(component['platformPath']).toEqual('ladbrokesMobile');
  });


  describe('#sessionLoginHandler', () => {
    beforeEach(() => {
      component['scrollTop'] = jasmine.createSpy();
      component['handleRedirectAfterSignUp'] = jasmine.createSpy();
      windowRef.nativeWindow.location.pathname = 'any';
      user.firstLogin = true;
      user.status = true;
      user.isRedirecting = false;
    });
    describe('@checkRemoteLink', () => {
      it('should call add to betslip', () => {
        component['checkRemoteLink']('#!?tab=featured&externalSelectionId=97188563');
        expect(command.executeAsync).toHaveBeenCalledWith(jasmine.any(String), jasmine.any(Array));
      });
    });
  });

  it ('should filterRibbonItems and remove hidden/disabled items', () => {
    const ribbonItemsMock = [
      {
        imageTitle: 'active',
        disabled: false,
        hidden: false,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'not hidden',
        hidden: false,
        disabled: false,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'disabled',
        disabled: true,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'hidden not disabled',
        hidden: true,
        disabled: false,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'disabled not hidden',
        hidden: false,
        disabled: true,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'hidden disabled',
        hidden: true,
        disabled: true,
        showInHome: true,
        sportName: ''
      },
      {
        imageTitle: 'NotInHome',
        hidden: false,
        disabled: false,
        showInHome: false,
        sportName: ''
      }
    ] as any;

    const resultMock = [
      {
        imageTitle: 'active',
        disabled: false,
        hidden: false,
        showInHome: true,
        iconClass: 'sportCatIcon',
        sportName: ''
      },
      {
        imageTitle: 'not hidden',
        hidden: false,
        disabled: false,
        showInHome: true,
        iconClass: 'sportCatIcon',
        sportName: ''
      }
    ] as any;

    const result = component['filterRibbonItems'](ribbonItemsMock);

    expect(result).toEqual(resultMock);
    expect(result.length).toEqual(2);
  });

  it ('should filterRibbonItems and remove restricted sport item', () => {
    germanSupportService.isRestrictedSport.and.returnValue(true);

    const ribbonItemsMock = [
      {
        imageTitle: 'restricted',
        disabled: false,
        hidden: false,
        showInHome: true,
        sportName: ''
      }
    ] as any;

    const result = component['filterRibbonItems'](ribbonItemsMock);

    expect(result).toEqual([]);
  });

  it ('should filterRibbonItems based on fanzone config', () => {
    component['fanzone'] = {
      active: true,
      fanzoneConfiguration: {
        sportsRibbon: true
      }
    } as any;
    const ribbonItemsMock = [
      {
        imageTitle: 'fanzone',
        disabled: false,
        hidden: false,
        showInHome: true,
        sportName: 'fanzone',
        fzDisabled:false
      }
    ] as any;
    user.status = true;
    fanzoneStorageService.get= jasmine.createSpy('get').and.returnValue({teamName:'everton',teamId:'fz00'});
    const result = component['filterRibbonItems'](ribbonItemsMock);

    expect(result[0].disabled).toEqual(false);
    expect(result[0].fzDisabled).toEqual(false);
  });
});
