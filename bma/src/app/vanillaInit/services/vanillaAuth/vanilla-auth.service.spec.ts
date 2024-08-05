import {
  NativeEvent,
  UserAutologoutEvent,
  UserLoggingInEvent,
  UserLoginEvent,
  UserLoginFailedEvent,
  UserLogoutEvent,
  UserUpdateEvent
} from '@frontend/vanilla/core';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import {
  VanillaAuthService
} from '@vanillaInitModule/services/vanillaAuth/vanilla-auth.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';
import { PortalNativeEvents } from '@vanillaInitModule/services/PortalNativeEventNotifier/portal-nativeEvents';
import { VANILLA_NATIVE_EVENTS } from '@vanillaInitModule/services/NativeBridgeAdapter/nativeEvents';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';

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
    storage,
    freeBetsBadgeLoader,
    windowRef,
    router,
    sessionService,
    proxyHeadersService,
    device,
    claimsService,
    rememberMeStatusService,
    navigationService,
    userInterfaceConfig;

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
      getTouchIdLogin: jasmine.createSpy('getTouchIdLogin'),
      setSportsUserName: jasmine.createSpy(),
      bppToken: 'Aoz_tendkshhe',
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
      appSeeTrackAction: jasmine.createSpy('appSeeTrackAction'),
      loginError: jasmine.createSpy('loginError'),
      touchIDLoginFailedIfExist: jasmine.createSpy('touchIDLoginFailedIfExist'),
      tdpeh: 'tdpeh',
      profileid: 'profileid',
      creferer: 'creferer',
      isWrapperStream: of(false),
      loginWithTouchID: jasmine.createSpy('loginWithTouchID'),
      getMobileOperatingSystem: jasmine.createSpy('getMobileOperatingSystem').and.returnValue('ios')
    };
    awsService = {
      addAction: jasmine.createSpy(),
      getUniqueSubscriberName: jasmine.createSpy('getUniqueSubscriberName').and.returnValue(`awsFirSubscr_${new Date().getTime()}`)
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback()),
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync')
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
        subscribe: jasmine.createSpy()
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
      },
      initOddsBoost: jasmine.createSpy('initOddsBoost').and.returnValue(of([])),
      getOddspreference: jasmine.createSpy()
    };
    vanillaAuth = {
      isAuthenticated: jasmine.createSpy().and.returnValue(Promise.resolve(false)),
      logout: jasmine.createSpy()
    };
    freeBetsBadgeLoader = {
      addBadgesToVanillaElements: jasmine.createSpy(),
      addBetpackCounter: jasmine.createSpy()
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
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn, time) => { fn(); }),
        clientConfig: {
          vnBalanceProperties: {
            availableBalance: 10
          }
        }
      },
      document: {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((listenerName, cb) => {
          cb && cb();
        })
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
    userInterfaceConfig = {
      homeBiometric: {
        android: true,
        ios: true 
      }
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
      userInterfaceConfig,
      ngZone
    );
  });

  describe('#init', () => {
    describe('#init - UserLoginEvent handling', () => {
      let event;
      beforeEach(() => {
        event = new UserLoginEvent();
        service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
        service['freebetCounterUpdate'] = jasmine.createSpy();
        
        pubsub.subscribe.and.callFake((a, b, cb) => cb());
      });

      it('should trigger userFinishedLogin status', fakeAsync(() => {
        service.init();

        expect(service['user'].userFinishedLogin).toBeFalsy();

        vanillaUser.events.next(event);

        tick();

        expect(service['user'].userFinishedLogin).toBeTruthy();
        expect(service['loginSequence']).toHaveBeenCalled();
      }));

      it('should set isOSPermitted-undefined userInterfaceConfig.homeBiometric not available', fakeAsync(() => {
        service['userInterfaceConfig'] = {} as any;
        service.init();

        expect(service['user'].userFinishedLogin).toBeFalsy();

        vanillaUser.events.next(event);

        tick();

        expect(service['isOSPermitted']).toBeUndefined();
      }));

      it('should set isOSPermitted-undefined userInterfaceConfig.homeBiometric null', fakeAsync(() => {
        service['userInterfaceConfig'] = {homeBiometric: null} as any;
        service.init();

        expect(service['user'].userFinishedLogin).toBeFalsy();

        vanillaUser.events.next(event);

        tick();

        expect(service['isOSPermitted']).toBeUndefined();
      }));

      it('should trigger userFinishedLogin status, checkDeviceOS returns false', fakeAsync(() => {
        service.init();

        expect(service['user'].userFinishedLogin).toBeFalsy();

        vanillaUser.events.next(event);

        tick();

        expect(service['user'].userFinishedLogin).toBeTruthy();
        expect(service['loginSequence']).toHaveBeenCalled();
      }));

      it('should trigger loginSequence', () => {
        spyOn(service, 'isLoggedIn').and.returnValue(true);
        service.init();
        vanillaUser.events.next(event);
        expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({loginPending: false}));
        expect(service['loginSequence']).toHaveBeenCalled();
      });

      describe('should check user status', () => {
        beforeEach(() => {
          spyOn(service, 'setLogoutStatus' as any);
          spyOn(service, 'isLoggedIn').and.returnValue(false);
          pubsub.subscribe = jasmine.createSpy('subscribe');  // avoid callback call for these two tests
        });

        it('and log out', () => {
          service.init();

          expect(nativeBridgeService.logout).toHaveBeenCalled();
        });

        it('log out and prevent IOS native app to hide home page too early', () => {
          pubsub.subscribe.and.callFake((s, c, fn) => fn());  // avoid callback call for these test
          spyOn(service as any, 'loadNative');
          device.isIos = true;
          service.init();

          expect(nativeBridgeService.logout).not.toHaveBeenCalled();
        });

        it('log out and prevent IOS native app to hide home page too early, checkDeviceOS is false and touchIDConfigured is true', () => {
          pubsub.subscribe.and.callFake((s, c, fn) => fn());  // avoid callback call for these test
          spyOn(service as any, 'loadNative');
          device.isIos = true;
          nativeBridgeService.touchIDConfigured = true;
          user.getTouchIdLogin.and.returnValue('enabled');
          service.init();

          expect(nativeBridgeService.logout).not.toHaveBeenCalled();
        });

        afterEach(() => {
          expect(service['isLoggedIn']).toHaveBeenCalled();
          expect(service['setLogoutStatus']).toHaveBeenCalledWith(jasmine.any(String));
        });
      });

      it('should handle UserLoginEvent storing OXI rememberMe token on autologin', () => {
        const nativeEvent: NativeEvent = {
          eventName: PortalNativeEvents.Login,
          parameters: {
            type: 'Autologin'
          }
        };
        spyOn(service, 'handleMobileAutoLogin').and.callThrough();
        service.handleMobileAutoLogin(nativeEvent);
        expect(storage.set).toHaveBeenCalledWith('rememberMe', 1);
      });

      it('should handle UserLoginEvent storing OXI rememberMe token on manual login', () => {
        const nativeEvent: NativeEvent = {
          eventName: PortalNativeEvents.Login,
          parameters: {
            type: 'Manual'
          }
        };
        spyOn(service, 'handleMobileAutoLogin').and.callThrough();
        service.handleMobileAutoLogin(nativeEvent);
        expect(storage.set).not.toHaveBeenCalled();
      });
    });

    it('#init should handle UserLogoutEvent', () => {
      const event = new UserLogoutEvent();
      event.isManualLogout = true;
      service['setLogoutStatus'] = jasmine.createSpy();
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({loginPending: false}));
      expect(service['setLogoutStatus']).toHaveBeenCalledWith('Logout by vanilla event: UserLogoutEvent');
      expect(service['loginSequence']).toHaveBeenCalled();
    });

    it('#init should handle UserAutologoutEvent', () => {
      const event = new UserAutologoutEvent();
      service['setLogoutStatus'] = jasmine.createSpy();
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({loginPending: false}));
      expect(service['setLogoutStatus']).toHaveBeenCalledWith('Logout by vanilla event: UserAutologoutEvent');
      expect(service['loginSequence']).toHaveBeenCalled();
    });

    it('#init should handle UserLoggingInEvent', () => {
      const event = new UserLoggingInEvent();
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(service['loginSequence']).toHaveBeenCalled();
    });

    it('#init should handle UserUpdateEvent', () => {
      const event = new UserUpdateEvent(null);
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(service['loginSequence']).toHaveBeenCalled();
    });

    it('#init should handle some general event when user is logged in', () => {
      const event = new Event(null);
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(pubsub.subscribe).toHaveBeenCalledWith('authFactory', 'RELOAD_COMPONENTS', jasmine.any(Function));
      expect(service['loginSequence']).toHaveBeenCalled();
    });

    it('#init should handle UserLoginFailedEvent', () => {
      const event = new UserLoginFailedEvent();

      service.init();
      vanillaUser.events.next(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FAILED_LOGIN);
      expect(user.set).toHaveBeenCalledWith({ loginPending: false });
    });

    it('#init should subscribe to balance update service', () => {
      service['setBalance'] = jasmine.createSpy('setBalance');
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      balanceService.balanceProperties.subscribe.and.callFake((callback) => {
        balanceProperties && callback(balanceProperties);
      });
      service.init();
      expect(service['loginSequence']).toHaveBeenCalled();
      expect(balanceService.balanceProperties.subscribe).toHaveBeenCalled();
      expect(service['setBalance']).toHaveBeenCalledWith(balanceProperties as any);
    });

    it('#init should not run setBalance after event', () => {
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      balanceService.balanceProperties.subscribe.and.callFake((callback) => {
        callback(false);
      });
      service['setBalance'] = jasmine.createSpy('setBalance');
      service.init();
      expect(service['setBalance']).not.toHaveBeenCalled();
    });

    it('#init should handle some general event when user is logged out', () => {
      const event = new Event(null);
      service['vanillaUser']['isAuthenticated'] = false;
      service['setLogoutStatus'] = jasmine.createSpy();
      service.init();
      vanillaUser.events.next(event);
      expect(pubsub.subscribe).toHaveBeenCalledWith('authFactory', 'RELOAD_COMPONENTS', jasmine.any(Function));
      expect(service['setLogoutStatus']).toHaveBeenCalledWith('Logout on VanillaAuthService init(vanillaUser.isAuthenticated: false)');
    });

    it('#init should call handleReloadComponentsEvent', () => {
      const event = new Event(null);
      service['handleReloadComponentsEvent'] = jasmine.createSpy();
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      expect(service['loginSequence']).toHaveBeenCalled();
      expect(service['handleReloadComponentsEvent']).toHaveBeenCalled();
    });

    it('#init should call triggerLoginDialog and an "action" method', () => {
      const event = new Event(null);
      const syncEvent = {
        placeBet: 'betslip',
        moduleName: 'betslip',
        action: jasmine.createSpy()
      };
      service['pubsub']['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
        if (method === pubsub.API.OPEN_LOGIN_DIALOG) {
          callback(syncEvent);
        } else if (method === pubsub.APP_IS_LOADED) {
        callback();
        }
      });
      service['triggerLoginDialog'] = jasmine.createSpy().and.returnValue(of(undefined));
      service['loginSequence'] = jasmine.createSpy().and.returnValue(of(undefined));
      service.init();
      vanillaUser.events.next(event);
      // expect(service['loginSequence']).toHaveBeenCalled();
      expect(service['pubsub']['subscribe'])
        .toHaveBeenCalledWith('vanillaAuthService', pubsub.API.OPEN_LOGIN_DIALOG, jasmine.any(Function));
      expect(syncEvent.action).toHaveBeenCalled();
      expect(service['triggerLoginDialog']).toHaveBeenCalled();
    });

    it('trigger APP_IS_LOADED with valid touchIDConfigured', () => {
      nativeBridgeService.touchIDConfigured = true;
      service['vanillaUser'].isAuthenticated = false;
      user.getTouchIdLogin.and.returnValue('enabled');
      service.init();
      expect(nativeBridgeService.loginWithTouchID).toHaveBeenCalledWith(false, '', false);
    });

    it('trigger APP_IS_LOADED with invalid touchIDConfigured', () => {
      nativeBridgeService.touchIDConfigured = false;
      service['userInterfaceConfig'].homeBiometric = { android: false, ios: false };
      service['vanillaUser'].isAuthenticated = false;
      user.getTouchIdLogin.and.returnValue('enabled');
      service['runBiometricLogin']();
      expect(nativeBridgeService.loginWithTouchID).not.toHaveBeenCalledWith(false, '', false);
    });

    it('trigger APP_IS_LOADED with valid touchIDConfigured, biometric false', () => {
      nativeBridgeService.touchIDConfigured = true;
      service['userInterfaceConfig'].homeBiometric = { android: false, ios: false };
      service['vanillaUser'].isAuthenticated = false;
      user.getTouchIdLogin.and.returnValue('enabled');
      service['runBiometricLogin']();
      expect(nativeBridgeService.loginWithTouchID).toHaveBeenCalledWith(false, '', false);
    });

    it('#init should call triggerNativeEvents when it is wrapper', () => {
      nativeBridgeService.isWrapperStream = of(true);
      service['triggerNativeEvents'] = jasmine.createSpy();
      service.init();
      expect(service['triggerNativeEvents']).toHaveBeenCalled();
    });
  });

  describe('loginDialogExists', () => {
    it('should return proper value based on dialog existence', () => {
      service['loginDialogOpened'] = false;
      expect(service.loginDialogExists()).toBe(false);

      service['loginDialogOpened'] = true;
      expect(service.loginDialogExists()).toBe(true);
    });
  });

  describe('#triggerLoginDialog', () => {
    it('#triggerLoginDialog should call correct methods and return correct results', () => {
      service['loginDialogOpened'] = false;
      const openedBy = 'openedBy';

      service.triggerLoginDialog(openedBy).subscribe((result) => {
        expect(result).toBe(afterClosedResult);
      });
      expect(vanillaLoginDialogService.open).toHaveBeenCalledWith(jasmine.objectContaining({openedBy}));
      expect(dialogRef.afterClosed).toHaveBeenCalled();
    });

    it('#triggerLoginDialog should call correct methods and return correct results when no params were passed', () => {
      service.triggerLoginDialog().subscribe((result) => {
        expect(result).toBe(afterClosedResult);
      });
      expect(vanillaLoginDialogService.open).toHaveBeenCalledWith(jasmine.objectContaining({}));
      expect(dialogRef.afterClosed).toHaveBeenCalled();
    });

    it('#should return empty stream and do not open login dialog if it already exists', () => {
      service['loginDialogOpened'] = true;
      const openedBy = 'openedBy';
      service.triggerLoginDialog(openedBy).subscribe((result) => {
        expect(result).toBe(null);
      });
    });
  });
  it('handleRegistrationRedirection should not close dialog', () => {
    expect(service['loginDialog']).toBeUndefined();
    service.handleRegistrationRedirection();
    expect(nativeBridgeService.onClosePopup).not.toHaveBeenCalled();
    expect(nativeBridgeService.onCloseLoginDialog).not.toHaveBeenCalled();
    expect(navigationService.goToRegistration).toHaveBeenCalled();
  });
  it('should check handleRegistrationRedirection method', () => {
    expect(service['loginDialog']).toBeUndefined();
    service.triggerLoginDialog('').subscribe((result) => {
      expect(result).toBe(afterClosedResult);
    });
    service.triggerLoginDialog();
    expect(service['loginDialog']).toBeDefined();
    service.handleRegistrationRedirection();
    expect(service['loginDialog']['close']).toHaveBeenCalledWith({openedBy: service['registrationRedirectEventName']});
    expect(navigationService.goToRegistration).toHaveBeenCalled();
  });

  it('should check if user is logged in', () => {
    expect(service['isLoggedIn']()).toBeTruthy();
  });

  it('#setLogoutStatus should call correct methods', () => {
    const logoutReason = 'some_reason';
    service['setLogoutStatus'](logoutReason);
    expect(awsService.addAction)
      .toHaveBeenCalledWith('vanillaAuth=>logout', jasmine.objectContaining({logoutReason}), service['subscriberName']);
    expect(user.logout).toHaveBeenCalled();
  });

  it('#login should call correct methods', () => {
    service['login']();
    expect(user.login).toHaveBeenCalledWith(vanillaUser.ssoToken);
    expect(user.resolveOpenApiAuth).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('LOGIN_PENDING', true);
    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.SESSION_LOGIN,
      jasmine.arrayContaining([jasmine.objectContaining({User: user, options: {}})]));
    expect(authService.innerSessionLoggedIn.next).toHaveBeenCalled();
  });

  describe('mapUserData', () => {

    it('#should call correct methods', () => {
      service['mapUserData']();
      expect(user.set).toHaveBeenCalledWith({
        firstname: 'firstName',
        lastname: 'lastName',
        vipLevel: null,
        username: 'username',
        currencyCode: 'currency',
        playerCode: 'cl_username',
        email: 'email',
        countryCode: 'country',
        birthDate: 'dateOfBirth',
        accountBusinessPhase: jasmine.any(Function),
        sseToken: 'ssoToken',
        sessionToken: 'ssoToken',
        firstLogin: true,
        isAuthenticated: true,
        title: 'title'
      });
      expect(user.set).toHaveBeenCalledWith({
        currency: 'currency',
        currencySymbol: '$',
        sportBalance: '10',
        sportBalanceWithSymbol: '10$'
      });
    });

    it('should set existingUser to true', () => {
      service['mapUserData']();
      expect(storage.set).toHaveBeenCalledWith('existingUser', true);
    });

    it('should pull data from claimsService', () => {
      service['mapUserData']();
      expect(claimsService.get).toHaveBeenCalledWith('tierCode');
    });

    it('#vipLevel (tireCode) = -1', () => {
      claimsService.get.and.returnValue('-1');
      service['mapUserData']();
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({ vipLevel: null }));
      expect(storage.set).toHaveBeenCalledWith('vipLevel', null);
      expect(storage.setCookie).toHaveBeenCalledWith('lbrims', null, environment.DOMAIN, 30, false);
    });

    it('#vipLevel (tireCode) = null', () => {
      claimsService.get.and.returnValue(null);
      service['mapUserData']();
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({ vipLevel: null }));
      expect(storage.set).toHaveBeenCalledWith('vipLevel', null);
      expect(storage.setCookie).toHaveBeenCalledWith('lbrims', null, environment.DOMAIN, 30, false);
    });

    it('#vipLevel (tireCode) = 0', () => {
      claimsService.get.and.returnValue('0');
      service['mapUserData']();
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({ vipLevel: null }));
      expect(storage.set).toHaveBeenCalledWith('vipLevel', null);
      expect(storage.setCookie).toHaveBeenCalledWith('lbrims', null, environment.DOMAIN, 30, false);
    });

    it('#vipLevel (tireCode) = 9', () => {
      claimsService.get.and.returnValue('9');
      service['mapUserData']();
      expect(user.set).toHaveBeenCalledWith(jasmine.objectContaining({ vipLevel: '9' }));
      expect(storage.set).toHaveBeenCalledWith('vipLevel', '9');
      expect(storage.setCookie).toHaveBeenCalledWith('lbrims', '9', environment.DOMAIN, 30, false);
    });

    it('should publish SET_PLAYER_INFO event', () => {
      service['mapUserData']();

      expect(service['pubsub'].publish).toHaveBeenCalledWith('SET_PLAYER_INFO', service['user']);
    });
  });

  it('loginSequence if user is already logged in', () => {
    service['mapUserData'] = jasmine.createSpy();
    service['login'] = jasmine.createSpy();
    authService.bppAuthSequence = jasmine.createSpy().and.returnValue(of({}));
    service['loginSequence']('test').subscribe();
    expect(service['mapUserData']).toHaveBeenCalled();
    expect(service['login']).toHaveBeenCalled();
    expect(proxyHeadersService.generateBppAuthHeaders).toHaveBeenCalled();
    expect(user.resolveProxyAuth).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.STORE_FREEBETS_ON_REFRESH);
  });

  it('loginSequence if user logging in', () => {
    service['mapUserData'] = jasmine.createSpy();
    service['login'] = jasmine.createSpy();
    authService.bppAuthSequence = jasmine.createSpy().and.returnValue(of({}));
    user.isRestoredBppUser =  jasmine.createSpy().and.returnValue(false);
    service['loginSequence']('test').subscribe();
    expect(service['mapUserData']).toHaveBeenCalled();
    expect(service['login']).toHaveBeenCalled();
    expect(authService.bppAuthSequence).toHaveBeenCalled();
    expect(afterLoginNotifications.start).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('LOGIN_PENDING', false);
    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.SUCCESSFUL_LOGIN);
  });

  it('#setBalance should call correct methods', () => {
    const sportBalance = vanillaUser.balanceProperties.availableBalance;
    const currencySymbol: string = coreToolsService.getCurrencySymbolFromISO(vanillaUser.currency);
    service['setBalance'](vanillaUser.balanceProperties);
    expect(user.set).toHaveBeenCalledWith({
      currency: vanillaUser.currency,
      currencySymbol: currencySymbol,
      sportBalance: String(sportBalance),
      sportBalanceWithSymbol: filtersService.currencyPosition(Number(sportBalance).toFixed(2), currencySymbol)
    });
    expect(nativeBridgeService.onBalanceChanged).toHaveBeenCalledWith({ amount: String(sportBalance) });
  });

  it('refreshBalance should return promise', () => {
    const promise = Promise.resolve();
    service['balanceService'].refresh = jasmine.createSpy().and.returnValue(promise);
    // expect(service.refreshBalance()).toBe(promise);
    service.refreshBalance();
    expect(service['balanceService'].refresh).toHaveBeenCalled();
  });

  describe('handleReloadComponentsEvent', () => {
    it('should logout if not authenticated and User was logged in and no remember me cookie', fakeAsync(() => {
      rememberMeStatusService.tokenExists.and.returnValue(false);
      windowRef.nativeWindow.location.origin = 'http://test';
      service['setLogoutStatus'] = jasmine.createSpy();
      service['vanillaUser'].isAuthenticated = true;
      service['handleReloadComponentsEvent']();

      tick();

      expect(nativeBridgeService['logout']).toHaveBeenCalled();
      expect(service['setLogoutStatus']).toHaveBeenCalledWith('Logout by handleReloadComponentsEvent');
      expect(windowRef.nativeWindow.location.href).toEqual('http://test');
    }));

    it('should not logout if authenticated', fakeAsync(() => {
      vanillaAuth.isAuthenticated = jasmine.createSpy().and.returnValue(Promise.resolve(true));
      windowRef.nativeWindow.location.origin = 'http://test';
      service['handleReloadComponentsEvent']();
      tick();
      expect(nativeBridgeService['logout']).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.location.href).not.toEqual('http://test');
    }));

    it('should not logout if was not logged in before', fakeAsync(() => {
      service['vanillaUser'].isAuthenticated = false;
      windowRef.nativeWindow.origin = 'http://test';
      service['handleReloadComponentsEvent']();
      tick();
      expect(nativeBridgeService['logout']).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.location.href).not.toEqual('http://test');
    }));

    it('should not logout if remember me cookie exist', fakeAsync(() => {
      rememberMeStatusService.tokenExists.and.returnValue(true);
      windowRef.nativeWindow.origin = 'http://test';
      service['handleReloadComponentsEvent']();
      tick();
      expect(nativeBridgeService['logout']).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.location.href).not.toEqual('http://test');
    }));
  });

  it('afterLoginDialogClose', () => {
    service['afterLoginDialogClose']();
    expect(nativeBridgeService.onClosePopup).toHaveBeenCalled();
  });

  describe('loadNative', () => {
    it('should trigger native methods', () => {
      service['device'].isIos = false;

      service['loadNative']();

      expect(nativeBridgeService.hideSplashScreen).toHaveBeenCalled();
      expect(nativeBridgeService.pageLoaded).toHaveBeenCalled();
      expect(nativeBridgeService.logout).not.toHaveBeenCalled();
    });

    it('should trigger native methods - andriod', () => {
      service['device'].isIos = false;
      service['device'].isAndroid = true;

      service['loadNative']();

      expect(nativeBridgeService.hideSplashScreen).toHaveBeenCalled();
      expect(nativeBridgeService.pageLoaded).toHaveBeenCalled();
      expect(nativeBridgeService.logout).toHaveBeenCalled();
    });

    it('should call logout if ios and not logged in', () => {
      service['device'].isIos = true;
      service['vanillaUser'].isAuthenticated = false;

      service['loadNative']();

      expect(nativeBridgeService.logout).toHaveBeenCalled();
      expect(nativeBridgeService.hideSplashScreen).toHaveBeenCalled();
      expect(nativeBridgeService.pageLoaded).toHaveBeenCalled();
    });
  });

  it('changeUserMenuListener should react on menu button click on ios home-screen and redirect to vanilla menu', () => {
    windowRef.document = {
      addEventListener: jasmine.createSpy('addEventListener').and.callFake((listenerName, cb) => {
        cb && cb();
      })
    };

    service['changeUserMenuListener']();
    expect(windowRef.document.addEventListener)
      .toHaveBeenCalledWith('CHANGE_RIGHT_HAND_SLIDE_STATE', jasmine.any(Function));
    expect(router.navigate).toHaveBeenCalledWith(['en/menu']);
  });

  it('triggerNativeEvents should invoke native methods', () => {
    service['setNativeCookie'] = jasmine.createSpy();
    service['changeUserMenuListener'] = jasmine.createSpy();
    service['handleVanillaNativeEvents'] = jasmine.createSpy();
    service['subscribeToNativeEvents'] = jasmine.createSpy();

    service['triggerNativeEvents']();

    expect(service['setNativeCookie']).toHaveBeenCalled();
    expect(service['changeUserMenuListener']).toHaveBeenCalled();
    expect(service['handleVanillaNativeEvents']).toHaveBeenCalled();
    expect(service['subscribeToNativeEvents']).toHaveBeenCalled();
  });

  describe('setNativeCookie', () => {
    it('should set native app cookie if not existed', () => {
      storage.getCookie.and.returnValue(false);

      service['setNativeCookie']();

      expect(storage.setCookie).toHaveBeenCalledWith('NativeApp', 'SPORTSW');
    });

    it('should NOT set native app cookie if existed', () => {
      storage.getCookie.and.returnValue(true);

      service['setNativeCookie']();

      expect(storage.setCookie).not.toHaveBeenCalledWith('NativeApp', 'SPORTSW');
    });
  });

  describe('setAppsFlyerCookies', () => {
    it('should set AppsFlyer cookies if not existed', () => {
      storage.getCookie.and.returnValue(false);

      service['setAppsFlyerCookies']();
      expect(nativeBridgeService.profileid).not.toBeNull();
      expect(nativeBridgeService.creferer).not.toBeNull();
      expect(storage.setCookie).toHaveBeenCalledWith('trackerId', nativeBridgeService.profileid, environment.DOMAIN, 30, true);
      expect(storage.setCookie).toHaveBeenCalledWith('trackerAffiliate', nativeBridgeService.profileid, environment.DOMAIN, 1, true);
      expect(storage.setCookie).toHaveBeenCalledWith('btag', nativeBridgeService.creferer, environment.DOMAIN, 30, true);
      expect(storage.setCookie).toHaveBeenCalledWith('tdpeh', nativeBridgeService.tdpeh, environment.DOMAIN, 30, true);
    });

    it('should NOT set AppsFlyer cookies if existed', () => {
      storage.getCookie.and.returnValue(true);

      service['setAppsFlyerCookies']();
      expect(nativeBridgeService.profileid).not.toBeNull();
      expect(nativeBridgeService.creferer).not.toBeNull();
      expect(nativeBridgeService.tdpeh).not.toBeNull();
      expect(storage.setCookie).not.toHaveBeenCalledWith('trackerId', nativeBridgeService.profileid, environment.DOMAIN, 30, true);
      expect(storage.setCookie).not.toHaveBeenCalledWith('trackerAffiliate', nativeBridgeService.profileid, environment.DOMAIN, 1, true);
      expect(storage.setCookie).not.toHaveBeenCalledWith('btag', nativeBridgeService.creferer, environment.DOMAIN, 30, true);
      expect(storage.setCookie).not.toHaveBeenCalledWith('tdpeh', nativeBridgeService.tdpeh, environment.DOMAIN, 30, true);
    });

    it('should NOT set AppsFlyer cookies if nativeBridgeService profileid is null', () => {
      storage.getCookie.and.returnValue(false);
      nativeBridgeService.profileid = null;
      nativeBridgeService.creferer = 'BTAG:123';

      service['setAppsFlyerCookies']();
      expect(nativeBridgeService.profileid).toBeNull();
      expect(storage.setCookie).not.toHaveBeenCalledWith('trackerId', nativeBridgeService.profileid, environment.DOMAIN, 30, true);
      expect(storage.setCookie).not.toHaveBeenCalledWith('trackerAffiliate', nativeBridgeService.profileid, environment.DOMAIN, 1, true);
      expect(storage.setCookie).toHaveBeenCalledWith('btag', '123', environment.DOMAIN, 30, true);
    });

    it('should NOT set AppsFlyer btag cookie if nativeBridgeService creferer is null', () => {
      storage.getCookie.and.returnValue(false);
      nativeBridgeService.creferer = null;
      nativeBridgeService.tdpeh = null;

      service['setAppsFlyerCookies']();
      expect(nativeBridgeService.creferer).toBeNull();
      expect(storage.setCookie).not.toHaveBeenCalledWith('btag', nativeBridgeService.creferer, environment.DOMAIN, 30, true);
      expect(storage.setCookie).not.toHaveBeenCalledWith('tdpeh', nativeBridgeService.tdpeh, environment.DOMAIN, 30, true);
    });
  });

  describe('subscribe to PubSub', () => {
    it('IMPLICIT_BALANCE_REFRESH should call balance refresh method', () => {
      service.refreshBalance = jasmine.createSpy();

      service.init();

      expect(service.refreshBalance).toHaveBeenCalled();
    });
  });

  describe('subscribeToNativeEvents', () => {
    beforeEach(() => {
      service['triggerLoginDialog'] = jasmine.createSpy('triggerLoginDialog').and.returnValue(of(null));
    });

    it('should subscribe to native events', () => {
      service['subscribeToNativeEvents']();

      expect(windowRef.nativeWindow.doLogin).toBeDefined();
      expect(windowRef.nativeWindow.openLoginDialog).toBeDefined();
    });

    describe('triggerLoginDialog subscription on openLoginDialog', () => {

      beforeEach(() => {
        service['afterLoginDialogClose'] = jasmine.createSpy();
      });

      it('should should sync dialogs for logged in user', () => {
        service['subscribeToNativeEvents']();
        windowRef.nativeWindow.openLoginDialog();

        expect(service['loginWasChecked']).toBeFalsy();
        expect(navigationService.goToLogin).not.toHaveBeenCalled();
        expect(service['triggerLoginDialog']).toHaveBeenCalled();
        expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('Login');
        expect(pubsub.subscribe).toHaveBeenCalledWith('vanillaAuth', 'LOGIN_POPUPS_END', jasmine.any(Function));
      });
      it('should not trigger triggerLoginDialog', () => {
        service['setDialogStatus'](true);
        service['subscribeToNativeEvents']();
        windowRef.nativeWindow.openLoginDialog();
        expect(service['triggerLoginDialog']).not.toHaveBeenCalled();
        expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('Login');
      });
      it('should should call afterLoginDialogClose for logged out user', () => {
        vanillaUser.isAuthenticated = false;
        service['subscribeToNativeEvents']();
        windowRef.nativeWindow.openLoginDialog();

        expect(service['loginWasChecked']).toBeFalsy();
        expect(navigationService.goToLogin).not.toHaveBeenCalled();
        expect(service['triggerLoginDialog']).toHaveBeenCalled();
        expect(service['afterLoginDialogClose']).toHaveBeenCalled();
        expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith('Login');
      });

      it('should call onLoginDialogClose with registrationRedirect parameter', () => {
        vanillaUser.isAuthenticated = false;
        const dialogOptions = {openedBy: service['registrationRedirectEventName']};
        service.triggerLoginDialog = jasmine.createSpy().and.returnValue(of(dialogOptions));
        service['subscribeToNativeEvents']();
        windowRef.nativeWindow.openLoginDialog();
        service.handleRegistrationRedirection();
        expect(service['afterLoginDialogClose']).toHaveBeenCalledWith(true);
      });

      it('should trigger showing `touch id failed message`', () => {
        service['subscribeToNativeEvents']();
        windowRef.nativeWindow.openLoginDialog({}, 'autologinerrortouch');

        expect(service['loginWasChecked']).toBeTruthy();
        expect(navigationService.goToLogin)
          .toHaveBeenCalledWith(jasmine.objectContaining({ loginMessageKey: 'autologinerrortouch' }));
      });
    });
  });

  it('#afterLoginDialogClose should trigger nativeBridge onClosePopup method with params', () => {
    service['afterLoginDialogClose'](true);
    expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('Login', {Registration: true});
  });

  it('#afterLoginHandler', () => {
    const userData = {
      eventName: 'eventName',
      parameters: {
        userName: 'userName',
        password: 'password',
        ssoToken: 'ssoToken',
        accountId: 'accountId',
        isFromBetslip: true
      }
    };
    storage.get = jasmine.createSpy().and.returnValue('lastUsername');
    user.getTouchIdLogin = jasmine.createSpy().and.returnValue('enabled');
    service['afterLoginHandler'](userData);
    expect(storage.get).toHaveBeenCalledWith('lastUsername');
    expect(storage.set).toHaveBeenCalledWith('lastUsername', userData.parameters.userName);
    expect(nativeBridgeService.loginSalesForce).toHaveBeenCalledWith(`cl_${userData.parameters.userName}`);
    expect(nativeBridgeService.loginIfExist)
      .toHaveBeenCalledWith(userData.parameters.accountId, userData.parameters.password);
    expect(nativeBridgeService.loginSessionToken).toHaveBeenCalledWith(
      jasmine.objectContaining({
        username: userData.parameters.userName,
        sessionToken: userData.parameters.ssoToken,
        isFromBetSlip: userData.parameters.isFromBetslip
      })
    );
    expect(user.getTouchIdLogin).toHaveBeenCalled();
    expect(user.setTouchIdLogin).toHaveBeenCalledWith('disabled');
  });

  it('#afterLoginHandler should not call setTouchIdLogin when touch id is disabled', () => {
    const userData = {
      eventName: 'eventName',
      parameters: {
        userName: 'userName',
        password: 'password',
        ssoToken: 'ssoToken',
        accountId: 'accountId',
        isFromBetslip: true
      }
    };
    storage.get = jasmine.createSpy().and.returnValue('lastUsername');
    user.getTouchIdLogin = jasmine.createSpy().and.returnValue('disabled');
    service['afterLoginHandler'](userData);
    expect(storage.get).toHaveBeenCalledWith('lastUsername');
    expect(storage.set).toHaveBeenCalledWith('lastUsername', userData.parameters.userName);
    expect(nativeBridgeService.loginSalesForce).toHaveBeenCalledWith(`cl_${userData.parameters.userName}`);
    expect(nativeBridgeService.loginIfExist)
      .toHaveBeenCalledWith(userData.parameters.accountId, userData.parameters.password);
    expect(nativeBridgeService.loginSessionToken).toHaveBeenCalledWith(
      jasmine.objectContaining({
        username: userData.parameters.userName,
        sessionToken: userData.parameters.ssoToken,
        isFromBetSlip: userData.parameters.isFromBetslip
      })
    );
    expect(user.getTouchIdLogin).toHaveBeenCalled();
    expect(user.setTouchIdLogin).not.toHaveBeenCalled();
  });

  it('#afterLoginHandler should not call setTouchIdLogin when lastUsername is the same as userName from event', () => {
    const userData = {
      eventName: 'eventName',
      parameters: {
        userName: 'userName',
        password: 'password',
        ssoToken: 'ssoToken',
        accountId: 'accountId',
        isFromBetslip: true
      }
    };
    storage.get = jasmine.createSpy().and.returnValue('');
    user.getTouchIdLogin = jasmine.createSpy().and.returnValue('enabled');
    service['afterLoginHandler'](userData);
    expect(storage.get).toHaveBeenCalledWith('lastUsername');
    expect(storage.set).toHaveBeenCalledWith('lastUsername', userData.parameters.userName);
    expect(nativeBridgeService.loginSalesForce).toHaveBeenCalledWith(`cl_${userData.parameters.userName}`);
    expect(nativeBridgeService.loginIfExist)
      .toHaveBeenCalledWith(userData.parameters.accountId, userData.parameters.password);
    expect(nativeBridgeService.loginSessionToken).toHaveBeenCalledWith(
      jasmine.objectContaining({
        username: userData.parameters.userName,
        sessionToken: userData.parameters.ssoToken,
        isFromBetSlip: userData.parameters.isFromBetslip
      })
    );
    expect(user.getTouchIdLogin).toHaveBeenCalled();
    expect(user.setTouchIdLogin).not.toHaveBeenCalled();
  });

  it('#nativeLogin should call doNativeLogin on NativeBridgeAdapter with proper arguments', () => {
    const cardNumber = '0123456789', pin = '1234', rememberMe = true, rememberMeName = null;
    service['nativeLogin'](cardNumber, pin, rememberMeName, rememberMe);
    expect(nativeBridgeAdapter.doNativeLogin).
    toHaveBeenCalledWith(cardNumber, pin, {isTouchIDEnabled: true, isFaceIDEnabled: false, rememberMe: true});
  });

  it('#nativeLogin should call doNativeLogin on NativeBridgeAdapter with default arguments', () => {
    const cardNumber = '0123456789', pin = '1234';
    service['nativeLogin'](cardNumber, pin);
    expect(nativeBridgeAdapter.doNativeLogin)
      .toHaveBeenCalledWith(cardNumber, pin, {isTouchIDEnabled: true, isFaceIDEnabled: false, rememberMe: false});
  });

  describe('handleVanillaNativeEvents', () => {
    it('OPEN_LOGIN_DIALOG', () => {
      nativeBridgeAdapter.nativeEventObservable = of({ eventName: VANILLA_NATIVE_EVENTS.OPEN_LOGIN_DIALOG });
      windowRef.nativeWindow.openLoginDialog = jasmine.createSpy();
      service['handleVanillaNativeEvents']();

      expect(windowRef.nativeWindow.openLoginDialog).toHaveBeenCalled();
    });

    it('LOGIN_FAILED', () => {
      nativeBridgeAdapter.nativeEventObservable = of({ eventName: VANILLA_NATIVE_EVENTS.LOGIN_FAILED });
      service['afterLoginErrorHandler'] = jasmine.createSpy();
      service['handleVanillaNativeEvents']();

      expect(service['afterLoginErrorHandler']).toHaveBeenCalled();
    });

    it('LOGIN', () => {
      nativeBridgeAdapter.nativeEventObservable = of({
        eventName: VANILLA_NATIVE_EVENTS.LOGIN,
        parameters: {
          userName: 'username'
        }});
      service['afterLoginHandler'] = jasmine.createSpy();
      service['handleVanillaNativeEvents']();

      expect(service['afterLoginHandler']).toHaveBeenCalled();
    });

    it('LOGIN_SCREEN_ACTIVE', () => {
      nativeBridgeAdapter.nativeEventObservable = of({ eventName: VANILLA_NATIVE_EVENTS.LOGIN_SCREEN_ACTIVE });
      service['setDialogStatus'] = jasmine.createSpy();
      service['checkLoginOption'] = jasmine.createSpy();
      service['handleVanillaNativeEvents']();

      expect(service['setDialogStatus']).toHaveBeenCalledWith(true);
      expect(service['checkLoginOption']).toHaveBeenCalled();
    });

    it('LOGIN_SCREEN_ACTIVE, loginWasChecked = true', () => {
      nativeBridgeAdapter.nativeEventObservable = of({ eventName: VANILLA_NATIVE_EVENTS.LOGIN_SCREEN_ACTIVE });
      service['setDialogStatus'] = jasmine.createSpy();
      service['checkLoginOption'] = jasmine.createSpy();
      service['loginWasChecked'] = true;
      service['handleVanillaNativeEvents']();

      expect(service['checkLoginOption']).not.toHaveBeenCalled();
    });

    it('no event', () => {
      nativeBridgeAdapter.nativeEventObservable = of({});
      service['handleVanillaNativeEvents']();

      expect(service['handleVanillaNativeEvents']()).toBe(undefined);
    });

    it('event is undefined', () => {
      nativeBridgeAdapter.nativeEventObservable = of(undefined);
      service['handleVanillaNativeEvents']();

      expect(service['handleVanillaNativeEvents']()).toBe(undefined);
    });
  });

  describe('checkLoginOption', () => {
    it('set loginWasChecked', () => {
      user.status = true;
      service['checkLoginOption']();
      expect(service['loginWasChecked']).toBeTruthy();
    });

    it('first time login', () => {
      storage.getCookie.and.returnValue('');
      service['checkLoginOption']();
      expect(storage.setCookie).toHaveBeenCalledWith('firstTimeLogin', true);
    });

  });


  describe('afterLoginErrorHandler', () => {
    let eventMock;
    beforeEach(() => {
      eventMock = {
        eventName: VANILLA_NATIVE_EVENTS.LOGIN_FAILED,
        parameters: {
          type: 'Autologin',
          errorCode: undefined
        }
      };
    });

    it('LOGIN_FAILED by Autologin', () => {
      service['afterLoginErrorHandler'](eventMock);
      const data = {
        errorCode: undefined,
        errorMessage: 'LOGIN ERROR',
        type: 'Autologin',
        timestamp: jasmine.any(Number)
      };

      expect(nativeBridgeService.appSeeTrackAction).toHaveBeenCalledWith({
        action: 'login-failed', data
      });
      expect(nativeBridgeService.loginError).toHaveBeenCalledWith(data);
      expect(nativeBridgeService.touchIDLoginFailedIfExist).toHaveBeenCalledWith(data);
    });

    it('LOGIN_FAILED', () => {
      eventMock.parameters.type = 'not autologin';
      service['afterLoginErrorHandler'](eventMock);

      expect(nativeBridgeService.touchIDLoginFailedIfExist).not.toHaveBeenCalled();
      expect(nativeBridgeService.loginError).toHaveBeenCalled();
    });

    it('LOGIN_FAILED by Autologin with any errorCode', () => {
      eventMock.parameters.errorCode = 123;
      service['afterLoginErrorHandler'](eventMock);

      expect(nativeBridgeService.touchIDLoginFailedIfExist).not.toHaveBeenCalled();
      expect(nativeBridgeService.loginError).toHaveBeenCalled();
    });
  });

   describe('freebetCounterUpdate',() => {
    it('test conditions for freebetCounterUpdate', () => {
      const freeBets: IFreebetToken[] = [{
        tokenId: '2200000778',
        freebetTokenId: '2200000778',
        freebetOfferId: '28985',
        freebetOfferName: 'CRM-Offer-1',
        freebetOfferDesc: 'LASPRETLASPONONFRBNN',
        freebetTokenDisplayText: '',
        freebetTokenValue: '5.00',
        freebetAmountRedeemed: '0.00',
        freebetTokenRedemptionDate: '2022-03-29 06:47:43',
        freebetRedeemedAgainst: '2022-03-29 06:47:43',
        freebetTokenExpiryDate: '2022-03-29 06:47:43',
        freebetMinPriceNum: '',
        freebetMinPriceDen: '',
        freebetTokenAwardedDate: '2022-03-29 06:47:43',
        freebetTokenStartDate: '2022-03-29 06:47:43',
        freebetTokenType: 'BETBOOST',
        freebetTokenRestrictedSet: {
            level: '',
            id: ''
        },
        freebetGameName: '',
        freebetTokenStatus: '',
        currency: '',
        tokenPossibleBet: {
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        },
        tokenPossibleBets: [{
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        }],
        freebetOfferType: '',
        tokenPossibleBetTags: {
            'tagName': 'FRRIDE'
        }
    }];
    const betToken = [{"tokenId":"36926","freebetTokenId":"41133694","freebetOfferId":"37850","freebetOfferName":"Rakesh Betpack","freebetOfferDesc":"COSPRETCOSPONONFRBNN","freebetTokenDisplayText":"","freebetTokenValue":"1.00","freebetMinStake":"","freebetMaxStake":"","freebetAmountRedeemed":"0.00","freebetTokenExpiryDate":"2023-02-04 22:22:03","freebetTokenAwardedDate":"2022-10-07 10:13:03","freebetTokenStartDate":"2022-09-27 14:44:02","freebetTokenType":"SPORTS","freebetOfferCategories":{"freebetOfferCategory":"Bet Pack"},"tokenPossibleBet":{"name":"Any Sports","betLevel":"ANY_SPORTS","betType":"","betId":"","channels":"","inPlay":"-"},"tokenPossibleBets":[{"name":"Any Sports","betLevel":"ANY_SPORTS","betType":"","betId":"","channels":"","inPlay":"-"}],"freebetOfferType":"","expires":"4 days"}];
      const  mockData = {
        available: true,
        data: freeBets,
        bettoken: betToken
      };
     service.freebetCounterUpdate(mockData);
     expect(freeBetsBadgeLoader.addBadgesToVanillaElements).not.toHaveBeenCalled();
     expect(freeBetsBadgeLoader.addBetpackCounter).not.toHaveBeenCalled();

    });
    it('test conditions for freebetCounterUpdate when FRRIDE token is not there', () => {
      const freeBets: IFreebetToken[] = [{
        tokenId: '2200000778',
        freebetTokenId: '2200000778',
        freebetOfferId: '28985',
        freebetOfferName: 'CRM-Offer-1',
        freebetOfferDesc: 'LASPRETLASPONONFRBNN',
        freebetTokenDisplayText: '',
        freebetTokenValue: '5.00',
        freebetAmountRedeemed: '0.00',
        freebetTokenRedemptionDate: '2022-03-29 06:47:43',
        freebetRedeemedAgainst: '2022-03-29 06:47:43',
        freebetTokenExpiryDate: '2022-03-29 06:47:43',
        freebetMinPriceNum: '',
        freebetMinPriceDen: '',
        freebetTokenAwardedDate: '2022-03-29 06:47:43',
        freebetTokenStartDate: '2022-03-29 06:47:43',
        freebetTokenType: 'BETBOOST',
        freebetTokenRestrictedSet: {
            level: '',
            id: ''
        },
        freebetGameName: '',
        freebetTokenStatus: '',
        currency: '',
        tokenPossibleBet: {
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        },
        tokenPossibleBets: [{
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        }],
        freebetOfferType: '',
    }];
    const betToken = [{"tokenId":"36926","freebetTokenId":"41133694","freebetOfferId":"37850","freebetOfferName":"Rakesh Betpack","freebetOfferDesc":"COSPRETCOSPONONFRBNN","freebetTokenDisplayText":"","freebetTokenValue":"1.00","freebetMinStake":"","freebetMaxStake":"","freebetAmountRedeemed":"0.00","freebetTokenExpiryDate":"2023-02-04 22:22:03","freebetTokenAwardedDate":"2022-10-07 10:13:03","freebetTokenStartDate":"2022-09-27 14:44:02","freebetTokenType":"SPORTS","freebetOfferCategories":{"freebetOfferCategory":"Bet Pack"},"tokenPossibleBet":{"name":"Any Sports","betLevel":"ANY_SPORTS","betType":"","betId":"","channels":"","inPlay":"-"},"tokenPossibleBets":[{"name":"Any Sports","betLevel":"ANY_SPORTS","betType":"","betId":"","channels":"","inPlay":"-"}],"freebetOfferType":"","expires":"4 days"}];

      const  mockData = {
        available: true,
        data: freeBets,
        bettoken: betToken    
      };
     service.freebetCounterUpdate(mockData);
     expect(freeBetsBadgeLoader.addBadgesToVanillaElements).not.toHaveBeenCalled();
     expect(freeBetsBadgeLoader.addBetpackCounter).not.toHaveBeenCalled();

    });
  });

  it('#login should call correct methods for all', () => {
    service['loginFlow'] = jasmine.createSpy();
    user.getPostLoginBonusSupValue = jasmine.createSpy('getPostLoginBonusSupValue').and.returnValue(false);
    service['login']();
    expect(service['loginFlow']).toHaveBeenCalled();
  });
  it('#login should call correct methods for Ladbrokes', () => {
    service['loginFlow'] = jasmine.createSpy();
    user.getPostLoginBonusSupValue = jasmine.createSpy('getPostLoginBonusSupValue').and.returnValue(true);
    service['login']();
    expect(service['loginFlow']).toHaveBeenCalled();
  });

});
