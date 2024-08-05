import { SbQuickbetSelectionComponent } from './sb-quickbet-selection.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { Subject } from 'rxjs';
import { LadbrokesQuickbetSelectionComponent as QuickbetSelectionComponent } from '@ladbrokesMobile/quickbet/components/quickbetSelection/quickbet-selection.component';

describe('SbQuickbetSelectionComponent', () => {
  let component: SbQuickbetSelectionComponent;
  let pubsub;
  let user;
  let locale;
  let filtersService;
  let quickbetDepositService;
  let QuickbetService;
  let quickbetUpdateService;
  let freeBetsFactory;
  let quickbetNotificationService;
  let commandService;
  let cmsService;
  let gtmService;
  let cdr;
  let windowRef;
  let timeService;
  let bppProviderService;
  let fiveASideContestSelectionService;
  let serviceClosureService;
  let sessionStorageService;
  let storageService;
  let currencyPipe;
  let bonusSuppressionService;
  let loginCb;

  beforeEach(() => {
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
            callback('frac');
          } else {
            callback();
          }
      }),
      unsubscribe: jasmine.createSpy()
    };
    locale = {
        getString: jasmine.createSpy().and.returnValue(''),
    };
    currencyPipe = {
      transform: jasmine.createSpy().and.returnValue('$25')
    };
    QuickbetService = {
      quickBetOnOverlayCloseSubj: new Subject<string>(),
    };
    quickbetNotificationService = {
      snbMaxPayoutMsgSub: new Subject<string>(),
    };
    user = {
      currencySymbol: '$'
    };

    component = new SbQuickbetSelectionComponent(

        pubsub,
        user,
        locale,
        filtersService,
        quickbetDepositService,
        QuickbetService,
        quickbetUpdateService,
        freeBetsFactory,
        quickbetNotificationService,
        commandService,
        cmsService,
        gtmService,
        cdr,
        windowRef,
        timeService,
        bppProviderService,
        fiveASideContestSelectionService,
        serviceClosureService,
        sessionStorageService,
        storageService,
        currencyPipe,
        bonusSuppressionService
   
    );
  });

  describe('#SbQuickbetSelectionComponent', () => {
    it('ngOnInit is called and quickBetOnOverlayCloseSubj is triggered', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      const closeFnHandlerSpy = spyOn(component, 'closeFnHandler');
      component.selection = {stake: '1.00'} as any;
      component.ngOnInit();
      QuickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      expect(closeFnHandlerSpy).toHaveBeenCalled();
    });

    it('ngOnInit is called and stake is 1.0 and value is 0', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '1.0'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('0')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('1.00');
    });

    it('ngOnInit is called and stake is undefined and value is "."', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('.')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('0.');
    });

    it('ngOnInit is called and stake is undefined and value is qb-5', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('qb-5')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('5');
    });

    it('ngOnInit is called and stake is undefined and value is 3', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('3')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('3');
    });

    it('ngOnInit is called and stake is "" and value is "delete"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: ''} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('delete')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('');
    });

    it('ngOnInit is called and stake is "1.23" and value is "delete"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '1.23'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('delete')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('1.2');
    });

    it('ngOnInit is called and stake is "1.23" and value is "qb-5"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '1.23'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('qb-5')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('6.23');
    });

    it('ngOnInit is called and stake is "0" and value is "2"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '0'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('2')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('2');
    });

    it('ngOnInit is called and stake is "0" and value is "2"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '0'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('2')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('2');
    });

    it('ngOnInit is called and stake is "12345" and value is "2"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '12345'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('2')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('12345');
    });

    it('ngOnInit is called and stake is "1" and value is "2"', () => {
      spyOn(QuickbetSelectionComponent.prototype, 'ngOnInit');
      component.selection = {stake: '1'} as any;
      const onStakeChangeSpy = spyOn(component, 'onStakeChange');
      pubsub.subscribe.and.callFake((file, method, callback) => {
        if(method === 'DIGIT_KEYBOARD_KEY_PRESSED') {
          callback('2')
        }
      })
      component.ngOnInit();
      expect(component.selection.stake).toBe('12');
    });

    it('onStakeElemClick is called and showKeyboard is false', () => {
      component.showKeyboard = false;
      component.onStakeElemClick();
      expect(component.showKeyboard).toBe(true);
    });

    it('placeBetFnHandler is called', () => {
      QuickbetSelectionComponent.prototype.placeBetFnHandler = jasmine.createSpy('super.placeBetFnHandler');
      component.placeBetFnHandler();
      expect(component.showKeyboard).toBe(false);
    });

    it('showFreeBet is called and freebetsList data available', () => {
      component.freebetsList = [
        {
          name: 'Weekly freebet 9.99$',
          freebetTokenValue: '9.99$',
          freebetTokenId: 123,
          id:123
        }
      ] as any[];

      expect(component.showFreeBet()).toBe(true);
    });

    it('showFreeBet is called and betPackList data available', () => {
      component.betPackList = [
        {
          name: 'Weekly freebet 9.99$',
          freebetTokenValue: '9.99$',
          value : '9.99$',
          freebetTokenId: 1235
  
        }
      ] as any[];

      expect(component.showFreeBet()).toBe(true);
    });
    
    it('addItem is called, prevMaxPayout as false and newItem as true', () => {
      component.maxPayMsg = 'Payout limit exceeded';
      component.selection = {maxPayout: '50000'} as any;
      component.addItem(true);
      expect(component.prevMaxPayout).toBe(true);
    });

    it('addItem is called, prevMaxPayout as true and newItem as false', () => {
      component.maxPayMsg = 'Payout limit exceeded';
      component.prevMaxPayout = true;
      component.selection = {maxPayout: '50000'} as any;
      component.addItem(false);
      expect(component.prevMaxPayout).toBe(false);
    });

  });
});
