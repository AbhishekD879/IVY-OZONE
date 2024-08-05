import { of, Subject } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { VanillaAuthService } from '@ladbrokesMobile/vanillaInit/services/vanillaAuth/vanilla-auth.service';

describe('VanillaAuthService', () => {
  let service: VanillaAuthService;
  let ngZone;
  let
    vanillaUser,
    user,
    nativeBridgeService,
    awsService,
    pubsub,
    coreToolsService,
    filtersService,
    vanillaLoginDialogService,
    balanceService,
    afterLoginNotifications,
    authService,
    vanillaAuth,
    accountUpgradeLinkService,
    nativeBridgeAdapter,
    freeBetsBadgeLoader,
    storage,
    windowRef,
    router,
    sessionService,
    proxyHeadersService,
    device,
    claimsService,
    rememberMeStatusService,
    navigationService,
    germanSupportService,
    cmsService;
  const balanceProperties = {
    accountBalance: 10.00,
    balanceForGameType: 10.00,
    bonusWinningsRestrictedBalance: 0,
    cashoutRestrictedBalance: 0,
    cashoutableBalance: 10.00,
    cashoutableBalanceReal: 10.00,
    availableBalance: 10.00,
    depositRestrictedBalance: 0,
    inPlayAmount: 0,
    releaseRestrictedBalance: 0,
    playMoneyBalance: -1,
    playMoneyInPlayAmount: -1,
    owedAmount: 0,
    taxWithheldAmount: 0,
    pokerWinningsRestrictedBalance: 0,
    cashoutRestrictedCashBalance: 0,
    payPalBalance: 0,
    currency: {
      id: 'EUR',
      name: 'Euro'
    }
  };
  const afterClosedResult = {};

  const dialogRef = {
    close: jasmine.createSpy(),
    afterClosed: jasmine.createSpy().and.returnValue(of(afterClosedResult))
  };

  beforeEach(() => {
    ngZone = {
      run: jasmine.createSpy('run').and.callFake((fn) => fn())
    };

    vanillaUser = {
      isAuthenticated: true,
      ssoToken: 'ssoToken',
      firstName: 'firstName',
      lastName: 'lastName',
      tierCode: '1',
      username: 'username',
      currency: 'currency',
      customerId: 'customerId',
      email: 'email',
      country: 'country',
      dateOfBirth: 'dateOfBirth',
      isFirstLogin: true,
      title: 'title',
      balanceProperties: {
        availableBalance: 10
      },
      events: new Subject()
    };
    user = {
      logout: jasmine.createSpy(),
      login: jasmine.createSpy(),
      set: jasmine.createSpy(),
      initProxyAuth: jasmine.createSpy(),
      resolveOpenApiAuth: jasmine.createSpy(),
      resolveProxyAuth: jasmine.createSpy(),
      rejectProxyAuth: jasmine.createSpy(),
      username: 'username',
      initAuthPromises: jasmine.createSpy(),
      isRestoredBppUser: jasmine.createSpy().and.returnValue(true),
      setTouchIdLogin: jasmine.createSpy(),
      getPostLoginBonusSupValue: jasmine.createSpy()
    };
    nativeBridgeService = {
      onBalanceChanged: jasmine.createSpy(),
      logout: jasmine.createSpy(),
      onClosePopup: jasmine.createSpy('onClosePopup'),
      onCloseLoginDialog: jasmine.createSpy('onCloseLoginDialog'),
      pageLoaded: jasmine.createSpy('pageLoaded'),
      hideSplashScreen: jasmine.createSpy('hideSplashScreen'),
      onOpenPopup: jasmine.createSpy('onOpenPopup'),
      loginIfExist: jasmine.createSpy(),
      loginSalesForce: jasmine.createSpy(),
      loginSessionToken: jasmine.createSpy(),
      profileid: 'profileid',
      creferer: 'creferer',
      isWrapperStream: of(false),
      getMobileOperatingSystem: jasmine.createSpy('getMobileOperatingSystem')
    };
    awsService = {
      addAction: jasmine.createSpy(),
      getUniqueSubscriberName: jasmine.createSpy('getUniqueSubscriberName').and.returnValue(`awsFirSubscr_${new Date().getTime()}`)
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback()),
      API: pubSubApi,
      publish: jasmine.createSpy()
    };
    coreToolsService = {
      getCurrencySymbolFromISO: jasmine.createSpy().and.returnValue('$')
    };
    filtersService = {
      currencyPosition: jasmine.createSpy().and.returnValue('10$')
    };
    vanillaLoginDialogService = {
      open: jasmine.createSpy().and.returnValue(dialogRef)
    };
    balanceService = {
      balanceProperties: {
        subscribe: jasmine.createSpy().and.returnValue(Promise.resolve(balanceProperties))
      },
      refresh: jasmine.createSpy()
    };
    afterLoginNotifications = {
      start: jasmine.createSpy()
    };
    authService = {
      bppAuthSequence: jasmine.createSpy(),
      innerSessionLoggedIn: {
        observers: [],
        next: jasmine.createSpy()
      }
    };
    vanillaAuth = {
      isAuthenticated: jasmine.createSpy().and.returnValue(Promise.resolve(false)),
      logout: jasmine.createSpy()
    };
    freeBetsBadgeLoader = {
      addBadgesToVanillaElements: jasmine.createSpy(),
      addOddsBoostCounter: jasmine.createSpy()
    };
    accountUpgradeLinkService = {
      businessPhase: jasmine.createSpy()
    };
    nativeBridgeAdapter = {
      nativeEventObservable: jasmine.createSpy('nativeBridgeAdapter.nativeEventObservable').and.returnValue(of({})),
      doNativeLogin: jasmine.createSpy('doNativeLogin')
    };
    storage = {
      set: jasmine.createSpy('set'),
      setCookie: jasmine.createSpy('setCookie'),
      getCookie: jasmine.createSpy('getCookie'),
    };
    windowRef = {
      nativeWindow: {
        location: {},
        clientConfig: {
          vnBalanceProperties: 1
        }
      }
    };
    router = {
      navigateTo: jasmine.createSpy(),
      navigate: jasmine.createSpy()
    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve({})),
      whenSession: jasmine.createSpy('whenSession').and.returnValue(Promise.resolve()),
    };
    proxyHeadersService = {
      generateBppAuthHeaders:  jasmine.createSpy('generateBppAuthHeaders')
    };
    device = {
      isiOS: jasmine.createSpy('device is IOS').and.returnValue(true)
    };
    claimsService = {
      get: jasmine.createSpy('get')
    };
    rememberMeStatusService = {
      tokenExists: jasmine.createSpy('tokenExists')
    };
    navigationService = {
      goToRegistration: jasmine.createSpy('goToRegistration'),
      goToLogin: jasmine.createSpy('goToLogin')
    };
    germanSupportService = {
      redirectToMainPageOnLogin: jasmine.createSpy('redirectToMainPage')
    };
    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig')
    };
    service = new VanillaAuthService(
      vanillaUser,
      user,
      nativeBridgeService,
      awsService,
      pubsub,
      coreToolsService,
      filtersService,
      vanillaLoginDialogService,
      balanceService,
      afterLoginNotifications,
      authService,
      vanillaAuth,
      claimsService,
      freeBetsBadgeLoader,
      accountUpgradeLinkService,
      nativeBridgeAdapter,
      storage,
      windowRef,
      router,
      sessionService,
      proxyHeadersService,
      device,
      rememberMeStatusService,
      navigationService,
      cmsService,
      germanSupportService,
      ngZone
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  describe('mapUserData', () => {
    it('should set countryCode to country', () => {
      service['mapUserData']();
      expect(storage.set.calls.allArgs()[2]).toEqual(['countryCode', 'country']);
    });
  });

  it('#login should call correct methods for Ladbrokes', () => {
    service['login']();
    expect(service['germanSupportService'].redirectToMainPageOnLogin).toHaveBeenCalledTimes(1);
  });
  it('#login should call correct methods for Ladbrokes', () => {
    user.getPostLoginBonusSupValue = jasmine.createSpy('getPostLoginBonusSupValue').and.returnValue(true);
    service['login']();
    expect(service['germanSupportService'].redirectToMainPageOnLogin).toHaveBeenCalledTimes(1);
  });
});
