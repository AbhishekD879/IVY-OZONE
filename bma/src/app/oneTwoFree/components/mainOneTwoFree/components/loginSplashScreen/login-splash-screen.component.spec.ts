import { LoginSplashScreenComponent } from './login-splash-screen.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('LoginSplashScreenComponent', () => {
  let component;
  let pubSubService;
  let router;
  let routingState;
  let windowRef;
  let deviceService;
  let accountUpgradeLinkService;
  let windowRefService;
  let gtmService;
  
  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    router = {
      navigate: jasmine.createSpy()
    };

    deviceService = {
      isMobile: true
    };

    routingState = {
      getPreviousUrl: jasmine.createSpy().and.returnValue('/some-custom-page')
    };

    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/1-2-free'
        }
      }
    };

    accountUpgradeLinkService = {
      inShopToMultiChannelLink: { get: () => null }
    };

    windowRefService = {
      nativeWindow: {
        location: {
          href: ''
        }
      }
    };

    gtmService = {
      push: jasmine.createSpy()
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
   

    component = new LoginSplashScreenComponent(
      pubSubService as any,
      router as any,
      routingState as any,
      windowRef as any,
      deviceService as any,
      accountUpgradeLinkService as any,
      windowRefService as any,
      gtmService as any
    );
    component.loginBtnClicked = false;
    component.isInShopUser = false;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call removeEventListener onDestroy component', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe)
      .toHaveBeenCalledWith('LoginSplashScreen');
  });

  it('should change processing status on login modal close', () => {
    component.processingStatus = true;
    pubSubService.subscribe.and.callFake((name, api, fn) => {
      if (api !== pubSubService.API.LOGIN_BUTTON_CLICKED) {
        fn();
      }
    });
    component.ngOnInit();
    expect(component.processingStatus).toEqual(false);
  });

  it('should RESET `processingStatus` & `loginBtnClicked` on failed login', () => {
    component.processingStatus = true;
    component.loginBtnClicked = true;
    pubSubService.subscribe.and.callFake((name, api, fn) => {
      if (api === pubSubService.API.FAILED_LOGIN) {
        fn();
      }
    });
    component.ngOnInit();
    expect(component.processingStatus).toEqual(false);
    expect(component.loginBtnClicked).toEqual(false);
  });

  it('should NOT change processing status on login modal close after LOGIN click', () => {
    expect(component.loginBtnClicked).toEqual(false);
    component.processingStatus = true;
    component.hiddenLoginModal = true;
    pubSubService.subscribe.and.callFake((name, api, fn) => {
      if (api !== pubSubService.API.FAILED_LOGIN) {
        fn();
      }
    });
    component.ngOnInit();
    expect(component.loginBtnClicked).toEqual(true);
    expect(component.processingStatus).toEqual(true);
  });

  it('should set `processing status` to true on login submit', () => {
    component['invokeLoginHandler']();
    expect(component.processingStatus).toEqual(true);
  });

  describe('Test `cancelLoginHandler` behaviour', () => {
    beforeEach(() => {
      component = new LoginSplashScreenComponent(
        pubSubService as any,
        router as any,
        routingState as any,
        windowRef as any,
        deviceService as any,
        accountUpgradeLinkService as any,
        windowRefService as any,
        gtmService as any
      );
    });

    it('should redirect to root', () => {
      component['routingState'] = {
        getPreviousUrl: jasmine.createSpy().and.returnValue('/')
      };

      component.cancelLoginHandler();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should redirect to root if `this.routingState.getPreviousUrl()` return *null*', () => {
      component['routingState'] = {
        getPreviousUrl: jasmine.createSpy().and.returnValue(null)
      };

      component.cancelLoginHandler();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should redirect to `some-custom-page`, i.e. previous page', () => {
      component.cancelLoginHandler();
      expect(router.navigate).toHaveBeenCalledWith(['/some-custom-page']);
    });

    it('should redirect to `root` if this.routingState.getPreviousUrl() return current pathname', () => {
      component['windowRef'] = {
        nativeWindow: {
          location: {
            pathname: '/some-custom-page'
          }
        }
      };

      component.cancelLoginHandler();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should set splash logo to landscape is app loaded NOT via mobile', () => {
      component['deviceService'] = {
        isMobile: false
      };

      environment.ONE_TWO_FREE_ENDPOINT = 'http://localhost/';

      component.ngOnInit();
      expect(component.splashTitle).toEqual('http://localhost/assets/1-2-free_logo_landscape.svg');
    });
  });

  describe('#playHandler', () => {
    it('should redirect user to upgrade journey link if USER is INSHOP', () => {
      const gtmData = {
        event: 'trackEvent',
        eventCategory: 'cta',
        eventAction: 'upgrade account',
        eventLabel: 'yes - upgrade Account'
      };

      Object.defineProperty(component['accountUpgradeLinkService'], 'inShopToMultiChannelLink', { get: () => 'http://ffs.com' });

      component['isInShopUser'] = true;

      component.playHandler();

      expect(component.gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
      expect(component['windowRefService'].nativeWindow.location.href).toEqual('http://ffs.com');
    });

    it('should invoke login if USER is NOT INSHOP', () => {
      spyOn(component.invokeLogin, 'emit');

      component.playHandler();

      expect(component['processingStatus']).toBeTruthy();
      expect(component['invokeLogin'].emit).toHaveBeenCalledTimes(1);
    });

    it('gaTaggingPush', () => {

      component['gaTaggingPush']('test1','test2','test3');

      expect(component.gtmService.push).toHaveBeenCalled();
    });
  });

});
