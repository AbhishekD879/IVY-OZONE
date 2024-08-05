import { forkJoin as observableForkJoin, of, Subscription } from 'rxjs';

import { BetTrackerComponent } from './bet-tracker.component';
import environment from '@environment/oxygenEnvConfig';
import { BET_TRACKER } from '@app/retail/constants/retail.constant';

describe('BetTrackerComponent', () => {
  let component: BetTrackerComponent;
  let asyncLoad;
  let windowRef;
  let upgradeAccountProviderService;
  let userService;
  let pubSubService;
  let changeDetectorRef;
  let recService;

  beforeEach(() => {
    asyncLoad = {
      loadJsFile: jasmine.createSpy().and.returnValue(of({})),
      loadCssFile: jasmine.createSpy().and.returnValue(of({}))
    };
    windowRef = {
      document: { dispatchEvent: jasmine.createSpy('dispatchEvent') },
      nativeWindow: {
        clientConfig: {
          vnChat: {
            chatBotAccessId: 'abcd'
          },
          vnReCaptcha: {
            enterpriseSiteKey: 'abc-Wu',
            instrumentationOnPageLoad: true
          }
        }
      }
    };
    upgradeAccountProviderService = {
      getCardRequest: jasmine.createSpy().and.returnValue(of({body: {data: { printedTokenCode: '12345678' } } }))
    };
    userService = {
      isRetailUser: () => true,
      cardNumber: '',
      username: 'userName',
      sessionToken: 'customerSessionId',
      set: jasmine.createSpy(),
      status: true
    };
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN'
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    recService = {
      addScript : jasmine.createSpy('addScript'),
    };
  });

  beforeEach(() => {
    component = new BetTrackerComponent(
      asyncLoad,
      windowRef,
      upgradeAccountProviderService,
      userService,
      pubSubService,
      changeDetectorRef,
      recService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component['initBetTracker'] = jasmine.createSpy('initBetTracker');
    });

    it('should call initBetTracker', () => {
      component.ngOnInit();

      expect(component['initBetTracker']).toHaveBeenCalled();
    });

    it('should subscribe to betTrackerComponent SUCCESSFUL_LOGIN', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => cb());

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'betTrackerComponent',
        pubSubService.API.SUCCESSFUL_LOGIN,
        jasmine.any(Function));
      expect(component['initBetTracker']).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from betTrackerComponent', () => {
      component['upgradeAccountSubscribe'] = new Subscription();
      component['bootstrapBetSubscribe'] = new Subscription();
      component['upgradeAccountSubscribe'].unsubscribe = jasmine.createSpy('unsubscribe');
      component['bootstrapBetSubscribe'].unsubscribe = jasmine.createSpy('unsubscribe');
      component.mode = 'BET_TRACKER';
      component.ngOnDestroy();

      expect(component['pubSubService'].unsubscribe).toHaveBeenCalled();
      expect(component['upgradeAccountSubscribe'].unsubscribe).toHaveBeenCalled();
      expect(component['bootstrapBetSubscribe'].unsubscribe).toHaveBeenCalled();
      expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalled();
    });

    it('should dispatch event if mode is BET_HISTORY', () => {
      component['upgradeAccountSubscribe'] = new Subscription();
      component['bootstrapBetSubscribe'] = new Subscription();
      component['upgradeAccountSubscribe'].unsubscribe = jasmine.createSpy('unsubscribe');
      component['bootstrapBetSubscribe'].unsubscribe = jasmine.createSpy('unsubscribe');
      component.mode = 'BET_HISTORY';
      component.ngOnDestroy();

      expect(component['pubSubService'].unsubscribe).toHaveBeenCalled();
      expect(component['upgradeAccountSubscribe'].unsubscribe).toHaveBeenCalled();
      expect(component['bootstrapBetSubscribe'].unsubscribe).toHaveBeenCalled();
      expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalled();
    });

    it('if subscription is not defined', () => {
      component['upgradeAccountSubscribe'] = null;
      component['bootstrapBetSubscribe'] = null;
      expect(() => {
        component.ngOnDestroy();
      }).not.toThrow();
    });
  });

  describe('userStatus', () => {
    it('should return user status', () => {
      const result = component.userStatus;

      expect(result).toBeTruthy();
    });
  });

  describe('#initBetTracker', () => {
    beforeEach(() => {
      component['bootstrapBetTracker'] = jasmine.createSpy();
    });

    it('should do call to APPOLO Service and run bootstrapBetTracker and set cardNumber and if user is MultiChannel and NOT have ' +
      'cardNumber', () => {
      component['initBetTracker']();

      expect(component['upgradeAccountProviderService'].getCardRequest).toHaveBeenCalledWith(
        {'username': 'userName', 'customerSessionId': 'customerSessionId'}
      );
      expect(component['userService'].set).toHaveBeenCalledWith({ cardNumber: '12345678'});
      expect(component['bootstrapBetTracker']).toHaveBeenCalledTimes(1);
    });

    it('should do call to APPOLO Service and run bootstrapBetTracker and if user is MultiChannel and NOT have cardNumber', () => {
      upgradeAccountProviderService.getCardRequest.and.returnValue(of({body: {data: { printedTokenCode: undefined } } }));

      component['initBetTracker']();

      expect(component['upgradeAccountProviderService'].getCardRequest).toHaveBeenCalledWith(
        {'username': 'userName', 'customerSessionId': 'customerSessionId'}
      );
      expect(component['userService'].set).not.toHaveBeenCalledWith({ cardNumber: '12345678'});
      expect(component['bootstrapBetTracker']).toHaveBeenCalledTimes(1);
    });

    it('should run bootstrapBetTracker if user is MultiChannel and have cardNumber', () => {
      // @ts-ignore
      component['userService'] = { isRetailUser: () => true, cardNumber: '123' };
      component['initBetTracker']();

      expect(component['bootstrapBetTracker']).toHaveBeenCalledTimes(1);
    });

    it('should run bootstrapBetTracker if user is NOT MultiChannel and have cardNumber', () => {
      // @ts-ignore
      component['userService'] = { isRetailUser: () => false, cardNumber: '123' };
      component['initBetTracker']();

      expect(component['bootstrapBetTracker']).toHaveBeenCalledTimes(1);
    });

  });

  describe('bootstrapBetTracker', () => {
    it('should return user status', () => {
      const result = component.userStatus;

      expect(result).toBeTruthy();
    });
  });

  describe('bootstrapBetTracker', () => {
    it('should return user status', () => {
      component['bootstrapBetTracker']();

      observableForkJoin([
        component['asyncLoad'].loadJsFile(''),
        component['asyncLoad'].loadCssFile('')
      ]).subscribe(null, null, () => {
        expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalled();
      });
    });
    it('should call addScript method ',()=>{
      component['bootstrapBetTracker']();
      expect(recService.addScript).toHaveBeenCalled();
    });
    it('should add recapcha token from client config and return user status', () => {
      const RECAPTCHA_SITE_KEY = component['windowRef'].nativeWindow.clientConfig.vnReCaptcha.enterpriseSiteKey;
      component['bootstrapBetTracker']();
      const mockParams = new CustomEvent(BET_TRACKER.BOOTSTRAP_BET_TRACKER,
        { detail: Object.assign({}, { accessId: RECAPTCHA_SITE_KEY })});
      observableForkJoin([
        component['asyncLoad'].loadJsFile(''),
        component['asyncLoad'].loadCssFile('')
      ]).subscribe(null, null, () => {
        expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalledWith(mockParams);
      });
    });

    it('should add recapcha token from BMA config and return user status', () => {
      component['windowRef'].nativeWindow.clientConfig.vnReCaptcha = undefined;
      const mockParams = new CustomEvent(BET_TRACKER.BOOTSTRAP_BET_TRACKER,
        { detail: Object.assign({}, { accessId: environment.GOOGLE_RECAPTCHA.ACCESS_TOKEN })});
      component['bootstrapBetTracker']();

      observableForkJoin([
        component['asyncLoad'].loadJsFile(''),
        component['asyncLoad'].loadCssFile('')
      ]).subscribe(null, null, () => {
        expect(component['windowRef'].document.dispatchEvent).toHaveBeenCalledWith(mockParams);
      });
    });
  });
});
