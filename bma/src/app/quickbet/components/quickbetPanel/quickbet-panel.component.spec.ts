import { of as observableOf, Subject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';
import { ISuspendedOutcomeError } from '@betslip/models/suspended-outcome-error.model';

describe('QuickbetPanelComponent', () => {
  let component: QuickbetPanelComponent,
    mockSelection, loginAndPlaceBets, placeBet;
  let rendererService,
    pubsub,
    userService,
    locale,
    quickbetDepositService,
    device,
    infoDialog,
    quickbetService,
    quickbetDataProviderService,
    quickbetNotificationService,
    cmsService,
    windowRefService,
    domToolsService,
    router,
    quickbetUpdateService,
    jsEventMock,
    changeDetectorRef,
    arcUserService,
    serviceClosureService,
    yourCallMarketService,
    dialogService,
    nativeBridgeService,
    sessionStorageService, user,quickDepositIframeService;

  const fakeSuspension: ISuspendedOutcomeError = { multipleWithDisableSingle: false, disableBet: true, msg: 'msg' };
  const fakePriceChange = 'fakePriceChange';

  beforeEach(fakeAsync(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    mockSelection = {
      isEachWay: false,
      stake: 0,
      disabled: false,
      updateCurrency: jasmine.createSpy('updateCurrency'),
      formatBet: jasmine.createSpy('formatBet'),
      potentialPayout: 0,
      isOutright: true,
      categoryId: '16',
      typeName: 'league',
      eventId: '123',
      categoryName: 'football'
    };

    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
    };
    pubsub = {
      unsubscribe: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
      publish: jasmine.createSpy(),
      publishSync: jasmine.createSpy(),
      API: {
        REUSE_QUICKBET_SELECTION: 'REUSE_QUICKBET_SELECTION',
        PAYMENT_ACCOUNTS_PASSED: 'PAYMENT_ACCOUNTS_PASSED',
        UPDATE_QUICKBET_NOTIFICATION: 'UPDATE_QUICKBET_NOTIFICATION',
        ODDS_BOOST_CHANGE: 'ODDS_BOOST_CHANGE',
        QUICKBET_CARD_CHANGE: 'QUICKBET_CARD_CHANGE',
        AFTER_PANEL_RENDER: 'AFTER_PANEL_RENDER',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGIN: 'SESSION_LOGIN',
        LOGIN_DIALOG_CLOSED: 'LOGIN_DIALOG_CLOSED',
        USER_INTERACTION_REQUIRED: 'USER_INTERACTION_REQUIRED',
        LOGIN_POPUPS_END: 'LOGIN_POPUPS_END',
        OPEN_LOGIN_DIALOG: 'OPEN_LOGIN_DIALOG',
        QUICKBET_PANEL_CLOSE: 'QUICKBET_PANEL_CLOSE',
        FIRST_BET_PLACEMENT_TUTORIAL: 'FIRST_BET_PLACEMENT_TUTORIAL',
        FIRST_BET: 'FIRST_BET',
        MY_BET_PLACED:'MY_BET_PLACED'
      }
    };
    userService = {
      isInShopUser: jasmine.createSpy(),
      status: true
    };
    locale = {
      getString: jasmine.createSpy('getString')
    };
    quickbetDepositService = {
      init: jasmine.createSpy('init'),
      update: jasmine.createSpy('update'),
      clearQuickDepositModel: jasmine.createSpy(),
      quickDepositModel: {
        neededAmountForPlaceBet: true
      }
    };
    device = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true),
      isWrapper: false,
      isAndroid: false
    };
    infoDialog = { openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup') };
    quickbetService = {
      removeQBStateFromStorage: jasmine.createSpy(),
      quickDepositModel: { neededAmountForPlaceBet: false },
      acceptChangedBoost: jasmine.createSpy(),
      activateReboost: jasmine.createSpy('activateReboost'),
    };
    quickbetDataProviderService = {
      quickbetPlaceBetListener: {
        next: jasmine.createSpy()
      },
      quickbetReceiptListener: new Subject()
    };
    quickbetNotificationService = {
      config: { type: '' },
      clear: jasmine.createSpy('clear'),
      saveErrorMessage: jasmine.createSpy('saveErrorMessage'),
      saveErrorMessageWithCode: jasmine.createSpy('saveErrorMessageWithCode')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({ winAlerts: { enabled: true } })),
      getFeatureConfig : jasmine.createSpy('getFeatureConfig ').and.returnValue(observableOf({
        visibleNotificationIconsFootball: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnBetReceipt: ['android']
    }))
    };

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((callback: Function, miliseconds: number) => {
          callback();
        }),
        pageYOffset: 0
      },
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        },
        querySelector: jasmine.createSpy('querySelector'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    domToolsService = {
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    quickbetUpdateService = {
      getEventSuspension: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('quickbetUpdateService.getEventSuspension.subscribe').and.callFake(cb => cb(fakeSuspension))
      }),
      getPriceChange: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('quickbetUpdateService.getPriceChange.subscribe').and.callFake(cb => cb(fakePriceChange))
      })
    };
    arcUserService = {
      quickbet: true
    };

    jsEventMock = jasmine.createSpyObj('jsEventMock', ['stopPropagation']);

    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus').and.returnValue(true)
    };

    yourCallMarketService = {
      removeAllMarkets: false
    };

    nativeBridgeService = {
      betPlaceSuccessful: jasmine.createSpy('betPlaceSuccessful'),
      multipleEventPageLoaded: jasmine.createSpy('multipleEventPageLoaded'),
      onEventAlertsClick: jasmine.createSpy('onEventAlertsClick'),
      hasShowFootballAlerts: jasmine.createSpy('hasShowFootballAlerts').and.returnValue(true),
      hasOnEventAlertsClick: jasmine.createSpy('hasOnEventAlertsClick').and.returnValue(true),
      getMobileOperatingSystem: jasmine.createSpy('getMobileOperatingSystem').and.returnValue('android'),
      eventPageLoaded: jasmine.createSpy('eventPageLoaded')
    };
    dialogService={
      API:{
        animationModal:'animationModal'
      },
      closeDialog:jasmine.createSpy('closeDialog')
    }

    sessionStorageService = {
        get: jasmine.createSpy('get').and.callFake(
          n => {
            if(n === 'firstBetTutorial') { return {firstBetAvailable:'true'}} 
            else if(n === 'betPlaced') { return false} 
        }), 
      set: jasmine.createSpy('set')
    };

    spyOn(console, 'warn');
    user={username :'test'};
  }));

  function createComponent(init?: boolean) {
    component = new QuickbetPanelComponent(rendererService, pubsub, userService, locale, quickbetDepositService,
      device, infoDialog, quickbetService, quickbetDataProviderService, quickbetNotificationService, cmsService,
      windowRefService, domToolsService, router, quickbetUpdateService, changeDetectorRef, arcUserService, nativeBridgeService, serviceClosureService
      ,yourCallMarketService,dialogService,sessionStorageService,user,quickDepositIframeService);
    component.selection = mockSelection;
    component.title = 'quickbet';
    !!init && component.ngOnInit();
  }

  describe('@ngOnInit', () => {
    it('should create component', fakeAsync(() => {
      createComponent(true);
      tick();
      expect(component).toBeDefined();
    }));

    it('should check for quick bet panel close', () => {
      createComponent();
      component.ngOnInit();
      component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => {
        if (arg2.includes('QUICKBET_PANEL_CLOSE')) {
          callback();
          expect(component.closePanel).toHaveBeenCalled();
        }
      });
      expect(component.onBoardingData).toBeDefined();
    });

    it('should call isState(receipt)',()=>
    {
      createComponent();
      component.isLuckyDip=true;
      component.ngOnInit();
      spyOn(component,'goToState')
      component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => {
        if (arg2.includes('MY_BET_PLACED')) {
          callback(true);
          expect(locale.getString).toHaveBeenCalled();
          expect(component.goToState).toHaveBeenCalled();
          expect(locale.getString).toHaveBeenCalledWith('quickbet.betReceiptTitle');
        }
      });

    })

    it('should check for quick bet panel close with session', () => {
      createComponent();
      sessionStorageService.get.and.returnValue({firstBetAvailable:false});
      component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => {
        if (arg2 && arg2.includes('QB_PANEL_CLOSE')) {
          callback();
          expect(component.closePanel).toHaveBeenCalled();
        }
      });
      component.ngOnInit();
      expect(component.onBoardingData).toBeUndefined();
    });

    it('should select default content on closePanel', () => {
      createComponent(true);
      component.selection.markets = [{isCashoutAvailable: 'N'}];
      spyOn(component, 'isState').and.callFake(() => 'receipt' as any);
      sessionStorageService.get = jasmine.createSpy()
      .withArgs('cashOutAvail').and.returnValue(true)
      .withArgs('betPlaced').and.returnValue(true);
      component.closePanel();
      expect(component.onBoardingData).toBeDefined();
      expect(pubsub.publish).toHaveBeenCalledWith('FIRST_BET_PLACEMENT_TUTORIAL', { step: 'betDetails', tutorialEnabled: true, type: 'defaultContent' });
    })

    it('should select cashout content on closePanel', () => {
      createComponent(true);
      component.isLuckyDip=true;
      spyOn(component, 'isState').and.callFake(() => 'receipt' as any).and.returnValue(true);
      component.selection.markets = [{isCashoutAvailable: 'Y'}];
      sessionStorageService.get = jasmine.createSpy()
      .withArgs('cashOutAvail').and.returnValue(false)
      .withArgs('betPlaced').and.returnValue(true);
      component.closePanel();
      expect(component.onBoardingData).toBeDefined();
      expect(component.dialogService.closeDialog).toHaveBeenCalledWith('animationModal',true)
      expect(pubsub.publish).toHaveBeenCalledWith('FIRST_BET_PLACEMENT_TUTORIAL', { step: 'betDetails', tutorialEnabled: true, type: 'cashOut' });
    })

    describe('after SUCCESSFUL_LOGIN or SESSION_LOGOUT', () => {
      describe('when closing panel expected on any placeBet type', () => {
        beforeEach(() => {
          createComponent();
          spyOn(component, 'closePanel');
          component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2: string[], callback) => {
            if (Array.isArray(arg2) && (arg2.includes('SUCCESSFUL_LOGIN') || arg2.includes('SESSION_LOGOUT'))) {
              callback();
            }
          });
        });

        it('should hide panel if inshop user logged in', () => {
          userService.isInShopUser = jasmine.createSpy('isInShopUser').and.callFake(() => true);
          spyOn(component, 'isState').and.callFake(() => 'quickbet' as any);
          component.ngOnInit();

          expect(component.closePanel).toHaveBeenCalled();
        });

        it('should hide panel if bet receipt is shown', () => {
          userService.isInShopUser = jasmine.createSpy('isInShopUser').and.callFake(() => false);
          spyOn(component, 'isState').and.callFake(() => 'receipt' as any);
          component.ngOnInit();

          expect(component.closePanel).toHaveBeenCalled();
        });
      });

      describe('when placing bet or reloading quickbet', () => {
        beforeEach(() => {
          createComponent();
          spyOn(component, 'isState').and.returnValue(false);
          userService.isInShopUser = jasmine.createSpy().and.returnValue(false);
        });

        it('should update currency and reinit quickbet deposit model', () => {
          spyOn<any>(component,'checkArcUserOnLogIn');
          component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback('quickbet'));
          component['werePopupsShown'] = false;
          component.ngOnInit();

          expect(userService.isInShopUser).toHaveBeenCalled();
          expect(component.loginAndPlaceBets).toBe(true);
          expect(mockSelection.updateCurrency).toHaveBeenCalled();
          expect(quickbetDepositService.init).toHaveBeenCalledWith(true);
        });

        it('should reuse selection and clear notifications if it is not a quickbet', () => {
          component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback('notquickbet'));
          component.reuseSelection = jasmine.createSpy('reuseSelection');
          component['werePopupsShown'] = true;
          arcUserService.quickbet = false;
          component.ngOnInit();

          expect(userService.isInShopUser).toHaveBeenCalled();
          expect(component.viewState).toEqual('initial');
          expect(quickbetNotificationService.clear).toHaveBeenCalled();
          expect(component.reuseSelection).toHaveBeenCalled();
        });

        it('should reuse selection and clear notifications if popups were displayed', () => {
          component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback('quickbet'));
          component.reuseSelection = jasmine.createSpy('reuseSelection');
          component['werePopupsShown'] = true;
          component.ngOnInit();

          expect(component.viewState).toEqual('initial');
          expect(quickbetNotificationService.clear).toHaveBeenCalled();
          expect(component.reuseSelection).toHaveBeenCalled();
        });

        it('should go to initial state and reuse selection', () => {
          component['pubsub'].subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback('notquickbet'));
          component['werePopupsShown'] = true;
          component.ngOnInit();

          expect(component.viewState).toEqual('initial');
          expect(userService.isInShopUser).toHaveBeenCalled();
          expect(mockSelection.updateCurrency).not.toHaveBeenCalled();
          expect(component.viewState).toEqual('initial');
        });
      });
    });

    it('should subscribe to LOGIN_POPUPS_END event', () => {
      createComponent(true);
      expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetPanel', 'LOGIN_POPUPS_END', jasmine.any(Function));
    });


    it('should execute LOGIN_POPUPS_END event', fakeAsync(() => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'LOGIN_POPUPS_END') {
          loginAndPlaceBets = handler;
        }
      });

      createComponent(true);
      component.loginAndPlaceBets = true;

      expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetPanel', 'LOGIN_POPUPS_END', jasmine.any(Function));
      tick();
      loginAndPlaceBets();
      expect(quickbetDepositService.init.calls.count()).toEqual(1);
    }));

    it('onInitReboost', () => {
      createComponent(true);
      component['quickbetService'].acceptChangedBoost = jasmine.createSpy().and.returnValue(true);
      component.selection.reboost = true;
      component.placeBet = jasmine.createSpy('placeBet');

      component.ngOnInit();
      expect(component.placeBet).toHaveBeenCalled();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });

    it('should reuseSelection on reboost', () => {
      quickbetService.acceptChangedBoost = jasmine.createSpy().and.returnValue(true);
      createComponent(true);
      Object.defineProperty(component['userService'], 'bppToken', { value: 'dasda' });
      component['quickbetDepositService'].quickDepositModel.neededAmountForPlaceBet = false as any;
      component.selection.reboost = true;
      component.reuseSelection = jasmine.createSpy('reuseSelection');
      component.placeBet();

      expect(quickbetService.activateReboost).toHaveBeenCalled();
      expect(component.reuseSelection).toHaveBeenCalled();
    });

    it('should not reuseSelection without reboost', () => {
      quickbetService.acceptChangedBoost = jasmine.createSpy().and.returnValue(true);
      createComponent(true);
      Object.defineProperty(component['userService'], 'bppToken', { value: 'dasda' });
      component['quickbetDepositService'].quickDepositModel.neededAmountForPlaceBet = false as any;
      component.selection.reboost = false;
      component.reuseSelection = jasmine.createSpy('reuseSelection');
      component.placeBet();

      expect(quickbetService.activateReboost).not.toHaveBeenCalled();
      expect(component.reuseSelection).not.toHaveBeenCalled();
    });

    it('should place bets on \'login and place bets\' action after all popup will be shown', fakeAsync(() => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'PAYMENT_ACCOUNTS_PASSED') {
          placeBet = handler;
        } else if (listeners === 'LOGIN_POPUPS_END') {
          loginAndPlaceBets = handler;
        }
      });
      createComponent(true);
      component.loginAndPlaceBets = true;
      component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
      expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetPanel', 'LOGIN_POPUPS_END', jasmine.any(Function));
      spyOn<any>(component, 'checkArcUser');
      loginAndPlaceBets();
      placeBet();
      expect(quickbetDepositService.init.calls.count()).toEqual(1);
      expect(quickbetDepositService.init).toHaveBeenCalledWith(true);
      expect(component.loginAndPlaceBets).toBeFalsy();
      expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetPanel', 'PAYMENT_ACCOUNTS_PASSED', jasmine.any(Function));
    }));

    it('should call place bet listener only if all coditions is true', () => {
      createComponent(true);

      component['quickbetDepositService'].quickDepositModel.neededAmountForPlaceBet = '1';
      component.placeBet();

      component['quickbetDepositService'].quickDepositModel.neededAmountForPlaceBet = '';
      component.placeBetPending.state = true;
      component.placeBet();

      component.placeBetPending.state = false;
      Object.defineProperty(component['userService'], 'bppToken', { value: null , configurable: true});
      component.placeBet();

      Object.defineProperty(component['userService'], 'bppToken', { value: 'dasdas' , configurable: true});
      component.placeBet();

      expect(quickbetDataProviderService.quickbetPlaceBetListener.next).toHaveBeenCalledTimes(1);
    });

    it('should stop placing bet if notification popup is displayed after used has logged in', () => {
      pubsub.subscribe.and.callFake((name, listeners, handler) => {
        if (listeners === 'USER_INTERACTION_REQUIRED') {
          handler();
        }
      });
      spyOn<any>(component,'checkArcNotify');
      createComponent(true);

      expect(mockSelection.loginAndPlaceBets).toBeFalsy();
    });

    it('should trigger save error message and update quickbet notification', () => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'UPDATE_QUICKBET_NOTIFICATION') {
          handler({ msg: 'test msg', type: 'error' });
        }
      });
      spyOn<any>(component, 'checkArcError');
      createComponent(true);
      expect(pubsub.subscribe).toHaveBeenCalled();
    });

    it('should not trigger save error message and update quickbet notification', () => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'UPDATE_QUICKBET_NOTIFICATION') {
          handler({});
        }
      });
      createComponent(true);

      expect(quickbetNotificationService.saveErrorMessage).not.toHaveBeenCalled();
    });

    it('should trigger quickbet deposit update after QUICKBET_CARD_CHANGE', () => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'QUICKBET_CARD_CHANGE') {
          handler();
        }
      });
      mockSelection.stake = 1;
      createComponent(true);

      expect(quickbetNotificationService.clear).toHaveBeenCalled();
      expect(quickbetDepositService.update).toHaveBeenCalledWith(1, false);
    });

    it('should not trigger quickbet deposit update after QUICKBET_CARD_CHANGE when stake is 0', () => {
      (pubsub.subscribe as jasmine.Spy).and.callFake((name, listeners, handler) => {
        if (listeners === 'QUICKBET_CARD_CHANGE') {
          handler();
        }
      });
      createComponent(true);

      expect(quickbetDepositService.update).not.toHaveBeenCalled();
    });

    it('should set system config value', fakeAsync(() => {
      createComponent(true);
      component.ngOnInit();
      tick();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component.sysConfig).toEqual({ winAlerts: { enabled: true } });
    }));

    it('should subscribe to QUICKBET_CARD_CHANGE event', () => {
      component.selection.stake = '2.00';
      createComponent(true);

      expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetPanel', 'QUICKBET_CARD_CHANGE', jasmine.any(Function));
    });

    it('should set slide up flag', () => {
      createComponent(true);

      expect(component.slideUpAnimation).toBeTruthy();
    });

    describe('preventing stake modification during LOGIN & PLACE BET', () => {
      beforeEach(() => {
        const listeners = {};
        pubsub.subscribe = (channel: string, method: string, callback: Function) => {
          listeners[method] = callback;
        };
        pubsub.publish = (channel: string, method: string, _) => {
          listeners[method] && listeners[method]();
        };
        createComponent(true);
        component.ngOnInit();
      });

      it('should prevent stake modification during session login', () => {
        pubsub.publish('QuickbetComponent', pubsub.API.SESSION_LOGIN);

        expect(component.loginAndPlaceBets).toBeTruthy();
      });
    });
    describe('preventing stake modification during LOGIN & PLACE BET when dialog is closed', () => {
      beforeEach(() => {
        const listeners = {};
        pubsub.subscribe = (channel: string, method: string, callback: Function) => {
          listeners[method] = callback;
        };
        pubsub.publish = (channel: string, method: string, _) => {
          listeners[method] && listeners[method]();
        };
      });
      it('should prevent stake modification right after popup close (if user is in loginPending state)', () => {
        userService.loginPending = true;
        createComponent(true);
        component.ngOnInit();
        pubsub.publish('QuickbetComponent', pubsub.API.LOGIN_DIALOG_CLOSED);

        expect(component.loginAndPlaceBets).toBeTruthy();
      });

      it('should disable stake modification guard on login error', () => {
        userService.loginPending = true;
        createComponent(true);
        component.ngOnInit();
        pubsub.publish('QuickbetComponent', pubsub.API.LOGIN_DIALOG_CLOSED);
        pubsub.publish('QuickbetComponent', pubsub.API.FAILED_LOGIN);

        expect(component.loginAndPlaceBets).toBeFalsy();
      });

      it('should disable stake modification guard when bet is not pending', () => {
        userService.loginPending = false;
        createComponent(true);
        component.ngOnInit();
        pubsub.publish('QuickbetComponent', pubsub.API.LOGIN_DIALOG_CLOSED);

        expect(component.loginAndPlaceBets).toBeFalsy();
      });
    });

    it('should subscribe on events', () => {
      createComponent(true);
      expect(quickbetUpdateService.getEventSuspension).toHaveBeenCalled();
      expect(quickbetUpdateService.getPriceChange).toHaveBeenCalled();
      expect(quickbetUpdateService.getEventSuspension().subscribe).toHaveBeenCalled();
      expect(quickbetUpdateService.getPriceChange().subscribe).toHaveBeenCalled();
    });

    it('should receive a event for the suspension handler', () => {
      createComponent(true);
      expect(component.placeSuspendedErr).toEqual(fakeSuspension);
      expect(component.showSuspendedNotification).toBe(fakeSuspension.disableBet);
      expect(component.showPriceChangeMessage).toBeFalsy();
    });

    it('should receive a event for the priceChange handler', () => {
      quickbetUpdateService = {
        getEventSuspension: jasmine.createSpy().and.returnValue({
          subscribe: jasmine.createSpy('quickbetUpdateService.getEventSuspension.subscribe'),
        }),
        getPriceChange: jasmine.createSpy().and.returnValue({
          subscribe: jasmine.createSpy('quickbetUpdateService.getPriceChange.subscribe').and.callFake(cb => cb(fakePriceChange))
        })
      };
      createComponent();
      component.selection.onStakeChange = jasmine.createSpy('onStakeChange');
      component.ngOnInit();
      expect(component.priceChangeText).toBe(fakePriceChange);
      expect(component.showPriceChangeMessage).toBeTruthy();
      expect(component.selection.onStakeChange).toHaveBeenCalled();
    });

    it('should receive a event for the priceChange handler (showSuspendedNotification = true)', () => {
      quickbetUpdateService = {
        getEventSuspension: jasmine.createSpy().and.returnValue({
          subscribe: jasmine.createSpy('quickbetUpdateService.getEventSuspension.subscribe'),
        }),
        getPriceChange: jasmine.createSpy().and.returnValue({
          subscribe: jasmine.createSpy('quickbetUpdateService.getPriceChange.subscribe').and.callFake(cb => cb(fakePriceChange))
        })
      };
      createComponent();
      component.showSuspendedNotification = true;
      component.ngOnInit();
      expect(component.priceChangeText).toBeUndefined();
      expect(component.showPriceChangeMessage).toBeFalsy();
    });
  });

  describe('@ngOnDestroy', () => {
    it('should not trigger save error message and update quickbet notification', () => {
      createComponent();
      (component['eventSuspensionSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      (component['priceChangeSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      spyOn<any>(component, 'toggleBodyScroll');
      component['BODY_CLASS'] = '';
      component.ngOnDestroy();
      expect(component['toggleBodyScroll']).toHaveBeenCalledWith(false);
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('QuickbetPanel');
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('QuickBetPanelClose');
      expect(quickbetService.removeQBStateFromStorage).toHaveBeenCalled();
    });

    it('should not trigger save error message and update quickbet notification', () => {
      createComponent();
      (component['eventSuspensionSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      (component['priceChangeSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      component['BODY_CLASS'] = 'quickbet-opened';
      component.ngOnDestroy();
      expect(quickbetService.removeQBStateFromStorage).not.toHaveBeenCalled();
    });

    it('should unsubscribe from quickbetUpdateService events', () => {
      createComponent();
      (component['eventSuspensionSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      (component['priceChangeSubscription'] as any) = { unsubscribe: jasmine.createSpy() };
      component.ngOnDestroy();
      expect(component['eventSuspensionSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['priceChangeSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['pubsub'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('@ngAfterContentInit', () => {
    it('should not trigger save error message and update quickbet notification', () => {
      createComponent(true);
      component.ngAfterContentInit();
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubsub.API.AFTER_PANEL_RENDER);
    });
  });

  it('should set viewState', () => {
    createComponent(true);
    component.goToState('initial');

    expect(component.viewState).toEqual('initial');
  });

  it('should open login dialog when user is logged out', () => {
    userService.status = false;
    createComponent(true);
    component.placeBet();

    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.OPEN_LOGIN_DIALOG, {
      placeBet: 'quickbet',
      moduleName: 'quickbet'
    });
  });

  it('reuseSelection (quickbet)', () => {
    createComponent(true);
    component.isQuickbet = () => true;
    component.selection.isBoostActive = false;

    component.reuseSelection();

    expect(pubsub.publish).toHaveBeenCalledWith(
      'REUSE_QUICKBET_SELECTION', component.selection.requestData
    );
    expect(pubsub.publish).toHaveBeenCalledWith(
      'ODDS_BOOST_CHANGE', false
    );
  });

  it('reuseSelection (not quickbet)', () => {
    createComponent(true);
    component.isQuickbet = () => false;
    component.reuseSelectionFnHandler = jasmine.createSpy();

    component.reuseSelection();

    expect(component.reuseSelectionFnHandler).toHaveBeenCalledTimes(1);
  });

  it('closePanel', () => {
    createComponent(true);
    component.isState = () => false;
    component.closeFnHandler = jasmine.createSpy();
    component.closePanel(jsEventMock);

    expect(quickbetDepositService.clearQuickDepositModel).toHaveBeenCalled();
    expect(component.closeFnHandler).toHaveBeenCalled();
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
    expect(pubsub.publishSync).toHaveBeenCalledWith('ODDS_BOOST_CHANGE');
    expect(jsEventMock.stopPropagation).toHaveBeenCalled();
  });

  it('closePanel and hide', () => {
    createComponent(true);
    component.isState = () => true;
    component.closeFnHandler = jasmine.createSpy();
    component.selection = {markets:[{isCashoutAvailable:'Y'}]} as any;
    component.closePanel(jsEventMock);

    expect(quickbetDepositService.clearQuickDepositModel).toHaveBeenCalled();
    expect(component.closeFnHandler).toHaveBeenCalled();
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
    expect(pubsub.publishSync).toHaveBeenCalledWith('ODDS_BOOST_CHANGE');
    expect(jsEventMock.stopPropagation).toHaveBeenCalled();
  });

  it('closePanel and hide with markets', () => {
    createComponent(true);
    component.isState = () => true;
    component.closeFnHandler = jasmine.createSpy();
    component.selection = {markets:[{isCashoutAvailable:'N'}]} as any;
    component.closePanel(jsEventMock);

    expect(quickbetDepositService.clearQuickDepositModel).toHaveBeenCalled();
    expect(component.closeFnHandler).toHaveBeenCalled();
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
    expect(pubsub.publishSync).toHaveBeenCalledWith('ODDS_BOOST_CHANGE');
    expect(jsEventMock.stopPropagation).toHaveBeenCalled();
  });

  it('should emit close handler', () => {
    quickbetNotificationService.config = { type: 'warning' };
    createComponent(true);
    spyOn(component.closeFn, 'emit');

    component.closeFnHandler();

    expect(component.closeFn.emit).toHaveBeenCalledWith(false);
    expect(quickbetNotificationService.clear).toHaveBeenCalled();
  });

  it('should emit reuseSelection handler', () => {
    createComponent(true);
    spyOn(component.reuseSelectionFn, 'emit');

    component.reuseSelectionFnHandler();

    expect(component.reuseSelectionFn.emit).toHaveBeenCalled();
  });

  it('should emit addToBetslip handler', () => {
    createComponent(true);
    spyOn(component.addToBetslipFn, 'emit');

    component.addToBetslipFnHandler();

    expect(component.addToBetslipFn.emit).toHaveBeenCalled();
  });

  it('should trigger quickbetReceiptListener', fakeAsync(() => {
    locale.getString.and.returnValue('testString');
    sessionStorageService.get.and.returnValue(false);
    createComponent(true);
    quickbetDataProviderService.quickbetReceiptListener.next([{receipt: {id: '123'}, categoryId: '16'}]);
    tick();
    component['placeBetListener']();
    tick();
    expect(component.placeBetPending.state).toBeFalsy();
    expect(locale.getString).toHaveBeenCalledWith('quickbet.betReceiptTitle');
    expect(component.title).toEqual('testString');
    expect(component.betReceipt).toEqual({receipt: {id: '123'}, footballAlertsVisible: false, categoryId: '16'});
    expect(component.viewState).toEqual('receipt');
  }));

  it('should show error while placing quickbet', fakeAsync(() => {
    createComponent(true);

    component['placeBetListener']();
    tick();
    quickbetDataProviderService.quickbetReceiptListener.next([{ error: 'error' }]);
    tick();
    expect(component.placeBetPending.state).toBeFalsy();
    expect(quickbetNotificationService.saveErrorMessageWithCode).toHaveBeenCalledWith('error', 'warning', '', undefined);
  }));

  it('should set youcall title if it is no quickbet', fakeAsync(() => {
    locale.getString.and.returnValue('yourcallString');
    createComponent(true);
    component['BODY_CLASS'] = 'yourcall';

    component['placeBetListener']();
    tick();
    quickbetDataProviderService.quickbetReceiptListener.next({
      selection: mockSelection,
      data: { receipt: 'receipt', totalStake: 'totalStake' }
    });
    tick();
    expect(locale.getString).toHaveBeenCalledWith('quickbet.yourCallBetreceipt');
    expect(component.title).toEqual('yourcallString');
    expect(component.betReceipt).toEqual(jasmine.any(Object));
  }));

  it('should call saveErrorMessageWithCode method with errorCode', fakeAsync(() => {
    createComponent(true);

    component['placeBetListener']();
    quickbetDataProviderService.quickbetReceiptListener.next([{ error: 'Stake is too low', errorCode: 'STAKE_TOO_LOW' }]);
    tick();

    expect(component.placeBetPending.state).toBeFalsy();
    expect(quickbetNotificationService.saveErrorMessageWithCode).toHaveBeenCalledWith('Stake is too low', 'warning', '', 'STAKE_TOO_LOW');
  }));

  it('should have winAlert as stepType for onboarding', fakeAsync(() => {
    device.isWrapper = true;
    createComponent(true);

    quickbetDataProviderService.quickbetReceiptListener.next([{receipt: {id: '123'}}]);
    tick();
    component['placeBetListener']();
    tick();

    expect(component.onBoardingData.type).toBe('winAlert');
  }));

  it('should remove body class', () => {
    createComponent(true);
    component['handleScroll'] = jasmine.createSpy('handleScroll');
    component['rendererService'].renderer.removeClass = jasmine.createSpy('removeClass');

    component['toggleBodyScroll'](false);

    expect(component['rendererService'].renderer.removeClass).toHaveBeenCalled();
    expect(component['handleScroll']).toHaveBeenCalledWith(false);
  });

  it('should add body class', () => {
    createComponent(true);
    component['handleScroll'] = jasmine.createSpy('handleScroll');
    component['rendererService'].renderer.addClass = jasmine.createSpy('addClass');

    component['toggleBodyScroll'](true);

    expect(component['rendererService'].renderer.addClass).toHaveBeenCalled();
    expect(component['handleScroll']).toHaveBeenCalledWith(true);
  });

  it('should not toggle body scroll', () => {
    windowRefService.document = {
      addEventListener: jasmine.createSpy('addEventListener')
    };
    createComponent(true);

    component['toggleBodyScroll'](false);

    expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
    expect(rendererService.renderer.removeClass).not.toHaveBeenCalled();
  });

  it('should sets YC bet receipt properties(default freebet value)', () => {
    const YCBetReseipt = ({
      selection: mockSelection,
      data: { receipt: 'receipt', totalStake: 'totalStake', betId: '123' }
    } as any);
    createComponent(true);

    component['setYCBetReceiptProps'](YCBetReseipt);

    expect(component.betReceipt.stake.freebet).toEqual('0');
  });

  it('should sets YC bet receipt date', () => {
    const YCBetReseipt = ({
      selection: mockSelection,
      data: { receipt: 'receipt', totalStake: 'totalStake', date: 'someDate', betId: '678' }
    } as any);
    createComponent(true);

    component['setYCBetReceiptProps'](YCBetReseipt);

    expect(component.betReceipt.date).toEqual('someDate');
  });

  it('should sets YC bet receipt properties', () => {
    mockSelection.freebet = {
      freebetTokenValue: '123'
    };
    mockSelection.freeBetOfferCategory = 'Bet Pack';
    const YCBetReseipt = ({
      selection: mockSelection,
      data: { receipt: 'receipt', totalStake: 'totalStake', betId: '8970' }
    } as any);
    createComponent(true);

    component['setYCBetReceiptProps'](YCBetReseipt);
    expect(component.betReceipt.stake.freebetOfferCategory).toEqual('Bet Pack');
    expect(component.betReceipt.stake.freebet).toEqual('123');
  });

  describe('#closeFnHandler', () => {
    beforeEach(() => {
      createComponent();
      component['closeFn'].emit = jasmine.createSpy('component[closeFn].emit');
      component['reuseSelectionFn'].emit = jasmine.createSpy('component[reuseSelectionFn].emit');
    });

    it('should call closeFnHandler QuickBet close case', () => {
      // @ts-ignore
      component['quickbetNotificationService'] = { config: { type: '' }, clear: jasmine.createSpy('clear') };
      component['BODY_CLASS'] = 'quickbet-opened';
      component.closeFnHandler();

      expect(quickbetNotificationService.clear).not.toHaveBeenCalled();
      expect(component['closeFn'].emit).toHaveBeenCalled();
    });

    it('should call closeFnHandler QuickBet close case', () => {
      // @ts-ignore
      component['quickbetNotificationService'] = { config: { type: 'warning' }, clear: jasmine.createSpy('clear') };
      component['BODY_CLASS'] = 'quickbet-opened';
      component.closeFnHandler();

      expect(component['quickbetNotificationService'].clear).toHaveBeenCalled();
      expect(component['closeFn'].emit).toHaveBeenCalled();
    });

    it('should call closeFnHandler BYB close case', () => {
      component['viewState'] = 'receipt';
      component['BODY_CLASS'] = '';
      spyOn(component, 'isState');
      component.closeFnHandler();

      expect(component['closeFn'].emit).toHaveBeenCalled();
    });

    it('should call closeFnHandler BYB reuse selections', () => {
      component['BODY_CLASS'] = '';
      component['viewState'] = 'initial';
      component.closeFnHandler();

      expect(component['reuseSelectionFn'].emit).toHaveBeenCalled();
    });
  });

  describe('@handleScroll', () => {
    it('should not add html class if it is not wrapper', () => {
      createComponent(true);
      component['rendererService'].renderer.addClass = jasmine.createSpy('addClass');
      component['handleScroll'](true);
      expect(windowRefService.document.querySelector).not.toHaveBeenCalled();
    });

    it('should not add html class if it is not android', () => {
      device.isAndroid = true;
      createComponent(true);
      component['handleScroll'](true);
      expect(windowRefService.document.querySelector).not.toHaveBeenCalled();
    });

    it('should add html class for android wrapper', () => {
      device.isAndroid = true;
      device.isWrapper = true;
      createComponent(true);

      component['handleScroll'](true);

      expect(windowRefService.document.querySelector).toHaveBeenCalledWith('html');
      expect(rendererService.renderer.addClass).toHaveBeenCalled();
      expect(component['windowScrollY']).toBe(0);
    });

    it('should remove html class for android wrapper and scroll to previous page position', () => {
      device.isAndroid = true;
      device.isWrapper = true;
      createComponent(true);

      component['handleScroll'](false);

      expect(windowRefService.document.querySelector).toHaveBeenCalledWith('html');
      expect(rendererService.renderer.removeClass).toHaveBeenCalled();
      expect(domToolsService.scrollPageTop).toHaveBeenCalledWith(0);
    });
  });

  it('should hide iframe and close window', () => {
    createComponent();
    component.selection.stake = '5';
    component.onCloseQuickDepositWindow();

    expect(quickbetDepositService.update).toHaveBeenCalledWith(component.selection.stake);
    expect(component.showIFrame).toBeFalsy();
    expect(component.quickDepositFormExpanded).toBeFalsy();
    expect(component.showPriceChangeMessage).toBeFalsy();
  });

  it('should hide iframe, close window and place bet', () => {
    createComponent();
    component.placeBet = jasmine.createSpy();
    component.closeIFrame();
    expect(component.showIFrame).toBeFalsy();
    expect(component.quickDepositFormExpanded).toBeFalsy();
    expect(component.placeBet).toHaveBeenCalled();
  });

  it('should set iframeLoaded property to true', () => {
    createComponent();
    component.onOpenIframe();
    expect(component.showIFrame).toBeTruthy();
    expect(component.iframeLoaded).toBeTruthy();
    expect(component.showPriceChangeMessage).toBeFalsy();
  });

  it('#getTotalStake is each way selection', () => {
    createComponent();
    component.selection.isEachWay = true;
    component.selection.stake = '5';
    expect(component.getTotalStake()).toBe(10);
  });

  it('#getTotalStake is not each way selection', () => {
    createComponent();
    component.selection.isEachWay = false;
    component.selection.stake = '5';
    expect(component.getTotalStake()).toBe(5);
  });
  describe('checkArcUser', () => {
    it('should not allow to place bet with quickbet', () => {
      createComponent();
      arcUserService.quickbet = true;
      spyOn(component.addToBetslipFn, 'emit');
      component['checkArcUser']();
      expect(component.addToBetslipFn.emit).toHaveBeenCalled();
    });
    it('should allow to place bet with quickbet', () => {
      createComponent();
      arcUserService.quickbet = false;
      component.placeBet = jasmine.createSpy('placeBet');
      component['checkArcUser']();
      expect(component.placeBet).toHaveBeenCalled();
    });
  });
  describe('checkArcUserOnLogIn', () => {
    it('should login and send to betslip', () => {
      createComponent();
      spyOn(component,'closePanel');
      arcUserService.quickbet = true;
      component['checkArcUserOnLogIn']();
      expect(component.closePanel).toHaveBeenCalled();
    });
    it('should login and not send to betslip', () => {
      createComponent();
      spyOn(component,'closePanel');
      arcUserService.quickbet = false;
      component['checkArcUserOnLogIn']();
      expect(component.closePanel).not.toHaveBeenCalled();
    });
  });
  describe('checkArcNotify', () => {
    it('should add to betslip if notification pops up', () => {
      createComponent();
      arcUserService.quickbet = true;
      spyOn(component.addToBetslipFn, 'emit');
      component['checkArcNotify']();
      expect(component.addToBetslipFn.emit).toHaveBeenCalled();
    });
    it('should show quickbet if notification pops up', () => {
      createComponent();
      arcUserService.quickbet = false;
      component['checkArcNotify']();
      expect(quickbetDepositService.update).toHaveBeenCalled();
    });
  });
  describe('checkArcError', () => {
    it('should add error msg to betslip', () => {
      createComponent();
      spyOn(component,'closePanel');
      arcUserService.quickbet = true;
      const message = { msg: 'test msg', type: 'error' };
      component['checkArcError'](message);
      expect(component.closePanel).toHaveBeenCalled();
    });
    it('should add error msg to quickbet', () => {
      createComponent();
      arcUserService.quickbet = false;
      const message = { msg: 'test msg', type: 'error' };
      component['checkArcError'](message);
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalled();
    });
  });
  describe('serviceClosure', () => {
    it('should userServiceClosureOrPlayBreak to be called for addToBetslipFnHandler', () => {
      createComponent(true);
      serviceClosureService.userServiceClosureOrPlayBreak = true;
      spyOn(component.addToBetslipFn, 'emit');
      component.addToBetslipFnHandler();
      expect(component.addToBetslipFn.emit).not.toHaveBeenCalled();
    });
    it('should userServiceClosureOrPlayBreak to be called for placeBet', () => {
      createComponent(true);
      serviceClosureService.userServiceClosureOrPlayBreak = true;
      component.placeBet();
      expect(component.selection.stake).toBeNull();
    });
  });
  describe('isState', () => {
    it('isState true', () => {
      component.selection = {state : 'st1', error : false} as any;
      component.viewState = 'receipt';
      component.isState('state');
      expect(yourCallMarketService.removeAllMarkets).toBeFalsy();
    });
  });
  it('isState true', () => {

    component.firstBetBoostEmit({});
    expect(component.onBoardingData).toBeDefined();
  });

  it('handleFootballAlerts', () => {
    component.betReceipt = {footballBellActive : false};
    component['handleFootballAlerts']({ detail: { isEnabled: true } });
    expect(component.betReceipt.footballBellActive).toEqual(true);
  });
  describe('checkFootballAlerts', () => {
    beforeEach(() => {
      createComponent(true);
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      nativeBridgeService.getMobileOperatingSystem.and.returnValue('android');
      mockSelection.isOutright = false;
      component.betReceipt = {};
    });

    it('should NOT do football Alerts Visible if no configuration in CMS', () => {
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {}
      }));

      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.betReceipt.footballAlertsVisible).toBeFalsy();
    });

    it('should get visible notification icons from sport types', () => {
      component.betReceipt = {};
      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.betReceipt.footballAlertsVisible).toBeTruthy();
      expect(nativeBridgeService.eventPageLoaded).toHaveBeenCalledWith(mockSelection.eventId, mockSelection.categoryName.toLocaleLowerCase());
    });

    it('should get visible notification icons from sport types - when visibleNotificationIcons only cms data available', () => {
      component.betReceipt = {};
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnBetReceipt: ['android']
      }));
      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.betReceipt.footballAlertsVisible).toBeTruthy();
      expect(nativeBridgeService.eventPageLoaded).toHaveBeenCalledWith(mockSelection.eventId, mockSelection.categoryName.toLocaleLowerCase());
    });

    it('should get visible notification icons from sport types - when hasShowFootballAlerts only enabled', () => {
      component.betReceipt = {};
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(false);
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnBetReceipt: ['android']
      }));
      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.betReceipt.footballAlertsVisible).toBeTruthy();
      expect(nativeBridgeService.eventPageLoaded).toHaveBeenCalledWith(mockSelection.eventId, mockSelection.categoryName.toLocaleLowerCase());
    });

    it('should set footballAlertsVisible (isOSPermitted = true, isFootball = false)', () => {
      component.betReceipt = {};
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        NativeConfig: {
          visibleNotificationIconsFootball: {
            multiselectValue: ['android'],
            value: []
          }
        }
      }));
      mockSelection.isOutright = false;

      component.checkFootballAlerts();
      expect(component.betReceipt.footballAlertsVisible).toBeFalsy();
    });

    it('should not set footballAlertsVisible', () => {
      component.betReceipt = {};
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      cmsService.getFeatureConfig.and.returnValue(observableOf({}));
      mockSelection.isOutright = false;

      component.checkFootballAlerts();

      expect(component.betReceipt.footballAlertsVisible).toBeFalsy();
    });

    it('should not set footballAlertsVisible - when type mismatch of not a string', () => {
      component.betReceipt = {};
      nativeBridgeService.hasOnEventAlertsClick.and.returnValue(true);
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIconsFootball: {
          multiselectValue: ['android'],
          value: ['notfound']
        },
        displayOnBetReceipt: ['android']
      }))
      mockSelection.isOutright = false;

      component.checkFootballAlerts();

      expect(component.betReceipt.footballAlertsVisible).toBeFalsy();
      expect(nativeBridgeService.eventPageLoaded).not.toHaveBeenCalled();
    });

    it('should get visible notification icons from sport types - when OS not Permitted', () => {
      component.betReceipt = {};
      cmsService.getFeatureConfig.and.returnValue(observableOf({
        visibleNotificationIcons: {
          multiselectValue: ['android'],
          value: 'league'
        },
        displayOnBetReceipt: ['dummy']
      }));
      component.checkFootballAlerts();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
      expect(component.betReceipt.footballAlertsVisible).toBeFalsy();
      expect(nativeBridgeService.eventPageLoaded).not.toHaveBeenCalled();
    });
  });

  it('should open quickdeposit popup', () => {
    component.openQuickDeposit();
    expect(component.quickDepositFormExpanded ).toBeTruthy();
  });
});
