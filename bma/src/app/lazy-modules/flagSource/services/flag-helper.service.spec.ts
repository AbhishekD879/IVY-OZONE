import { BehaviorSubject } from 'rxjs';
import { FlagHelperService } from './flag-helper.service';
describe('FlagHelperService', () => {
  let service: FlagHelperService;
  let windowRefService;
  let storageService;
  let pubsub;
  let userService;
  let flagSourceService;
  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        ldkeys: '123',
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        })
      }
    };
    userService = {
        logout: jasmine.createSpy(),
        login: jasmine.createSpy(),
        set: jasmine.createSpy(),
        initProxyAuth: jasmine.createSpy(),
        resolveProxyAuth: jasmine.createSpy(),
        rejectProxyAuth: jasmine.createSpy(),
        isInShopUser: jasmine.createSpy().and.returnValue(false),
        proxyPromiseResolved: jasmine.createSpy().and.returnValue(true),
        username: 'username',
        bppToken: 'Aoz_dshfdfefnfE20--e'
    };
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      getCookie: jasmine.createSpy('getCookie').and.returnValue(1)
    };
    pubsub = {
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SUCCESSFUL_LOGOUT: 'SUCCESSFUL_LOGOUT'
      },
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
    };

    flagSourceService = {
        flagStore: '',
        flagUpdate: new BehaviorSubject<any>({}),
        onAppInit: jasmine.createSpy('onAppInit'),
        getServerFlags: jasmine.createSpy('getServerFlags'),
        updateFlagstore: jasmine.createSpy('updateFlagstore').and.returnValue(1)
      };
  });
  describe('FlagHelperService', () => {
    beforeEach(() => {
      service = new FlagHelperService(windowRefService, pubsub, userService, storageService,flagSourceService);
      service.client = {
        variation: jasmine.createSpy(),
        waitUntilReady: jasmine.createSpy().and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy().and.returnValue({}),
        on:jasmine.createSpy(),
        identify:  jasmine.createSpy(),
     } as any;
    });

    it('constructor', () => {
      expect(service).toBeTruthy();
    });

    it('getContext  with login', () => {
      userService.status = true;
      userService.custId = '567';
      service.getUserGAId = jasmine.createSpy().and.returnValue(Promise.resolve('123'));
      service.getContext();
      expect(userService.status).toEqual(true);
    });

    it('getContext with logout', () => {
      userService = {
        status: false,
        custId: '567'
      };
      service.getUserGAId = jasmine.createSpy().and.returnValue(Promise.resolve('123'));
      service.getContext();
      expect(userService.status).toEqual(false);
    });

    it('getCookie', () => {
      document.cookie = 'cookie'
      service.getCookie('LD');
      expect(service.getCookie('LD')).toEqual('');
    });

    it('getCookie', () => {
      document.cookie = 'LD_GA=false; lang=en';
      service.getCookie('LD_GA');
      expect(service.getCookie('LD_GA')).toEqual('false');
    });

    it('identifyContext', () => {
      service.client = {} as any;
      service.getContext = jasmine.createSpy().and.returnValue(Promise.resolve('123'));
      service.client = {
        identify: jasmine.createSpy('identify').and.callFake((a, b, cb) => cb && cb()),
      } as any;
      userService = {
        status: false,
        custId: '567'
      };
      service.identifyContext();
      expect(service.getContext).toHaveBeenCalled();
    });

    it('getLDFlagsFromServer', () => {
      spyOn(service, 'publishAllFlags');
      const spyon = spyOn(service, 'getClientFlags');
      service.initializeLD = jasmine.createSpy().and.returnValue(Promise.resolve({
        variation: jasmine.createSpy(),
        waitUntilReady: jasmine.createSpy().and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy().and.returnValue({'ShowQuickLinks':'true'}),
        on:jasmine.createSpy(),
        identify:  jasmine.createSpy(),
      }));
      const mockData = '{singlequotetest_flatest_flaggsinglequote:singlequotefalsesinglequote,singlequoteshow-betslip-revamp-barsinglequote:singlequote&quot;betslip-revamp-bar-with-counter&quot;singlequote,singlequotetest_flagsinglequote:singlequotetruesinglequote,singlequoteShowQuickLinkssinglequote:singlequotetruesinglequote,singlequotebsRevampsinglequote:singlequote&quot;accabar&quot;singlequote,singlequoteshow-betslip-countersinglequote:singlequotetruesinglequote,singlequoteshow-betslip-accabarsinglequote:singlequote&quot;betslip&quot;singlequote}';
      service.getLDFlagsFromServer(mockData);
      expect(spyon).not.toHaveBeenCalled();
    });

    it('publishAllFlags', () => {
      service.publishAllFlags('showQuickLinks');
      expect(flagSourceService.updateFlagstore).toHaveBeenCalled();
    });

    it('publishFlag', () => {
      service.client = {
        variation: jasmine.createSpy(),
        waitUntilReady: jasmine.createSpy().and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy(),
        on:jasmine.createSpy(),
        identify:  jasmine.createSpy(),
     } as any;
      service.client.variation = jasmine.createSpy('variation').and.returnValue('123');
      service.publishFlag('showQuickLinks', true);
      expect(flagSourceService.updateFlagstore).toHaveBeenCalled();
    }); 

    it('getClientFlags', () => {
      spyOn(service, 'publishFlag');
      service.client =  {
        variation: jasmine.createSpy(),
        waitUntilReady: jasmine.createSpy().and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy().and.returnValue({'ShowQuickLinks':'true'}),
        on:jasmine.createSpy(),
        identify:  jasmine.createSpy(),
     } as any;
      service.getClientFlags();
      expect(service.publishFlag).not.toHaveBeenCalled();
    });

    it('getClientFlags with fallbackflags', () => {
      spyOn(service, 'publishFlag');
      service.client =  {
        variation: jasmine.createSpy(),
        waitUntilReady: jasmine.createSpy().and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy().and.returnValue({}),
        on:jasmine.createSpy(),
        identify:  jasmine.createSpy(),
     } as any;
      service.getClientFlags();
      expect(service.publishFlag).not.toHaveBeenCalled();
    });

    it('initialiseFlagsOfServer', () => {
      spyOn(service, 'getLDFlagsFromServer');
      flagSourceService.flagStore = '{singlequotetest_flatest_flaggsinglequote:singlequotefalsesinglequote,singlequoteshow-betslip-revamp-barsinglequote:singlequote&quot;betslip-revamp-bar-with-counter&quot;singlequote,singlequotetest_flagsinglequote:singlequotetruesinglequote,singlequoteShowQuickLinkssinglequote:singlequotetruesinglequote,singlequotebsRevampsinglequote:singlequote&quot;accabar&quot;singlequote,singlequoteshow-betslip-countersinglequote:singlequotetruesinglequote,singlequoteshow-betslip-accabarsinglequote:singlequote&quot;betslip&quot;singlequote}';
      service.initialiseFlagsOfServer();
      expect(service.getLDFlagsFromServer).toHaveBeenCalled();
    });
    
    it('getClientFlags with publishflag when key is wrong', () => {
      spyOn(service, 'publishFlag');
      service.client = {
        waitUntilReady: jasmine.createSpy('waitUntilReady').and.returnValue(Promise.resolve({})),
        allFlags: jasmine.createSpy('allFlags').and.returnValue({}),
        on: jasmine.createSpy('on').and.callFake((p1, cb) => {
          cb({}, true);
          expect(service.publishFlag).toHaveBeenCalled();
        }),
        identify:  jasmine.createSpy(),
        variation: jasmine.createSpy(),
      } as any;
      service.client.waitUntilReady =  jasmine.createSpy('waitUntilReady').and.returnValue(Promise.resolve({}));
      service.getClientFlags();
      expect(service.client.waitUntilReady).toHaveBeenCalled();
    });

    it('getLDOptions', () => {
      service.getLDOptions();
      expect(service.getLDOptions()).toBeTruthy();
    });

    it('getUserGAId', () => {
      spyOn(service, 'getCookie').and.returnValue('1');
      service.getUserGAId().then((val) => {
        expect(val).toBe('1');
      }
      );
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });

    it('getUserGAId', () => {
      spyOn(service, 'getCookie').and.returnValue('');
      service.getUserGAId().then((val) => {
        expect(val).toBe('1');
      }
      );
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });

    it('getUserGAId', () => {
      storageService.getCookie = jasmine.createSpy('getCookie').and.returnValue(undefined)
      storageService.setCookie = jasmine.createSpy('setCookie');
      spyOn(service, 'getCookie').and.returnValue('');
      service.getUserGAId().then((val) => {
        expect(service.getLDOptions()).toBeTruthy();
      }
      );
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
    });

   it('initializeLD', () => {
      spyOn(service, 'getLDOptions');
      service.getContext = jasmine.createSpy().and.returnValue(Promise.resolve('123'));
      service.initializeLD();
      expect(service.getContext).toHaveBeenCalled();
    });
  });
})