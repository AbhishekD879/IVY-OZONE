import { pubSubApi } from '../communication/pubsub/pubsub-api.constant';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';

describe('UserService', () => {
  let service: UserService;

  let storage;
  let pubsub;
  let localeService;
  let windowRef;
  let sessionStorage;

  beforeEach(() => {
    storage = {
      setCookie: jasmine.createSpy(),
      get: jasmine.createSpy(),
      set: jasmine.createSpy(),
      remove: jasmine.createSpy(),
      removeCookie: jasmine.createSpy(),
      getCookie: jasmine.createSpy()
    };

    windowRef = {
      nativeWindow: {
        NativeBridge: undefined
      }
    };
    pubsub = {
      publish: jasmine.createSpy(),
      API: pubSubApi
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('foo')
    };

    sessionStorage = {
      get: jasmine.createSpy(),
      set: jasmine.createSpy()
    }

    service = new UserService(storage, pubsub, localeService, windowRef);
  });

  it('constructor', () => {
    expect(storage.getCookie).toHaveBeenCalledTimes(2);
    expect(storage.set).toHaveBeenCalledTimes(1);
    expect(storage.get).toHaveBeenCalledTimes(1);
    expect(storage.get).toHaveBeenCalledWith('USER');

    expect(service['openApiAuthPromise']).toBeDefined();
    expect(service['proxyAuthPromise']).toBeDefined();
  });

  it('getOpenApiAuth', () => {
    expect(service.getOpenApiAuth()).toEqual(service['openApiAuthPromise']);
  });

  describe('getProxyAuth', () => {
    it('should make api call to auth for digital user', () => {
      service.data = {
        accountBusinessPhase: 'multi-channel'
      };
      expect(service.getProxyAuth()).toEqual(service['proxyAuthPromise']);
    });

    it('should\'t make api call to auth for in shop user', () => {
      service.data = {
        accountBusinessPhase: 'in-shop'
      };
      expect(service.getProxyAuth()).not.toEqual(service['proxyAuthPromise']);
    });
  });

  it('setExternalCookies: false', () => {
    service.setExternalCookies();
    expect(storage.removeCookie).toHaveBeenCalledWith('X_MB_NATIVE');
    expect(storage.removeCookie).toHaveBeenCalledTimes(4);
  });

  it('setExternalCookies: true', () => {
    service.data.status = true;
    service.setExternalCookies();
    expect(storage.setCookie).toHaveBeenCalledTimes(3);
  });

  it('setExternalCookies: X_MB_NATIVE cookie for wrapper apps', () => {
    environment.DOMAIN = 'test';
    windowRef.nativeWindow.NativeBridge = true;
    service.setExternalCookies();
    expect(storage.setCookie).toHaveBeenCalledWith('X_MB_NATIVE', 'true', environment.DOMAIN, 365, true);
  });

  it('isRestoredBppUser', () => {
    service.data.bppToken = 'askj381w';
    service.data.username = 'oxygenUser';
    storage.get = jasmine.createSpy().and.returnValue('oxygenUser');

    expect(service.isRestoredBppUser()).toBeTruthy();
  });

  it('setTouchIdLogin', () => {
    service.setTouchIdLogin('oxygenUser');
    expect(storage.setCookie).toHaveBeenCalledTimes(1);
    expect(storage.setCookie).toHaveBeenCalledWith('touchIdLogin', 'oxygenUser');
  });

  describe('getTouchIdLogin', () => {
    it('touchIdLogin false', () => {
      expect(service.getTouchIdLogin()).toEqual('disabled');
    });

    it('touchIdLogin present', () => {
      storage.getCookie = jasmine.createSpy().and.returnValue('oxygenUser');
      expect(service.getTouchIdLogin()).toEqual('oxygenUser');
      expect(storage.getCookie).toHaveBeenCalledTimes(1);
      expect(storage.getCookie).toHaveBeenCalledWith('touchIdLogin');
    });
  });

  describe('getLoggedInUser', () => {
    it('getLoggedInUser false', () => {
      expect(service.getLoggedInUser()).toEqual(undefined);
    });

    it('getLoggedInUser present', () => {
      storage.getCookie = jasmine.createSpy().and.returnValue('sportsbookUsername');
      expect(service.getLoggedInUser()).toEqual('sportsbookUsername');
      expect(storage.getCookie).toHaveBeenCalledTimes(1);
      expect(storage.getCookie).toHaveBeenCalledWith('sportsbookUsername');
    });
  });

  describe('getPostLoginBonusSupValue', () => {
    it('user login false', () => {
      expect(service.getPostLoginBonusSupValue()).toEqual(false);
    });

    it('user logged in', () => {
      storage.getCookie = jasmine.createSpy('mobileLogin.PostLoginValues').and.returnValue({bonusSuppression: true});
      expect(service.getPostLoginBonusSupValue()).toEqual(true);
      expect(storage.getCookie).toHaveBeenCalledTimes(1);
      expect(storage.getCookie).toHaveBeenCalledWith('mobileLogin.PostLoginValues');
    });
  });

  it('login', () => {
    service.login('qi23j1');
    service.data.status = true;
    service.setExternalCookies();
    expect(storage.setCookie).toHaveBeenCalledTimes(6);

    expect(storage.set).toHaveBeenCalledTimes(4);
    expect(storage.set).toHaveBeenCalledWith('USER', jasmine.anything());
  });

  it('logout', () => {
    service.logout();

    expect(storage.remove).toHaveBeenCalledTimes(7);
    expect(storage.removeCookie).toHaveBeenCalledTimes(5);
    expect(storage.removeCookie).toHaveBeenCalledWith('X_MB_NATIVE');

    expect(pubsub.publish).toHaveBeenCalledTimes(1);
    expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SESSION_LOGOUT);
  });
  it('logout without remove username cookie', () => {
    service.removeUsernameCookie = false;
    service.logout();

    expect(storage.remove).toHaveBeenCalledTimes(7);
    expect(storage.removeCookie).toHaveBeenCalledTimes(4);
    expect(storage.removeCookie).toHaveBeenCalledWith('X_MB_NATIVE');

    expect(pubsub.publish).toHaveBeenCalledTimes(1);
    expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SESSION_LOGOUT);
  });
  it('should check and clean storage data', () => {
    spyOn(service, 'isRouletteJourney').and.returnValue(true);
    service.breakRouletteJourney();

    expect(service.isRouletteJourney).toHaveBeenCalled();
    expect(pubsub.publish).toHaveBeenCalledWith('ROULETTE_JOURNEY_END');
    expect(storage.remove).toHaveBeenCalledWith('rouletteJourney');
  });

  it('should not clean storage data if not journey', () => {
    spyOn(service, 'isRouletteJourney').and.returnValue(false);
    service.breakRouletteJourney();

    expect(service.isRouletteJourney).toHaveBeenCalled();
    expect(storage.remove).not.toHaveBeenCalled();
  });


  describe('canActivateJourney', () => {
    it('should return true', () => {
      const params = {
        targetPage: 'targetPage',
        referrerPage: 'referrerPage'
      };
      service.data.status = false;
      expect(service.canActivateJourney(params as any)).toEqual(true);
    });

    it('should return false if no params', () => {
      const params = {};
      service.data.status = false;
      expect(service.canActivateJourney(params as any)).toEqual(false);
    });

    it('should return false if no targetPage', () => {
      const params = {
        referrerPage: 'referrerPage'
      };
      service.data.status = false;
      expect(service.canActivateJourney(params as any)).toEqual(false);
    });

    it('should return false if no referrerPage', () => {
      const params = {
        targetPage: 'targetPage',
      };
      service.data.status = false;
      expect(service.canActivateJourney(params as any)).toEqual(false);
    });

    it('should return false if user logined', () => {
      const params = {
        targetPage: 'targetPage',
        referrerPage: 'referrerPage'
      };
      service.data.status = true;
      expect(service.canActivateJourney(params as any)).toEqual(false);
    });
  });

  describe('getJourneyParams', () => {
    it('should return object with url params', () => {
      const url = 'https://sports.coral.co.uk/?targetPage=signup&referrerPage=referrerPageUrl';
      const result = service.getJourneyParams(url);

      expect(result).toEqual({
        targetPage: 'signup',
        referrerPage: 'referrerPageUrl'
      });
    });

    it('should return object with null params', () => {
      const url = 'https://sports.coral.co.uk/';
      const result = service.getJourneyParams(url);

      expect(result).toEqual({
        targetPage: null,
        referrerPage: null
      });
    });
  });

  describe('user deposit', () => {
    it('should return a value of 5', () => {
      service.data.sportBalance = 0;
      expect(service.getUserDepositNeededAmount(4, true)).toEqual('5.00');
    });

    it('should return a value of 10', () => {
      service.data.sportBalance = 0;
      expect(service.getUserDepositNeededAmount(10, true)).toEqual('10.00');
    });

    it('should return a value of 5', () => {
      service.data.sportBalance = 10;
      expect(service.getUserDepositNeededAmount(15, false)).toEqual('5.00');
    });

    it('should return a value of 5', () => {
      service.data.sportBalance = 0;
      expect(service.getUserDepositNeededAmount(0, false)).toEqual('5.00');
    });

    it('should return a value of 6(if isBetslip = true it means that' +
      'amount field is already calculated and equal to neededAmountForPlaceBet)', () => {
      service.data.sportBalance = 5;
      expect(service.getUserDepositNeededAmount(6, true)).toEqual('6.00');
    });
  });

  describe('user deposit message', () => {
    it('should return string', () => {
      service.data.sportBalance = 10;
      service.data.currencySymbol = '$';

      expect(service.getUserDepositMessage(15, false)).toEqual('foo');
      expect(localeService.getString).toHaveBeenCalledWith('bs.betslipDepositNotification', ['$5.00']);
    });

    it('should return string if from betslip', () => {
      service.data.sportBalance = 10;
      service.data.currencySymbol = '$';

      expect(service.getUserDepositMessage(15, true)).toEqual('foo');
      expect(localeService.getString).toHaveBeenCalledWith('bs.betslipDepositNotification', ['$15.00']);
    });
  });
  it('resolveOpenApiAuth', () => {
    service.resolveOpenApiAuth();
    expect(service['openApiAuthIsPending']).toBeFalsy();
  });
  it('resolveProxyAuth', () => {
    service.resolveProxyAuth();
    expect(service['proxyAuthPromiseIsPending']).toBeFalsy();
  });
  it('rejectOpenApiAuth', () => {
    service.rejectOpenApiAuth();
    expect(service['openApiAuthIsPending']).toBeFalsy();
  });
  it('rejectProxyAuth', () => {
    service.rejectProxyAuth();
    expect(service['proxyAuthPromiseIsPending']).toBeFalsy();
  });
  describe('initProxyAuth', () => {
    it('promise already created', () => {
      service['proxyAuthPromiseIsPending'] = true;
      service.initProxyAuth();
      expect(service['openApiAuthIsPending']).toBeTruthy();
    });
    it('promise not created', () => {
      service['proxyAuthPromiseIsPending'] = false;
      service.initProxyAuth();
      expect(service['openApiAuthIsPending']).toBeTruthy();
    });
  });
  describe('initAuthPromises', () => {
    it('promises created', () => {
      service['openApiAuthIsPending'] = true;
      service['proxyAuthPromiseIsPending'] = true;
      service.initAuthPromises();
      expect(service['openApiAuthIsPending']).toBeTruthy();
      expect(service['proxyAuthPromiseIsPending']).toBeTruthy();
    });
    it('promises not created', () => {
      service['openApiAuthIsPending'] = false;
      service['proxyAuthPromiseIsPending'] = false;
      service.initAuthPromises();
      expect(service['openApiAuthIsPending']).toBeTruthy();
      expect(service['proxyAuthPromiseIsPending']).toBeTruthy();
    });
  });
  describe('proxyPromiseResolved', () => {
    it('should return false', () => {
      service['proxyAuthPromiseIsPending'] = true;
      const res = service['proxyPromiseResolved']();
      expect(res).toBeFalsy();
    });
    it('should return true', () => {
      service['proxyAuthPromiseIsPending'] = false;
      const res = service['proxyPromiseResolved']();
      expect(res).toBeTruthy();
    });
  });

  it('should remove native X_MB_NATIVE cookie', () => {
    service.removeNativeCookie();

    expect(storage.removeCookie).toHaveBeenCalledWith('X_MB_NATIVE');
  });  

  it('should call toteBetReset', () => {
    storage.get.and.returnValue({poolBet: {freebetTokenId: 1, freebetTokenValue: 1}});
    service.toteBetReset();
    expect(service).toBeTruthy();
  });  
});
