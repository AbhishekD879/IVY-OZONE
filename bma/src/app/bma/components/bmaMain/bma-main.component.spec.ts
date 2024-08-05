import { of, Subscription, throwError } from 'rxjs';
import { NavigationEnd, NavigationStart } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';
import { BmaMainComponent } from './bma-main.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import * as env from '@environment/oxygenEnvConfig';
import { SPRITE_PATH } from '@bma/constants/image-manager.constant';
import { PERFORMANCE_API_MEASURE,PERFORMANCE_API_MARK } from '@app/lazy-modules/performanceMark/enums/performance-mark.enums';
import { NETWORK_CONSTANTS } from '@app/lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
describe('BmaMainComponent', () => {
  const COOKIE_LENGTH = 'cookiesLength';
  const environment = env as any;

  let component: BmaMainComponent;
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
  let sessionStorage, seoDataService;
  let ezNavVanillaService;
  let fanzoneHelperService;
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
      username: 'username',
      set: jasmine.createSpy(),
      getJourneyParams: jasmine.createSpy('getJourneyParams').and.returnValue({}),
      canActivateJourney: jasmine.createSpy('canActivateJourney').and.returnValue(false),
      isRouletteJourney: jasmine.createSpy('isRouletteJourney').and.returnValue(false),
      breakRouletteJourney: jasmine.createSpy('breakRouletteJourney'),
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
          href: 'https://sports.coral.co.uk/',
          pathname: ''
        },
        document: {
          referrer: '',
          cookie: 'cookie'
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
    locale = {
      getLocale: jasmine.createSpy('getLocale')
    };
    nativeBridge = {
      logout: jasmine.createSpy('logout'),
      getBuildVersion: jasmine.createSpy('getBuildVersion')
    };
    pubsubReg = {};
    pubsub = {
      publish: jasmine.createSpy().and.callFake( (channel) => pubsubReg[channel] && pubsubReg[channel]() ),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((domain, channel, fn) => { pubsubReg[channel] = fn; }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    cms = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        
        Generals: {
          betSlipAnimation: false
        }}
    )),
      getStaticBlock: jasmine.createSpy().and.returnValue(of({})),
      extractInitialIcons: jasmine.createSpy().and.returnValue(of([])),
      getMenuItems: jasmine.createSpy().and.returnValue(of([{ showInHome: true,targetUri:'racingsuperseries'}])),
      triggerSystemConfigUpdate: jasmine.createSpy('triggerSystemConfigUpdate'),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    seoDataService = {
      organisationPageSeo: jasmine.createSpy('organisationPageSeo')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy(),
      remove: jasmine.createSpy('remove'),
      setCookie: jasmine.createSpy(),
      getCookie: jasmine.createSpy('getCookie').and.returnValue('redirectUrl'),
      removeCookie: jasmine.createSpy()
    };
    afterLoginNotifications = {
      start: jasmine.createSpy()
    };
    authService = {
      mainInit: jasmine.createSpy(),
      getTempToken: jasmine.createSpy().and.returnValue(of({}))
    };
    location = {
      path: jasmine.createSpy().and.returnValue('')
    };
    insomnia = {
      init: jasmine.createSpy(),
      initNetworkIndicator: jasmine.createSpy()
    };
    gtm = {
      push: jasmine.createSpy(),
      pushCachedEvents: jasmine.createSpy(),
      pushLogoutInfo: jasmine.createSpy('pushLogoutInfo')
    };
    filtersService = {
      sportCatIcon: jasmine.createSpy('sportCatIcon').and.returnValue('iconClass'),
      filterLinkforRSS: jasmine.createSpy('filterLinkforRSS').and.returnValue((of('promotion/details/exclusion'))),
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy().and.returnValue(false)
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy(),
        removeClass: jasmine.createSpy(),
        addClass: jasmine.createSpy()
      }
    };
    domTools = {
      css: jasmine.createSpy(),
      scrollPageTop: jasmine.createSpy()
    };
    router = {
      events: of(new NavigationEnd(1, '/', '/')),
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(Promise.resolve(jasmine.any(String))),
      navigate: jasmine.createSpy('navigate')
    };
    dialogService = {
      closeDialogs: jasmine.createSpy('closeDialogs'),
      modalListener: of(null)
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy(),
      getSegmentHistory: jasmine.createSpy(),
      getPreviousSegment: jasmine.createSpy(),
      loadRouting: jasmine.createSpy(),
      getCurrentUrl: jasmine.createSpy(),
      getRouteParam: jasmine.createSpy('getRouteParam'),
      replayRouterEvents: {
        subscribe: jasmine.createSpy('subscribe')
      },
      togglePortalSwitch: jasmine.createSpy('togglePortalSwitch')
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
      redirectCurrPage: jasmine.createSpy('redirectCurrPage')
    };

    awsService = {
      API: {},
      addAction: jasmine.createSpy('addAction')
    };

    sessionStorage = jasmine.createSpyObj('storageService', ['set', 'get', 'remove']);

    ezNavVanillaService = {
      isDeviceBrowserValidForCasino: jasmine.createSpy('isDeviceBrowserValidForCasino').and.returnValue(true),
      casinoMyBetsVanillaInit: jasmine.createSpy('casinoMyBetsVanillaInit')
    };

    fanzoneHelperService = {
      appBuildVersion: jasmine.createSpy('appBuildVersion')
    };

    initNetworkIndicatorService = { init: jasmine.createSpy('init') };

    spyOn(console, 'warn');

    component = new BmaMainComponent(
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
      fanzoneHelperService,
      initNetworkIndicatorService
    );
  });

  describe('#constructor', () => {
    it('isDeviceBrowserValidForCasino() will return true', () => {
      component['ezNavVanillaService'].isMyBetsInCasino = true;
      expect(component).toBeTruthy();
    })
  });

  describe('ngOnInit', () => {
    it('general calls', done => {
      windowRef.nativeWindow.setTimeout.and.callFake(cb => {
        cb(); // call setTimeout callback
      });
      component.ngOnInit();
      expect(dynamicComponentLoader.getComponentFactory).not.toHaveBeenCalled();
      // expect(pubsub.subscribe).toHaveBeenCalledTimes(17);
      expect(dynamicComponentLoader.getComponentFactory).not.toHaveBeenCalled();
      expect(sessionStorage.set).toHaveBeenCalled();
      done();
    });
    it('should init resizeListerner', () => {
      component['breakPoint'] = jasmine.createSpy('component.breakPoint');
      rendererService.renderer.listen.and.callFake( (a, b, cb) => {
        cb();
      });
      component.ngOnInit();
      expect(component['breakPoint']).toHaveBeenCalled();
    });
    it('Should subscribe to SEGMENTED_INIT_FE_REFRESH', () => {
      device.isMobile = true;
      component['getMenuItems'] = jasmine.createSpy('getMenuItems');
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (Array.isArray(method) && method[1] === pubsub.API.SEGMENTED_INIT_FE_REFRESH) {
            callback();
            expect(component['getMenuItems']).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });

    it('should get storage info for extra places QUICKBET_EXTRAPLACE_SELECTION', () => {
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.QUICKBET_EXTRAPLACE_SELECTION) {
            callback();
            expect(sessionStorage.set).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });

    it('Should subscribe to APP_BUILD_VERSION and update MenuItems', () => {
      component['getMenuItems'] = jasmine.createSpy('getMenuItems');
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.APP_BUILD_VERSION) {
            callback("v10");
            expect(component['getMenuItems']).toHaveBeenCalled();
            expect(fanzoneHelperService.appBuildVersion).toBe("v10");
          }
        });
      component.ngOnInit();
    });
    it('Should subscribe to STREAM_BET_VIDEO_MODE', () => {
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.STREAM_BET_VIDEO_MODE) {
            callback();
          }
        });
      component.ngOnInit();
    });
    it('Should subscribe to FZ_MENUS_UPDATE and update MenuItems', () => {
      component['getMenuItems'] = jasmine.createSpy('getMenuItems');
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.FZ_MENUS_UPDATE) {
            callback();
            expect(component['getMenuItems']).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });

    it('should subscribe to Gaming Overlay', fakeAsync(() => {
      pubsub.subscribe.and.callFake((a, b, cb) => {
        if (b === 'GAMING_OVERLAY_OPEN') {
          cb();
        }
      });
      component.ngOnInit();
      tick();
      expect(component.isGamingOpen).toBe(true);
    }));
    it('should subscribe to Gaming Overlay', fakeAsync(() => {
      pubsub.subscribe.and.callFake((a, b, cb) => {
        if (b === 'GAMING_OVERLAY_CLOSE') {
          cb();
        }
      });
      component.ngOnInit();
      tick();
      expect(component.isGamingOpen).toBe(false);
    }));

    describe('setConfigs method', () => {
      it('should set correct state', (() => {
        const testData = {
          Banners: {
            transitionDelay: 'true',
            newName: true
          },
          Layouts: {
            ShowLeftMenu: 'true',
            ShowTopMenu: 'true',
            ShowRightMenu: 'true'
          },
          LCCP: {
            gameFrequency: '1',
            gameFrequencyValues: '2',
            hourlyAlerts: '3'
          }
        };
        const result = component['setConfigs'](testData);

        expect(result).toBe(testData);
        expect(component.sysConfig).toBe(testData);
        expect(component.transition).toBe('true');
      }));
    });
    afterEach(() => {
      performance.clearMarks();
      performance.clearMeasures();
    });
  });

  describe('ngAfterViewInit', () => {

    it('should not call renderBetslip', () => {
      component['renderBetslip'] = jasmine.createSpy();
      pubsub.subscribe = jasmine.createSpy().and.callFake((name, channel, callback) => callback());
      component.ngAfterViewInit();
      expect(pubsub.subscribe).not.toHaveBeenCalled();
      expect(component['renderBetslip']).not.toHaveBeenCalled();
    });

    it('should publish APP_IS_LOADED pubsub event', () => {
      component.ngAfterViewInit();
      expect(pubsub.publish).toHaveBeenCalledWith('APP_IS_LOADED');
    });

    it('should set "bma-ready" class name to <html>', () => {
      component.ngAfterViewInit();
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(windowRef.document.documentElement, 'bma-ready');
    });
  });

  describe('ngOnDestroy', () => {
    beforeEach(() => {
      component['routeChangeSuccessHandler'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
    });

    it('should unsubscribe listeners', () => {
      (component as any).resizeListerner = jasmine.createSpy('resizeListerner');
      (component as any).windowResizeListener = jasmine.createSpy('windowResizeListener');
      component['slideOutBetslipRef'] = { destroy: jasmine.createSpy('destroy') } as any;

      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('BmaMainComponent');
      expect(component['resizeListerner']).toHaveBeenCalled();
      expect(component['windowResizeListener']).toHaveBeenCalled();
      expect(component['slideOutBetslipRef'].destroy).toHaveBeenCalled();
    });

    it('shoud not throw error if resize listener is not defined', () => {
      component['resizeListerner'] = null;
      expect(() => component.ngOnDestroy()).not.toThrowError();
    });

    it('should unsubscribe from cmsConfigsSubscription', () => {
      component['cmsConfigsSubscription'] = new Subscription();
      component['cmsConfigsSubscription'].unsubscribe = jasmine.createSpy();

      component.ngOnDestroy();
      expect(component['cmsConfigsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('@addContentViewEvent', () => {
    it('should track gtm view', () => {
      const mockLocation = 'myPage';

      location.path.and.returnValue(mockLocation);
      component['addContentViewEvent']();

      expect(gtm.push).toHaveBeenCalledWith('content-view', {
        screen_name: mockLocation
      });
    });
  });

  describe('@showSportMenu', () => {
    it('should set "isHomeURL" as true when location is empty (home) url', () => {
      component.isHomeURL = false;
      location.path.and.returnValue('');
      component['showSportMenu']();

      expect(component.isHomeURL).toEqual(true);
    });

    it('should set "isHomeURL" as true when location contains home url', () => {
      component.isHomeURL = false;
      location.path.and.returnValue('/home/featured');
      component['showSportMenu']();

      expect(component.isHomeURL).toEqual(true);
    });

    it('should set "isHomeURL" as false when location is not match home url', () => {
      component.isHomeURL = true;
      location.path.and.returnValue('/some/page');
      component['showSportMenu']();

      expect(component.isHomeURL).toEqual(false);
    });
  });

  describe('@showWidgetColumns', () => {
    it('should set "showRC" as false if device is mobile', () => {
      component.showRC = true;
      device.isMobile = true;
      device.isDesktop = false;
      component['showWidgetColumns']();

      expect(component.showRC).toEqual(false);
    });

    it('should set "showRC" as true if current segment is as tabs page', () => {
      component.showRC = false;
      device.isMobile = false;
      device.isDesktop = true;
      routingState.getCurrentSegment.and.returnValue('tabs');
      component['showWidgetColumns']();

      expect(component.showRC).toEqual(true);
    });

    it('should set "showRC" as false if current segment is as signUp page', () => {
      component.showRC = true;
      device.isMobile = false;
      routingState.getCurrentSegment.and.returnValue('signUp');
      component['showWidgetColumns']();

      expect(component.showRC).toEqual(false);
    });

    it('should set "showRC" as true if current segment is as not configured page and device is not mobile', () => {
      component.showRC = false;
      device.isMobile = false;
      routingState.getCurrentSegment.and.returnValue('someSegment');
      component['showWidgetColumns']();

      expect(component.showRC).toEqual(true);
    });

    it('should emit pubsub event', () => {
      component['showWidgetColumns']();

      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.SHOW_HIDE_WIDGETS);
    });
  });

  describe('@scrollTop', () => {
    it('should not scroll page to the top if footbal tutorial active', () => {
      component['isFootbalTutorialActive'] = () => true;

      component['scrollTop']();
      expect(domTools.scrollPageTop).not.toHaveBeenCalled();
    });

    it('should  scroll page to the top if footbal tutorial is not active', () => {
      component['isFootbalTutorialActive'] = () => false;

      component['scrollTop']();
      expect(domTools.scrollPageTop).toHaveBeenCalled();
    });
  });

  describe('@handleRouteChange On Navigation Start', () => {
    let eventStart;
    beforeEach(() => {
      eventStart = new NavigationStart(1, '/inplay');
    });
    it('handleRouteChange with NavigationStart and w/o BMA:CTI', () => {
      routingState.getCurrentSegment.and.returnValue('tabs');
      performance.clearMarks();
      component['handleRouteChange'](eventStart);
      expect(performance.getEntriesByName(PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.Mark).length > 0);
    });
    it('handleRouteChange with NavigationStart and with BMA:CTI and BMA:NAV', () => {
      routingState.getCurrentSegment.and.returnValue('tabs');
      performance.mark(PERFORMANCE_API_MARK.CTI);
      performance.mark(PERFORMANCE_API_MARK.TTI);
      performance.measure(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.TTI);
      component['handleRouteChange'](eventStart);
      expect(performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure).length === 0);
    });
    it('handleRouteChange with NavigationStart and For Loading Inplay Fisrt Sport', () => {
      routingState.getCurrentSegment.and.returnValue('inPlay.firstSport');
      performance.clearMarks();
      component['handleRouteChange'](eventStart);
      expect(performance.getEntriesByName(PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.Mark).length === 0);
    });
  });

  describe('@handleRouteChange', () => {
    let eventEnd;

    beforeEach(() => {
      eventEnd = new NavigationEnd(0, '', '');
      user.isRouletteJourney.and.returnValue(false);
    });
    it('should not remove "gameBaseUrl" cookie if previous segment not available', () => {
      routingState.getCurrentSegment.and.returnValue('page');
      component['handleRouteChange'](eventEnd);

      expect(storageService.removeCookie).not.toHaveBeenCalled();
    });

    it('should not remove "gameBaseUrl" cookie if current segment not available', () => {
      routingState.getPreviousSegment.and.returnValue('page');
      component['handleRouteChange'](eventEnd);

      expect(storageService.removeCookie).not.toHaveBeenCalled();
    });

    it('should not remove "gameBaseUrl" cookie if current and previous segments are equal', () => {
      const segmentName: string = 'page';

      routingState.getPreviousSegment.and.returnValue(segmentName);
      routingState.getCurrentSegment.and.returnValue(segmentName);
      component['handleRouteChange'](eventEnd);

      expect(storageService.removeCookie).not.toHaveBeenCalled();
    });

    it('should not remove "gameBaseUrl" cookie if current segments belongs to deposit group', () => {
      routingState.getPreviousSegment.and.returnValue('page');
      routingState.getCurrentSegment.and.returnValue('/deposit/page');
      component['handleRouteChange'](eventEnd);

      expect(storageService.removeCookie).not.toHaveBeenCalled();
    });

    it('should remove "gameBaseUrl" cookie if current and previous segments are different and current ' +
      'segment is not from deposit group', () => {
      routingState.getPreviousSegment.and.returnValue('deposit/page');
      routingState.getCurrentSegment.and.returnValue('newpage');
      component['handleRouteChange'](eventEnd);

      expect(storageService.removeCookie).toHaveBeenCalledWith('gameBaseUrl');
    });

    it('should not close dialogs when navigated from neteller page', () => {
      routingState.getPreviousSegment.and.returnValue('deposit.neteller');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).not.toHaveBeenCalled();
    });

    it('should not close dialogs when navigated from addToBetSlip page', () => {
      routingState.getPreviousSegment.and.returnValue('addToBetSlip');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).not.toHaveBeenCalled();
    });

    it('should not close dialogs when user is on deposit page', () => {
      routingState.getCurrentSegment.and.returnValue('deposit.registered');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).not.toHaveBeenCalled();
    });

    it('should not close dialogs when navigated from deposit registered page', () => {
      routingState.getPreviousSegment.and.returnValue('deposit.registered');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).not.toHaveBeenCalled();
    });

    it('should not close dialogs when navigated to home page', () => {
      location.path.and.returnValue('/home/private-markets');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).not.toHaveBeenCalled();
    });

    it('should close dialogs when navigated from not skipped page', () => {
      location.path.and.returnValue('/some/page');
      routingState.getCurrentSegment.and.returnValue(('newpage'));
      routingState.getPreviousSegment.and.returnValue('somepage');
      component['handleRouteChange'](eventEnd);

      expect(dialogService.closeDialogs).toHaveBeenCalled();
      expect(sessionStorage.set).toHaveBeenCalled();
    });

    describe('for RouletteJourney', () => {
      it('should not check roulette journey if not homepage ', () => {
        eventEnd = new NavigationEnd(0, '', '');
        routingState.getCurrentSegment.and.returnValue('deposit.registered');
        routingState.getPreviousSegment.and.returnValue('deposit.registered');
        spyOn<any>(component, 'checkIfHomeUrl').and.returnValue(true);
        component['handleRouteChange'](eventEnd);

        expect(user.getJourneyParams).not.toHaveBeenCalled();
        expect(user.isRouletteJourney).not.toHaveBeenCalled();
      });

      it('should check roulette journey ', () => {
        eventEnd = new NavigationEnd(0, '', '');
        routingState.getCurrentSegment.and.returnValue('some-page');
        routingState.getPreviousSegment.and.returnValue('some-new-page');
        spyOn<any>(component, 'checkIfHomeUrl').and.returnValue(false);
        component['handleRouteChange'](eventEnd);

        expect(user.getJourneyParams).toHaveBeenCalledWith(jasmine.any(String));
        expect(user.isRouletteJourney).toHaveBeenCalled();
      });

      describe('', () => {
        beforeEach(() => {
          eventEnd = new NavigationEnd(0, '', '');
          routingState.getCurrentSegment.and.returnValue('some-page');
          routingState.getPreviousSegment.and.returnValue('some-new-page');
          spyOn<any>(component, 'checkIfHomeUrl').and.returnValue(false);
        });

        it('should call closeDialogs if not RouletteJourney', () => {
          user.isRouletteJourney.and.returnValue(false);
          component['handleRouteChange'](eventEnd);

          expect(dialogService.closeDialogs).toHaveBeenCalled();
        });

        it('should call closeDialogs if RouletteJourney and not entry point', () => {
          user.isRouletteJourney.and.returnValue(true);
          user.getJourneyParams.and.returnValue({});
          component['handleRouteChange'](eventEnd);

          expect(dialogService.closeDialogs).toHaveBeenCalled();
        });

        it('should not call closeDialogs if RouletteJourney and entry point', () => {
          user.isRouletteJourney.and.returnValue(true);
          user.getJourneyParams.and.returnValue({
            targetPage: 'targetPage',
            referrerPage: 'referrerPage'
          });
          component['handleRouteChange'](eventEnd);

          expect(dialogService.closeDialogs).not.toHaveBeenCalled();
        });
      });
    });
  });

  describe('@subscribeToGlobalEvents', () => {
    beforeEach(() => {
      component['getGtmIds'] = jasmine.createSpy('getGtmIds').and.returnValue(['gtmId1', 'gtmId2']);
    });

    it('should call through callbacks of pubsub subscribes', () => {
      pubsub.subscribe = (arg1: string, arg2: string | string[], Function) => Function();

      component['subscribeToGlobalEvents']();

      expect(cms.triggerSystemConfigUpdate).toHaveBeenCalled();
      expect(gtm.pushLogoutInfo).toHaveBeenCalled();
      expect(nativeBridge.logout).toHaveBeenCalled();
      expect(user.set).toHaveBeenCalledWith({ showBalance: undefined });
      expect(component.loginPending).toBeUndefined();
      expect(routingState.getRouteParam).toHaveBeenCalled();
      expect(storageService.getCookie).toHaveBeenCalled();
    });

    it('cbURL exist', () =>  {
      user.isRedirecting = true;
      user.status = true;
      component['doRedirect'] = jasmine.createSpy();
      routingState.getRouteParam.and.returnValue('cbURL');
      storageService.get.and.returnValue('{{username}}{{tempToken}}');
      pubsub.subscribe.and.callFake( (a, b, cb) => {
        cb();
      });
      component['subscribeToGlobalEvents']();
      expect(storageService.set).toHaveBeenCalled();
      expect(component['doRedirect']).toHaveBeenCalled();
      authService.getTempToken.and.returnValue(throwError(null));
      component['subscribeToGlobalEvents']();
      expect(component['doRedirect']).toHaveBeenCalled();
      storageService.get.and.returnValue('{{username}}');
      component['subscribeToGlobalEvents']();
    });

    describe('when DEFERRED_MODULES_LOADED PubSub event occurs', () => {

      beforeEach(() => {
        spyOn(component as any, 'loadAdditionalIcons');

        component['subscribeToGlobalEvents']();
        component.sysConfig = { gtm: { enabled: true } } as any;
        expect(pubsub.subscribe.calls.allArgs()).toContain(['BmaMainComponent', 'DEFERRED_MODULES_LOADED', jasmine.any(Function)]);
      });

      it('should wait 1000ms before proceeding', () => {
        pubsubReg['DEFERRED_MODULES_LOADED']();
        expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
        expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledBefore(component['getGtmIds'] as any);
      });

      it('should get GTM IDs for current environment', () => {
        pubsubReg['DEFERRED_MODULES_LOADED']();
        expect(component['getGtmIds']).toHaveBeenCalled();
      });

      it('should not get GTM IDs for current environment if no sysConfig for it', () => {
        component.sysConfig = {} as any;
        pubsubReg['DEFERRED_MODULES_LOADED']();
        expect(component['getGtmIds']).not.toHaveBeenCalled();
      });

      it('should load additional sprite', () => {
        pubsubReg['DEFERRED_MODULES_LOADED']();

        expect(component['loadAdditionalIcons']).toHaveBeenCalled();
      });

      it('should map GTM IDs to JS file loader Observables', () => {
        pubsubReg['DEFERRED_MODULES_LOADED']();
        const allArgs = asyncScriptLoaderService.loadJsFile.calls.allArgs();
        expect(allArgs).toContain(['https://www.googletagmanager.com/gtm.js?id=gtmId1']);
        expect(allArgs).toContain(['https://www.googletagmanager.com/gtm.js?id=gtmId2']);
      });

      describe('should load gtm-script.js', () => {
        beforeEach(() => {
          asyncScriptLoaderService.loadJsFile.and.callFake(fileName => of(fileName));
        });

        it('once all GTM scripts are loaded', () => {
          pubsubReg['DEFERRED_MODULES_LOADED']();
        });

        it('if at least one GTM script is loaded successfully', () => {
          asyncScriptLoaderService.loadJsFile.and.callFake(fileName =>
            fileName.indexOf('gtmId1') >= 0 ? throwError('error') : of(fileName));
          pubsubReg['DEFERRED_MODULES_LOADED']();
        });

        afterEach(() => {
          expect(asyncScriptLoaderService.loadJsFile.calls.allArgs()).toContain(['../../../../assets/gtm/gtm-script.js']);
          expect(awsService.addAction).toHaveBeenCalledWith(COOKIE_LENGTH, 6);
        });
      });

      describe('should not load gtm-script.js', () => {
        beforeEach(() => {
          asyncScriptLoaderService.loadJsFile.and.callFake(fileName =>
            fileName.indexOf('gtmId1') >= 0 || fileName.indexOf('gtmId2') >= 0 ? throwError('error') : of(fileName));
        });

        it('if all GTM script fail to load successfully', () => {
          pubsubReg['DEFERRED_MODULES_LOADED']();
        });

        it('and log error warning', () => {
          pubsubReg['DEFERRED_MODULES_LOADED']();
          expect(console.warn).toHaveBeenCalledWith('No GTM scripts were loaded.');
        });

        afterEach(() => {
          expect(asyncScriptLoaderService.loadJsFile.calls.allArgs()).not.toContain(['../../../../assets/gtm/gtm-script.js']);
        });
      });

      it('asyncScriptLoaderService observables should emit only once', () => {
        asyncScriptLoaderService.loadJsFile.and.callFake(fileName => of(fileName, fileName, fileName));
        pubsubReg['DEFERRED_MODULES_LOADED']();

        expect(asyncScriptLoaderService.loadJsFile.calls.allArgs()).toEqual([
          ['https://www.googletagmanager.com/gtm.js?id=gtmId1'],
          ['https://www.googletagmanager.com/gtm.js?id=gtmId2'],
          ['../../../../assets/gtm/gtm-script.js'],
          ['/assets/insomnia.js'],
          ['/assets/network-indicator.js']
        ]);
        expect(gtm.pushCachedEvents).toHaveBeenCalledTimes(1);
      });
    });
  });

  describe('loadFeaturedIcons', () => {
    it('stored content is featured', () => {
      storageService.get.and.returnValue({ "name": "featured", "content": "test"});
      component['loadFeaturedIcons']();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.featuredIcons).toBe("test");
    });
    it('stored content is not featured', () => {
      storageService.get.and.returnValue({ "name": "home", "content": "test"});
      component['loadFeaturedIcons']();
      expect(asyncScriptLoaderService.getSvgSprite).toHaveBeenCalledWith(SPRITE_PATH.featured);
    });

    it('should get icons', () => {
      component['loadFeaturedIcons']();

      expect(asyncScriptLoaderService.getSvgSprite).toHaveBeenCalledWith(SPRITE_PATH.featured);
    });
  });

  describe('loadAdditionalIcons', () => {

    it('should get icons', () => {
      component['loadAdditionalIcons']();

      expect(asyncScriptLoaderService.getSvgSprite).toHaveBeenCalledWith(SPRITE_PATH.additional);
    });

    describe('when REDIRECT event occurs', () => {
      it('should not change redirect url if url is absolute', () => {
        navigationService.isAbsoluteUri.and.returnValue(true);
        component['subscribeToGlobalEvents']();
        pubsubReg['REDIRECT']();
        expect(navigationService.redirectCurrPage).toHaveBeenCalledWith('redirectUrl');
      });

      it('shoud call callback if no redirect url in storage', () => {
        const callbackSpy = jasmine.createSpy('callbackSpy');
        storageService.getCookie.and.returnValue('');
        component['subscribeToGlobalEvents']();
        pubsubReg['REDIRECT'](callbackSpy);
        expect(callbackSpy).toHaveBeenCalledTimes(1);
      });

      it('shoud not throw error if callback is not function', () => {
        storageService.getCookie.and.returnValue('');
        expect(() => {
          component['subscribeToGlobalEvents']();
          pubsubReg['REDIRECT'](null);
        }).not.toThrowError();
      });
    });
  });

  describe('getGtmIds', () => {
    let originalGoogleTagManagerID;

    it('should return value of environment.googleTagManagerID', () => {
      originalGoogleTagManagerID = environment.googleTagManagerID;
      environment.googleTagManagerID = ['gtmId1', 'gtmId2'];
      expect(component['getGtmIds']()).toEqual(['gtmId1', 'gtmId2']);
    });

    xit('should return value of environment.googleTagManagerID', () => {
      originalGoogleTagManagerID = environment.googleTagManagerID;
      environment.googleTagManagerID = ['gtmId1'];
      expect(component['getGtmIds']()).toEqual(['gtmId1']);
    });

    xit('should return empty array', () => {
      originalGoogleTagManagerID = environment.googleTagManagerID;
      environment.googleTagManagerID = null;
      expect(component['getGtmIds']()).toEqual([]);
    });

    afterAll(() => {
      environment.googleTagManagerID = originalGoogleTagManagerID;
    });
  });

  describe( 'getDeviceType', () => {
    let devices;
    beforeEach( () => {
      devices = [];
    });
    it('should  return no device', () => {
      expect(component['getDeviceType'](undefined)).toBe('');
    });
    it('should  return tablet', () => {
      devices['landscapeTablet'] = 'test';
      expect(component['getDeviceType'](devices)).toBe('tablet');
    });
    it('should  return test', () => {
      devices['test'] = 'test';
      expect(component['getDeviceType'](devices)).toBe('test');
    });
  });

  describe('checkIfHomeUrl', () => {
    it('should checkIfHomeUrl /', () => {
      location.path.and.returnValue('');
      expect(component['checkIfHomeUrl']()).toEqual(true);
    });

    it('should checkIfHomeUrl /home', () => {
      location.path.and.returnValue('/home/');
      expect(component['checkIfHomeUrl']()).toEqual(true);
    });

    it('should checkIfHomeUrl /?utm_source=PWA', () => {
      location.path.and.returnValue('utm_source=PWA');
      expect(component['checkIfHomeUrl']()).toEqual(true);
    });

    it('should checkIfHomeUrl /sports/test', () => {
      location.path.and.returnValue('sports/test');
      expect(component['checkIfHomeUrl']()).toEqual(false);
    });

    it('should checkIfHomeUrl starts with query /?', () => {
      location.path.and.returnValue('?native=1&installedAppVersion=7.0');
      expect(component['checkIfHomeUrl']()).toEqual(true);
    });

    it('should checkIfHomeUrl contains query /?', () => {
      location.path.and.returnValue('sports/test?native=1');
      expect(component['checkIfHomeUrl']()).toEqual(false);
    });
  });

  it('#setLogoutState should logout', () => {
    component['setLogoutState']();

    expect(gtm.pushLogoutInfo).toHaveBeenCalled();
    expect(nativeBridge.logout).toHaveBeenCalled();
  });

  it('#subscribeToRouterEvents should subscribe to router events via ReplaceSubject wrapper', () => {
    component['subscribeToRouterEvents']();
    expect(routingState.replayRouterEvents.subscribe).toHaveBeenCalled();
  });

  describe('ngOnInit', () => {
    it('should not toggle portal switch', () => {
      device.isWrapper = false;
      component.ngOnInit();
      expect(routingState.togglePortalSwitch).not.toHaveBeenCalled();
    });

    it('should toggle portal switch', () => {
      device.isWrapper = true;
      component.ngOnInit();
      expect(routingState.togglePortalSwitch).toHaveBeenCalled();
    });
  });

  describe('ngOnInit (fix for iOS)', () => {
    const body = { tagName: 'BODY', offsetTop: 1 };

    beforeEach(() => {
      device.isIos = true;
      device.isWrapper = true;
      windowRef.nativeWindow.pageYOffset = 1;
      windowRef.document.querySelector.and.returnValue(body);
    });

    describe('open event', () => {
      it('shoud set body top position to -1px', () => {
        dialogService.modalListener = of({ type: 'open', name: 'Login' });
        location.path.and.returnValue('/');
        component.ngOnInit();
        expect(domTools.css).toHaveBeenCalledWith(body, { top: '-1px' });
        expect(rendererService.renderer.addClass).toHaveBeenCalledWith(body, 'ios-modal-wrapper');
        expect(rendererService.renderer.addClass).toHaveBeenCalledWith(body, 'ios-modal-opened');
      });

      it('shoud set body top position to 0px', () => {
        device.isWrapper = false;
        windowRef.nativeWindow.pageYOffset = 0;
        dialogService.modalListener = of({ type: 'open', name: 'Login' });
        location.path.and.returnValue('/');
        component.ngOnInit();
        expect(domTools.css).toHaveBeenCalledWith(body, { top: '0px' });
        expect(rendererService.renderer.addClass).toHaveBeenCalledWith(body, 'ios-modal-opened');
      });

      it('shoud not set body top position (not login event)', () => {
        dialogService.modalListener = of({ type: 'open', name: '' });
        location.path.and.returnValue('/');
        component.ngOnInit();
        expect(domTools.css).not.toHaveBeenCalled();
      });

      it('shoud not set body top position (signup)', () => {
        dialogService.modalListener = of({ type: 'open', name: '' });
        location.path.and.returnValue('/signup');
        component.ngOnInit();
        expect(domTools.css).not.toHaveBeenCalled();
      });
    });

    describe('close event', () => {
      it('shoud scroll and set top position to 0px', () => {
        dialogService.modalListener = of({ type: 'close' });
        location.path.and.returnValue('/');
        component['isFootbalTutorialActive'] = () => false;
        component.ngOnInit();
        expect(windowRef.nativeWindow.scrollBy).toHaveBeenCalledWith(0, '-1');
        expect(domTools.css).toHaveBeenCalledWith(body, { top: '0px' });
      });

      it('shoud not scroll but set top position to 0px', () => {
        dialogService.modalListener = of({ type: 'close' });
        location.path.and.returnValue('/');
        component['isFootbalTutorialActive'] = () => true;
        component.ngOnInit();
        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
        expect(domTools.css).toHaveBeenCalledWith(body, { top: '0px' });
      });

      it('shoud not scroll and not set top position (signup)', () => {
        dialogService.modalListener = of({ type: 'closeAll' });
        location.path.and.returnValue('/signup');
        component.ngOnInit();
        expect(windowRef.nativeWindow.scrollBy).not.toHaveBeenCalled();
        expect(domTools.css).not.toHaveBeenCalled();
      });
    });

    it('unhandled event', () => {
      dialogService.modalListener = of({ type: '' });
      component['showSportMenu'] = () => {};
      component.ngOnInit();
      location.path = jasmine.createSpy();
      expect(location.path).not.toHaveBeenCalled();
    });
  });

  it('getMenuItems', () => {
    cms.getSystemConfig = () => of({ Generals: {} });
    spyOn(component as any, 'showSportMenu');
    spyOn(component as any, 'showWidgetColumns');

    component['getMenuItems']();

    expect(component['showSportMenu']).toHaveBeenCalledTimes(1);
    expect(component['showWidgetColumns']).toHaveBeenCalledTimes(1);
  });

  it('getMenuItems should call filterLinkforRSS', () => {
    (filtersService['filterLinkforRSS']as any).and.returnValue(of('promotion/details/exclusion'));
    component['getMenuItems']();
    expect(filtersService.filterLinkforRSS).toHaveBeenCalled();
  });
  describe('breakPoint', () => {
    let wnd;
    beforeEach(() => {
      device.mobileWidth = 300;
      device.mobileWidth = 300;
      device.landTabletWidth = 800;
      device.desktopWidth = 1300;
      wnd = windowRef.nativeWindow;
    });

    it('should set mobile view', () => {
      wnd.innerWidth = 250;
      component['breakPoint']();
      expect(wnd.view).toEqual({ mobile: true, tablet: false, landscapeTablet: false, desktop: false });
    });

    it('should set table view', () => {
      wnd.innerWidth = 600;
      component['breakPoint']();
      expect(wnd.view).toEqual({ mobile: false, tablet: true, landscapeTablet: false, desktop: false });
    });

    it('should set landscape table view', () => {
      wnd.innerWidth = 900;
      component['breakPoint']();
      expect(wnd.view).toEqual({ mobile: false, tablet: false, landscapeTablet: true, desktop: false });
    });

    it('should set desktop view', () => {
      wnd.innerWidth = 1400;
      component['breakPoint']();
      expect(wnd.view).toEqual({ mobile: false, tablet: false, landscapeTablet: false, desktop: true });
    });
  });

  describe('#checkForFiveASideUrl',() => {
    it('should check for valid five aside url',() => {
      const mockLocation = '5-a-side/pre-leader-board/';
      location.path.and.returnValue(mockLocation);
      expect(component.checkForFiveASideUrl()).toBeTruthy();
    });
    it('should check for invalid  five aside url',() => {
      const mockLocation = 'inplay';
      location.path.and.returnValue(mockLocation);
      expect(component.checkForFiveASideUrl()).toBeFalsy();
    });
  });

  describe('@subscribeToNetworkIndicatorStatus', () => {
    it('Should subscribe to NW_I_STATUS and update NW_I_Object if isMobile is true', () => {
      const update = {
        displayText: 'Test display text',
        networkSpeed: 'slow',
        infoMsg: 'message'
      } as any;
      device.isMobile = true;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS) {
          fn(update);
        }
      });
      component.ngOnInit();
      expect(component.NW_I_Object).toEqual(update);
    });
    it('Should not subscribe to NW_I_STATUS and update NW_I_Object if isMobile is false', () => {
      const update = {
        displayText: 'Test display text',
        networkSpeed: 'slow',
        infoMsg: 'message'
      } as any;
      device.isMobile = false;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === NETWORK_CONSTANTS.NW_I_STATUS) {
          fn(update);
        }
      });
      component.ngOnInit();
      expect(component.NW_I_Object).not.toEqual(update);
    });
  });
});
