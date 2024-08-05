import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';
import { OddsBoostService } from './odds-boost.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

describe('OddsBoostService', () => {
  let service: OddsBoostService;
  let cmsService;
  let coreToolsService;
  let dialogService;
  let bppService;
  let storageService;
  let userService;
  let betslipDataService;
  let infoDialogService;
  let localeService;
  let pubSubService;
  const fracToDecService = new FracToDecService({} as any);
  let gtmService;
  let router;
  let changeCallback;
  let spCallback;
  let boostSendGtmCallback;
  let openInfoDialogCallback;
  let betslipSlideoutCallback;
  let storeOddsBoostCallback;
  let decrementOddsBoostCounterCallback;
  let freeBetsBadgeLoader;

  beforeEach(() => {
    freeBetsBadgeLoader = {
      addOddsBoostCounter: jasmine.createSpy('addOddsBoostCounter')
    };

    cmsService = {
      initialData: {
        oddsBoost: {}
      },
      getOddsBoost: jasmine.createSpy().and.returnValue(observableOf({})),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        maxPayOut: {
          maxPayoutFlag: true,
          maxPayoutMsg: 'your return is one million'
        },
        OddsBoostMsgConfig:{
          noThanks: 'No, thanks',
          yesPlease: 'Yes, please',
          okThanks: 'Ok, thanks',
          continueWith: 'WANT TO CONTINUE?',
          cancelBoostPriceMessage: 'Selecting a free bet or bet token will cancel your boosted price, are you sure you want to continue',
          cantBoostMessage: 'Unfortunately you can’t boost your odds while using a free bet or bet token. Please de-select your free bet to boost your odds'
        }
      }))
    };
    coreToolsService = {
      getOwnDeepProperty: jasmine.createSpy('getOwnDeepProperty')
    };
    dialogService = {
      openDialog: jasmine.createSpy().and.callFake((msg, comp, bool, cb) => {
        if (cb.onBeforeClose) {
          cb.onBeforeClose();
        }
      }),
      closeDialog: jasmine.createSpy(),
      API: {
        informationDialog: 'informationDialog'
      }
    };
    bppService = {
      send: jasmine.createSpy().and.returnValue(observableOf({}))
    };
    storageService = {
      get: jasmine.createSpy(),
      set: jasmine.createSpy(),

    };
    userService = {
      username: 'user1',
      currencySymbol: 'GBP',
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false)
    };
    betslipDataService = {
      bets: [{ oddsBoost: true }]
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy()
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((file, method, cb) => {
        if (method === pubSubApi.ODDS_BOOST_CHANGE) {
          changeCallback = cb;
        } else if (method === pubSubApi.ODDS_BOOST_HANDLE_SP) {
          spCallback = cb;
        } else if (method === pubSubApi.ODDS_BOOST_SEND_GTM) {
          boostSendGtmCallback = cb;
        } else if (method === pubSubApi.ODDS_BOOST_INFO_DIALOG) {
          openInfoDialogCallback = cb;
        } else if (method === pubSubApi['show-slide-out-betslip-true']) {
          betslipSlideoutCallback = cb;
        } else if (method === pubSubApi.ODDS_BOOST_CHECK_BS_SELECTIONS) {
          cb();
        } else if (method === 'show-slide-out-betslip-true') {
          betslipSlideoutCallback = cb;
        } else if (method === 'STORE_ODDS_BOOST') {
          storeOddsBoostCallback = cb;
        } else if (method === 'ODDS_BOOST_DECREMENT_COUNTER') {
          decrementOddsBoostCounterCallback = cb;
        }
      }),
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    router = {
      navigateByUrl: jasmine.createSpy('open')
    };

    service = new OddsBoostService(
      cmsService,
      coreToolsService,
      dialogService,
      bppService,
      storageService,
      userService,
      infoDialogService,
      localeService,
      pubSubService,
      betslipDataService,
      fracToDecService,
      gtmService,
      router,
      freeBetsBadgeLoader
    );
  });

  it('init', () => {
    const tokens: any[] = [{}];
    service.init(tokens);

    expect(freeBetsBadgeLoader.addOddsBoostCounter).toHaveBeenCalledWith(tokens);
    expect(service.tokens).toBe(tokens);
  });

  it('should subscribe to events', () => {
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_CHANGE', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_HANDLE_SP', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_SEND_GTM', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_CHECK_BS_SELECTIONS', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'show-slide-out-betslip-true', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_INFO_DIALOG', jasmine.anything());
    expect(pubSubService.subscribe).toHaveBeenCalledWith('OddsBoostService', 'ODDS_BOOST_DECREMENT_COUNTER', jasmine.anything());
  });

  it('should subscribe to ODDS_BOOST_DECREMENT_COUNTER and decrement counter', () => {
    userService.status = true;
    service['boostTokens'] = [{} as any];

    decrementOddsBoostCounterCallback();

    expect(freeBetsBadgeLoader.addOddsBoostCounter).toHaveBeenCalledWith([]);
  });

  it('should subscribe to ODDS_BOOST_DECREMENT_COUNTER and decrement counter, no error is no tokens', () => {
    userService.status = true;
    service['boostTokens'] = null;
    decrementOddsBoostCounterCallback();

    expect(freeBetsBadgeLoader.addOddsBoostCounter).toHaveBeenCalledWith([]);
  });

  it('should not decrement boosts counter is not loggedin', () => {
    userService.status = false;
    decrementOddsBoostCounterCallback();

    expect(freeBetsBadgeLoader.addOddsBoostCounter).not.toHaveBeenCalled();
  });


  it('isBoostActive', () => {
    service['boostActive'] = true;
    expect(service['isBoostActive']()).toBe(service['boostActive']);
  });

  it('showTokensInfoDialog (no available tokens)', fakeAsync(() => {
    service.isNewTokensAvailable = () => false;
    service.getOddsBoostTokens = jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([]));
    service.getStorageTokens = jasmine.createSpy('getStorageTokens');
    service.storeTokens = jasmine.createSpy('storeTokens');

    service.showTokensInfoDialog().subscribe();
    tick();

    expect(service.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(service.getStorageTokens).toHaveBeenCalled();
    expect(service.storeTokens).toHaveBeenCalled();
    expect(dialogService.openDialog).not.toHaveBeenCalled();
   }));

  it('showTokensInfoDialog (available tokens present)', fakeAsync(() => {
    service.isNewTokensAvailable = () => true;
    service.getOddsBoostTokens = jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([]));
    service.getStorageTokens = jasmine.createSpy('getStorageTokens');
    service.storeTokens = jasmine.createSpy('storeTokens');

    service.showTokensInfoDialog().subscribe();
    tick();

    expect(service.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_INTERACTION_REQUIRED');
    expect(service.getStorageTokens).toHaveBeenCalled();
    expect(service.storeTokens).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'oddsBoostInfo', jasmine.any(Function), false, jasmine.any(Object)
    );
  }));

  it('showTokensInfoDialog (available tokens present) with showToggle set to true', fakeAsync(() => {
    service.isNewTokensAvailable = () => true;
    service.getOddsBoostTokens = jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([]));
    service.getStorageTokens = jasmine.createSpy('getStorageTokens');
    service.storeTokens = jasmine.createSpy('storeTokens');

    service.showTokensInfoDialog().subscribe();
    tick();

    expect(service.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_INTERACTION_REQUIRED');
    expect(service.getStorageTokens).toHaveBeenCalled();
    expect(service.storeTokens).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'oddsBoostInfo', jasmine.any(Function), false, jasmine.any(Object)
    );
  }));

  it('showTokensInfoDialog (available tokens present) with showToggle set to false', fakeAsync(() => {
    service.isNewTokensAvailable = () => true;
    service.getOddsBoostTokens = jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([]));
    service.getStorageTokens = jasmine.createSpy('getStorageTokens');
    service.storeTokens = jasmine.createSpy('storeTokens');
    cmsService.initialData.oddsBoost.allowUserToToggleVisibility = false;

    service.showTokensInfoDialog().subscribe();
    tick();

    expect(service.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_INTERACTION_REQUIRED');
    expect(service.getStorageTokens).toHaveBeenCalled();
    expect(service.storeTokens).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'oddsBoostInfo', jasmine.any(Function), false, jasmine.any(Object)
    );
  }));

  it('showTokensInfoDialog (available tokens present) with showToggle not configured on CMS site', fakeAsync(() => {
    service.isNewTokensAvailable = () => true;
    service.getOddsBoostTokens = jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([]));
    service.getStorageTokens = jasmine.createSpy('getStorageTokens');
    service.storeTokens = jasmine.createSpy('storeTokens');
    delete cmsService.initialData.oddsBoost.allowUserToToggleVisibility;

    service.showTokensInfoDialog().subscribe();
    tick();

    expect(service.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_INTERACTION_REQUIRED');
    expect(service.getStorageTokens).toHaveBeenCalled();
    expect(service.storeTokens).toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'oddsBoostInfo',
      jasmine.any(Function),
      false, {
      oddsBoostTokens: [],
      oddsBoostConfig: jasmine.any(Object),
      onBeforeClose: jasmine.any(Function)
    }
    );
  }));

  describe('showInfoDialog', () => {
    it('show dialog', () => {
      OddsBoostService.maxBoostValue = '1';

      service.showInfoDialog();

      expect(localeService.getString).toHaveBeenCalledWith('oddsboost.infoDialog.title');
      expect(localeService.getString).toHaveBeenCalledWith(
        'oddsboost.infoDialog.text', [OddsBoostService.maxBoostValue, userService.currencySymbol]
      );
      expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    });

    it('show dialog with more button', () => {
      cmsService.initialData.oddsBoost.moreLink = 'more';
      infoDialogService.openInfoDialog.and.callFake((...args) => args[5][0].handler());

      service.showInfoDialog();

      expect(router.navigateByUrl).toHaveBeenCalledWith('more');
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });
  });

  it('openFirstTimeDialog (1st time)', () => {
    service.showInfoDialog = jasmine.createSpy();
    service.isOddsBoostBetslipHeaderAvailable = () => true;
    OddsBoostService.oddsBoostSeen = false;
    OddsBoostService.maxBoostValue = '10';
    service['openFirstTimeDialog']();

    expect(OddsBoostService.oddsBoostSeen).toBeTruthy();
    expect(storageService.set).toHaveBeenCalledWith('oddsBoostSeen', true);
    expect(service.showInfoDialog).toHaveBeenCalled();
  });

  it('openFirstTimeDialog (2nd time)', () => {
    service.isOddsBoostBetslipHeaderAvailable = () => true;
    OddsBoostService.oddsBoostSeen = true;
    OddsBoostService.maxBoostValue = '10';
    service['openFirstTimeDialog']();

    expect(storageService.set).not.toHaveBeenCalled();
  });

  it('should openFirstTimeDialog', () => {
    OddsBoostService.oddsBoostSeen = false;
    OddsBoostService.maxBoostValue = '75';
    service.isOddsBoostBetslipHeaderAvailable = () => true;
    openInfoDialogCallback();
    expect(storageService.set).toHaveBeenCalledWith('oddsBoostSeen', true);
  });

  it('should openFirstTimeDialog on betslip slideout', () => {
    OddsBoostService.oddsBoostSeen = false;
    OddsBoostService.maxBoostValue = '10';
    service.isOddsBoostBetslipHeaderAvailable = () => true;
    betslipSlideoutCallback();
    expect(storageService.set).toHaveBeenCalledWith('oddsBoostSeen', true);
  });

  it('isOddsBoostEnabled', () => {
    service.isOddsBoostEnabled();
    expect(coreToolsService.getOwnDeepProperty).toHaveBeenCalledWith(
      cmsService.initialData, 'oddsBoost.enabled'
    );
  });

  it('isOddsBoostBetslipHeaderAvailable', () => {
    userService.status = true;
    service.isOddsBoostEnabled = () => true;
    service['hasSelectionsWithBoost'] = () => true;
    expect(service.isOddsBoostBetslipHeaderAvailable()).toBeTruthy();

    userService.status = false;
    service.isOddsBoostEnabled = () => true;
    service['hasSelectionsWithBoost'] = () => true;
    expect(service.isOddsBoostBetslipHeaderAvailable()).toBeFalsy();

    userService.status = true;
    service.isOddsBoostEnabled = () => false;
    service['hasSelectionsWithBoost'] = () => true;
    expect(service.isOddsBoostBetslipHeaderAvailable()).toBeFalsy();

    userService.status = true;
    service.isOddsBoostEnabled = () => true;
    service['hasSelectionsWithBoost'] = () => false;
    expect(service.isOddsBoostBetslipHeaderAvailable()).toBeFalsy();
  });

  it('setMaxBoostValue', () => {
    service.setMaxBoostValue('10');
    expect(OddsBoostService.maxBoostValue).toBe('10');
  });

  it('hasSelectionsWithBoost', () => {
    betslipDataService.bets = [];
    expect(service.hasSelectionsWithBoost()).toBeFalsy();

    betslipDataService.bets = [{ info: () => ({}) }];
    expect(service.hasSelectionsWithBoost()).toBeFalsy();

    betslipDataService.bets = [{
      oddsBoost: ['1'],
      info: () => ({ disabled: true })
    }];
    expect(service.hasSelectionsWithBoost()).toBeFalsy();

    betslipDataService.bets = [{
      oddsBoost: ['1'],
      info: () => ({ disabled: false })
    }];
    expect(service.hasSelectionsWithBoost()).toBeTruthy();
  });

  it('canBoostSelections', () => {
    service.hasSelectionsWithBoost = () => false;
    betslipDataService.bets = [];
    expect(service.canBoostSelections()).toBeFalsy();

    service.hasSelectionsWithBoost = () => true;
    betslipDataService.bets = [{
      info: () => ({
        isSPLP: true,
        pricesAvailable: true
      }),
      price: { type: 'SP' }
    }];
    expect(service.canBoostSelections()).toBeFalsy();

    service.hasSelectionsWithBoost = () => true;
    betslipDataService.bets = [{
      info: () => ({
        isSPLP: true,
        pricesAvailable: false
      }),
      price: { type: 'SP' }
    }];
    expect(service.canBoostSelections()).toBeTruthy();

    service.hasSelectionsWithBoost = () => true;
    betslipDataService.bets = [{
      info: () => ({
        isSPLP: true,
        pricesAvailable: false
      }),
      price: { type: 'LP' }
    }];
    expect(service.canBoostSelections()).toBeTruthy();
  });

  it('hasSelectionsWithFreeBet', () => {
    betslipDataService.bets = [];
    expect(service.hasSelectionsWithFreeBet()).toBeFalsy();

    betslipDataService.bets = [{}];
    expect(service.hasSelectionsWithFreeBet()).toBeFalsy();

    betslipDataService.bets = [{ freeBet: { id: 1 }}];
    expect(service.hasSelectionsWithFreeBet()).toBeTruthy();
  });

  it('getOddsBoostTokens', fakeAsync(() => {
    coreToolsService.getOwnDeepProperty.and.returnValue([{}] as any);
    service.getOddsBoostTokens().subscribe();
    tick();
    expect(bppService.send).toHaveBeenCalledWith('accountOddsBoost', 'BETBOOST');
    expect(coreToolsService.getOwnDeepProperty).toHaveBeenCalledWith(
      jasmine.any(Object), 'response.model.freebetToken', []
    );

    expect(service['boostTokens']).toEqual([{}] as any);
    expect(freeBetsBadgeLoader.addOddsBoostCounter).toHaveBeenCalled();
  }));

  it('getOddsBoostTokens should call different method on page refresh', () => {
    service.getOddsBoostTokens(true).subscribe(() => {
      expect(bppService.send).toHaveBeenCalledWith('allAccountFreebets', 'BETBOOST');
    });
  });

  it('should not call bpp service in case if user is in-shop in getOddsBoostTokens', fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');
    const errorHandler = jasmine.createSpy('errorHandler');

    userService.isInShopUser.and.returnValue(true);
    service.getOddsBoostTokens().subscribe(successHandler, errorHandler);
    tick();
    expect(successHandler).toHaveBeenCalledWith([]);
    expect(errorHandler).not.toHaveBeenCalled();
  }));

  it('settleOddsBoostTokens', fakeAsync(() => {
    const betObj = { params: { }};
    service['sortBetTokens'] = jasmine.createSpy('sortBetTokens');
    service['removeIneligibleBoosts'] = jasmine.createSpy('removeIneligibleBoosts');

    service.settleOddsBoostTokens([betObj] as any).subscribe((res) => {
      expect(res[0]).toEqual(betObj as any);
      expect(service['sortBetTokens']).toHaveBeenCalledWith(betObj as any);
      expect(service['removeIneligibleBoosts']).toHaveBeenCalled();
    });
    tick();
  }));

  it('removeIneligibleBoosts acca betType case', () => {
    const bets = [
      { type: 'SGL', oddsBoost: {}},
      { type: 'DBL',
        lines: 1,
        oddsBoost: {
          sorting: {
            type: 'DBL'
          }
        }
      }
    ] as any;

    service['removeIneligibleBoosts'](bets);
    expect(bets[0].oddsBoost).toBe(null);
  });

  it('removeIneligibleBoosts different tokens case', () => {
    service['removeDifferentTokens'] = jasmine.createSpy();
    const bets = [
      { type: 'SGL', oddsBoost: { id: 123 }},
      { type: 'SGL', oddsBoost: { id: 234 }},
      { type: 'DBL', lines: 1, oddsBoost: { id: 321, sorting: { type: 'ANY'}}}
    ] as any;

    service['removeIneligibleBoosts'](bets);
    expect(service['removeDifferentTokens']).toHaveBeenCalledWith(bets);
  });

  it('removeIneligibleBoosts different tokens case no acca', () => {
    service['removeDifferentTokens'] = jasmine.createSpy();

    const bets = [
      { type: 'SGL', oddsBoost: { id: 123 }},
      { type: 'SGL', oddsBoost: { id: 234 }},
      { type: 'DBL', oddsBoost: { id: 321, sorting: { type: 'ANY'}}}
    ] as any;

    service['removeIneligibleBoosts'](bets);
    bets.pop();
    expect(service['removeDifferentTokens']).toHaveBeenCalledWith(bets);
  });

  it('removeDifferentTokens', () => {
    service['sortingFlow'] = jasmine.createSpy('sortingFlow');
    const bets = [
      { type: 'SGL', oddsBoost: { id: '123' }},
      { type: 'DBL', oddsBoost: { id: '321', sorting: { type: 'ANY'}}}
    ] as any;

    service['removeDifferentTokens'](bets);

    expect(service['sortingFlow']).toHaveBeenCalledWith([{ id: '123' } as any, { id: '321', sorting: { type: 'ANY'}}]);
    expect(bets[0].oddsBoost).toEqual({ id: '123' });
    expect(bets[1].oddsBoost).toEqual(null);
  });

  it('getBetLevel', () => {
    expect(service['getBetLevel']({ tokenPossibleBets: [{ betLevel: '123' }]} as any)).toEqual('123');
    expect(service['getBetLevel']([] as any)).toEqual('');
    expect(service['getBetLevel']([{}] as any)).toEqual('');
  });

  it('sortPageTokens case #1', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort').and.returnValue(null);
    service['betNameSort'] = jasmine.createSpy('betNameSort');

    service['sortPageTokens'](arr);

    expect(service['betNameSort']).toHaveBeenCalled();
  });

  it('sortPageTokens case #2', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betLevelSort').and.returnValue(null);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort').and.returnValue(arr);
    service['betNameSort'] = jasmine.createSpy('betNameSort');

    service['sortPageTokens'](arr);

    expect(service['betExpirySort']).toHaveBeenCalled();
    expect(service['betNameSort']).not.toHaveBeenCalled();
  });

  it('sortPageTokens case #3', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betTypeSort').and.returnValue(arr);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort');


    service['sortPageTokens'](arr);

    expect(service['betLevelSort']).toHaveBeenCalled();
    expect(service['betExpirySort']).not.toHaveBeenCalled();
  });

  it('sortPageTokens case #4', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(arr);
    service['betLevelSort'] = jasmine.createSpy('betLevelSort');


    service['sortPageTokens'](arr);

    expect(service['betTypeSort']).toHaveBeenCalled();
    expect(service['betLevelSort']).not.toHaveBeenCalled();
  });

  it('sortBetTokens', () => {
    const bet = {
      params: {
        oddsBoosts: [{
          id: 123,
          tokenPossibleBets: [{
            betLevel: 'ANY'
          }],
          freebetOfferType: 'ANY'
        }],
        oddsBoost: null
      }
    } as any;

    service['sortingFlow'] = jasmine.createSpy('sortingFlow').and.returnValue([{
      id: 123
    }]);
    service['sortBetTokens'](bet);

    const extendedToken = {
      id: 123,
      tokenPossibleBets: [{
        betLevel: 'ANY'
      }],
      freebetOfferType: 'ANY',
      sorting: { level: 'ANY', type: 'ANY' }
    };

    expect(service['sortingFlow']).toHaveBeenCalledWith([extendedToken as any]);
    expect(bet.oddsBoost).toEqual(extendedToken);
  });

  it('sortBetTokens no oddsBoosts', () => {
    const bet = {
      params: {}
    } as any;

    service['sortingFlow'] = jasmine.createSpy('sortingFlow');

    service['sortBetTokens'](bet);
    expect(service['sortingFlow']).toHaveBeenCalledWith([]);
  });

  it('sortBetTokens no freebet tokens', () => {
    const bet = {
      params: {
        oddsBoosts: [{ id: 123 }],
        oddsBoost: null
      }
    } as any;

    service['sortingFlow'] = jasmine.createSpy('sortingFlow');
    service['sortBetTokens'](bet);

    expect(service['sortingFlow']).toHaveBeenCalledWith([{
      id: 123,
      sorting: {}
    } as any]);
  });


  it('sortingFlow case #1', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort').and.returnValue(null);
    service['betNameSort'] = jasmine.createSpy('betNameSort');

    service['sortingFlow'](arr);

    expect(service['betNameSort']).toHaveBeenCalled();
  });

  it('sortingFlow case #2', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betLevelSort').and.returnValue(null);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort').and.returnValue(arr);
    service['betNameSort'] = jasmine.createSpy('betNameSort');

    service['sortingFlow'](arr);

    expect(service['betExpirySort']).toHaveBeenCalled();
    expect(service['betNameSort']).not.toHaveBeenCalled();
  });

  it('sortingFlow case #3', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(null);
    service['betLevelSort'] = jasmine.createSpy('betTypeSort').and.returnValue(arr);
    service['betExpirySort'] = jasmine.createSpy('betExpirySort');


    service['sortingFlow'](arr);

    expect(service['betLevelSort']).toHaveBeenCalled();
    expect(service['betExpirySort']).not.toHaveBeenCalled();
  });

  it('sortingFlow case #4', () => {
    const arr = [{ sorting: {} }, { sorting: {} }] as any;
    service['betTypeSort'] = jasmine.createSpy('betTypeSort').and.returnValue(arr);
    service['betLevelSort'] = jasmine.createSpy('betLevelSort');


    service['sortingFlow'](arr);

    expect(service['betTypeSort']).toHaveBeenCalled();
    expect(service['betLevelSort']).not.toHaveBeenCalled();
  });

  it('betTypeSort', () => {
    expect(service['betTypeSort']('ANY', 'SGL')).toBe(0);
    expect(service['betTypeSort']('DBL', 'SGL')).toBe(-1);
    expect(service['betTypeSort']('', 'TBL')).toBe(1);
  });

  it('betLevelSort', () => {
    expect(service['betLevelSort']('ANY', 'SELECTION')).toBe(1);
    expect(service['betLevelSort']('SELECTION', 'CLASS')).toBe(-1);
    expect(service['betLevelSort']('CATEGORY', 'CATEGORY')).toBe(0);
  });

  it('betExpirySort', () => {
    expect(service['betExpirySort']('2018-12-31T12:56:08.000Z', '2018-12-15T12:56:08.000Z')).toBe(1);
    expect(service['betExpirySort']('2018-12-15T12:56:08.000Z', '2018-12-31T12:56:08.000Z')).toBe(-1);
    expect(service['betExpirySort']('2018-12-31T12:56:08.000Z', '2018-12-31T12:56:08.000Z')).toBe(0);
  });

  it('betNameSort', () => {
    expect(service['betNameSort']('ATEST', 'bTEST')).toBe(-1);
    expect(service['betNameSort']('BTEST', 'aTEST')).toBe(1);
  });

  it('betTypeIndex', () => {
    expect(service['betTypeIndex']('')).toBe(1);
    expect(service['betTypeIndex']('ANY')).toBe(1);
    expect(service['betTypeIndex']('SGL')).toBe(1);
    expect(service['betTypeIndex']('DBL')).toBe(2);
    expect(service['betTypeIndex']('TBL')).toBe(3);
    expect(service['betTypeIndex']('ACC8')).toBe(8);
    expect(service['betTypeIndex']('TEST')).toBe(1);
  });

  it('storeTokens', () => {
    const tokens: any[] = [{}];
    service.storeTokens(tokens);
    expect(service.tokens).toBe(service['boostTokens']);
    expect(storageService.set).toHaveBeenCalledWith(
      `oddsBoostTokens-${userService.username}`, tokens
    );
  });

  it('getStorageTokens', () => {
    service.getStorageTokens();
    expect(storageService.get).toHaveBeenCalledWith(`oddsBoostTokens-${userService.username}`);
  });

  it('isNewTokensAvailable', () => {
    expect(
      service.isNewTokensAvailable([], [])
    ).toBeFalsy();

    expect(
      service.isNewTokensAvailable(
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }] as any[], []
      )
    ).toBeTruthy();

    expect(
      service.isNewTokensAvailable(
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }] as any[],
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }] as any[]
      )
    ).toBeFalsy();

    expect(
      service.isNewTokensAvailable(
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }, { freebetTokenId: '3'}] as any[],
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }] as any[]
      )
    ).toBeTruthy();

    expect(
      service.isNewTokensAvailable(
        [{ freebetTokenId: '1' }, { freebetTokenId: '1a'}, { freebetTokenId: '2' }] as any[],
        [{ freebetTokenId: '1' }, { freebetTokenId: '2' }] as any[]
      )
    ).toBeTruthy();
  });

  it('showOddsBoostSpDialog', () => {
    service.showOddsBoostSpDialog();
    expect(localeService.getString).toHaveBeenCalledWith('oddsboost.spDialog.title');
    expect(localeService.getString).toHaveBeenCalledWith('oddsboost.spDialog.text');
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.ODDS_BOOST_CHANGE, false);
  });

  it('showOddsBoostFreeBetDialog (boost active)', () => {
    const betslipDialog = {
      noThanks: 'No, thanks',
      yesPlease: 'Yes, please',
      okThanks: 'Ok, thanks',
      continueWith: 'WANT TO CONTINUE?',
      cancelBoostPriceMessage: 'Selecting a free bet or bet token will cancel your boosted price, are you sure you want to continue',
      cantBoostMessage: 'Unfortunately you can’t boost your odds while using a free bet or bet token. Please de-select your free bet to boost your odds'
    };
    service.showOddsBoostFreeBetDialog(true, 'betslip');
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.continueWith);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.cancelBoostPriceMessage);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.noThanks);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.yesPlease);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'informationDialog', jasmine.any(Function), true, jasmine.any(Object)
    );
  });

  it('showOddsBoostFreeBetDialog (boost inactive)', () => {
    const betslipDialog = {
      noThanks: 'No, thanks',
      yesPlease: 'Yes, please',
      okThanks: 'Ok, thanks',
      continueWith: 'WANT TO CONTINUE?',
      cancelBoostPriceMessage: 'Selecting a free bet or bet token will cancel your boosted price, are you sure you want to continue',
      cantBoostMessage: 'Unfortunately you can’t boost your odds while using a free bet or bet token. Please de-select your free bet to boost your odds'
    };
    service.showOddsBoostFreeBetDialog(false, 'betslip');
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.continueWith);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.cantBoostMessage);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.okThanks);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'informationDialog', jasmine.any(Function), true, jasmine.any(Object)
    );
  });

  it('showOddsBoostFreeBetDialog (boost active, type quickbet)', () => {
    const betslipDialog = {
      noThanks: 'No, thanks',
      yesPlease: 'Yes, please',
      okThanks: 'Ok, thanks',
      continueWith: 'WANT TO CONTINUE?',
      cancelBoostPriceMessage: 'Selecting a free bet or bet token will cancel your boosted price, are you sure you want to continue',
      cantBoostMessage: 'Unfortunately you can’t boost your odds while using a free bet or bet token. Please de-select your free bet to boost your odds'
    };
    service.showOddsBoostFreeBetDialog(true, 'quickbet');
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.continueWith);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.cancelBoostPriceMessage);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.noThanks);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.yesPlease);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'informationDialog', jasmine.any(Function), true, jasmine.any(Object)
    );
  });

  it('showOddsBoostFreeBetDialog (boost inactive, type quickbet)', () => {
    const betslipDialog = {
      noThanks: 'No, thanks',
      yesPlease: 'Yes, please',
      okThanks: 'Ok, thanks',
      continueWith: 'WANT TO CONTINUE?',
      cancelBoostPriceMessage: 'Selecting a free bet or bet token will cancel your boosted price, are you sure you want to continue',
      cantBoostMessage: 'Unfortunately you can’t boost your odds while using a free bet or bet token. Please de-select your free bet to boost your odds'
    };
    service.showOddsBoostFreeBetDialog(false, 'quickbet');
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.continueWith);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.cantBoostMessage);
    expect(localeService.getString).toHaveBeenCalledWith(betslipDialog.okThanks);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'informationDialog', jasmine.any(Function), true, jasmine.any(Object)
    );
  });

  it('should storeTokens after page refresh on event STORE_ODDS_BOOST', fakeAsync(() => {
    const tokens: any[] = [{}];

    storeOddsBoostCallback(tokens);
    tick();

    expect(storageService.set).toHaveBeenCalled();
    expect(service['boostTokens']).toEqual(tokens);
  }));

  it('subscribeToEvents', () => {
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OddsBoostService', 'ODDS_BOOST_CHANGE', jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OddsBoostService', 'ODDS_BOOST_HANDLE_SP', jasmine.any(Function)
    );
  });

  it('getBoostActiveFromStorage', () => {
    service['getBoostActiveFromStorage']();
    expect(storageService.get).toHaveBeenCalledWith('oddsBoostActive');
  });

  it('getOldPriceFromBetslipStake', () => {
    service['convertPotentialPayoutToPrice'] = jasmine.createSpy().and.returnValue(123);

    const stake: any = {
      price: {
        priceDec: 10,
        priceNum: 3,
        priceDen: 4
      },
      potentialPayout: 11.2
    };

    expect(service.getOldPriceFromBetslipStake(stake, 'single')).toEqual({
      decimal: stake.price.priceDec,
      num: stake.price.priceNum,
      den: stake.price.priceDen
    });

    expect(service.getOldPriceFromBetslipStake(stake, 'multiple')).toEqual(123 as any);
    expect(service.getOldPriceFromBetslipStake(stake, 'acca')).toEqual(123 as any);
    expect(service.getOldPriceFromBetslipStake(stake, 'test')).toEqual(undefined);
  });

  it('getNewPriceFromBetslipStake', () => {
    service['convertPotentialPayoutToPrice'] = jasmine.createSpy().and.returnValue(123);

    const stake: any = {
      Bet: {
        oddsBoost: {
          enhancedOddsPrice: 5.6,
          enhancedOddsPriceNum: 3,
          enhancedOddsPriceDen: 2
        }
      }
    };

    expect(service.getNewPriceFromBetslipStake(stake, 'single')).toEqual({
      decimal: stake.Bet.oddsBoost.enhancedOddsPrice,
      num: stake.Bet.oddsBoost.enhancedOddsPriceNum,
      den: stake.Bet.oddsBoost.enhancedOddsPriceDen
    });

    expect(service.getNewPriceFromBetslipStake(stake, 'multiple')).toEqual(123 as any);
    expect(service.getNewPriceFromBetslipStake(stake, 'acca')).toEqual(123 as any);
    expect(service.getNewPriceFromBetslipStake(stake, 'test')).toEqual(undefined);
  });

  it('getOldPriceFromQuickBet', () => {
    const selection: any = {
      price: {
        priceDec: 10,
        priceNum: 3,
        priceDen: 4
      }
    };

    expect(service.getOldPriceFromQuickBet(selection)).toEqual({
      decimal: selection.price.priceDec,
      num: selection.price.priceNum,
      den: selection.price.priceDen
    });
  });

  it('getNewPriceFromQuickBet', () => {
    const selection: any = {
      oddsBoost: {
        enhancedOddsPrice: 10,
        enhancedOddsPriceNum: 3,
        enhancedOddsPriceDen: 4
      }
    };

    expect(service.getNewPriceFromQuickBet(selection)).toEqual({
      decimal: selection.oddsBoost.enhancedOddsPrice,
      num: selection.oddsBoost.enhancedOddsPriceNum,
      den: selection.oddsBoost.enhancedOddsPriceDen
    });

    delete selection.oddsBoost;
    expect(service.getNewPriceFromQuickBet(selection)).toEqual({
      decimal: 0, num: 0, den: 0
    });
  });

  it('closeOddsBoostFreeBetDialog', () => {
    service['closeOddsBoostFreeBetDialog']('ok thanks', 'betslip');
    expect(dialogService.closeDialog).toHaveBeenCalledWith(
      dialogService.API.informationDialog
    );
  });

  it('closeOddsBoostFreeBetDialog', () => {
    service['closeOddsBoostFreeBetDialog']('ok thanks', 'quickbet');
    expect(dialogService.closeDialog).toHaveBeenCalledWith(
      dialogService.API.informationDialog
    );
  });

  it('continueWithOddsBoost', () => {
    service['doNotUnsetFreeBets'] = false;
    service['continueWithOddsBoost']();
    expect(pubSubService.publish).toHaveBeenCalledWith('ODDS_BOOST_UNSET_FREEBETS');

    service['doNotUnsetFreeBets'] = true;
    service['continueWithOddsBoost']();
    expect(service['doNotUnsetFreeBets']).toBeFalsy();
  });

  it('continueWithFreeBet', () => {
    service['closeOddsBoostFreeBetDialog'] = jasmine.createSpy();

    service['continueWithFreeBet']('Ok thanks', 'click');

    expect(pubSubService.publish).toHaveBeenCalledWith('ODDS_BOOST_CHANGE', false);
    expect(service['doNotUnsetFreeBets']).toBeTruthy();
    expect(service['closeOddsBoostFreeBetDialog']).toHaveBeenCalled();
  });

  it('convertPotentialPayoutToPrice', () => {
    userService.oddsFormat = 'dec';
    expect(service['convertPotentialPayoutToPrice'](2.5178)).toEqual({
      decimal: '2.52'
    });

    userService.oddsFormat = 'frac';
    expect(service['convertPotentialPayoutToPrice'](2.5678)).toEqual({
      num: '1.56', den: '1'
    });
  });

  it('getOddsBoostTokensCount', () => {
    service.getOddsBoostTokensCount().subscribe((count: number) => {
      expect(count).toBe(0);
    });
  });

  it('getOddsBoostTokensCount', () => {
    service.getOddsBoostTokens = jasmine.createSpy().and.returnValue(observableOf([1, 2, 3]));
    service.getOddsBoostTokensCount().subscribe((count: number) => {
      expect(count).toBe(3);
    });
  });

  it('should update stored oddsBoostActive value', () => {
    changeCallback(false);
    expect(storageService.set).toHaveBeenCalledWith('oddsBoostActive', false);
  });

  describe('ODDS_BOOST_HANDLE_SP', () => {
    beforeEach(() => {
      service['showOddsBoostSpDialog'] = jasmine.createSpy('showOddsBoostSpDialog');
    });

    it('case#1', () => {
      service['isOddsBoostEnabled'] = jasmine.createSpy('isOddsBoostEnabled').and.returnValue(true);
      service['isBoostActive'] = jasmine.createSpy('isBoostActive').and.returnValue(true);
      spCallback();
      expect(service['showOddsBoostSpDialog']).toHaveBeenCalled();
    });

    it('case#2', () => {
      service['isOddsBoostEnabled'] = jasmine.createSpy('isOddsBoostEnabled').and.returnValue(true);
      service['isBoostActive'] = jasmine.createSpy('isBoostActive').and.returnValue(false);
      spCallback();
      expect(service['showOddsBoostSpDialog']).not.toHaveBeenCalled();
    });

    it('case#3', () => {
      service['isOddsBoostEnabled'] = jasmine.createSpy('isOddsBoostEnabled').and.returnValue(false);
      spCallback();
      expect(service['showOddsBoostSpDialog']).not.toHaveBeenCalled();
    });
  });

  describe('checkBetslipSelections', () => {
    it('should disable odds boost if cannot boost selections', () => {
      betslipDataService.bets = [{}];
      coreToolsService.getOwnDeepProperty.and.returnValue(true);
      service['boostActive'] = true;
      service['checkBetslipSelections']();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.ODDS_BOOST_CHANGE, false);
    });

    it('should not disable odds boost #1', () => {
      betslipDataService.bets = [];
      service['checkBetslipSelections']();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not disable odds boost #2', () => {
      betslipDataService.bets = [{}];
      coreToolsService.getOwnDeepProperty.and.returnValue(false);
      service['checkBetslipSelections']();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not disable odds boost #3', () => {
      betslipDataService.bets = [{
        oddsBoost: {}, info: () => ({})
      }];
      coreToolsService.getOwnDeepProperty.and.returnValue(true);
      service['boostActive'] = true;
      service['checkBetslipSelections']();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('should check if max stake exceeded', () => {
    OddsBoostService.maxBoostValue = '100';
    expect(service.isMaxStakeExceeded(300)).toBeTruthy();
    OddsBoostService.maxBoostValue = '100';
    expect(service.isMaxStakeExceeded(50)).toBeFalsy();
  });

  it('should send event to gtm (toogle on)', () => {
    service.sendEventToGTM('quickbet', true);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quickbet',
      eventAction: 'odds boost',
      eventLabel: 'toggle on'
    });
  });

  it('should send event to gtm (toogle off)', () => {
    service.sendEventToGTM('quickbet', false);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quickbet',
      eventAction: 'odds boost',
      eventLabel: 'toggle off'
    });
  });

  it('should send event to gtm on button click event', () => {
    boostSendGtmCallback({ origin: 'betslip', state: true });
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      event: 'trackEvent',
      eventCategory: 'betslip',
      eventAction: 'odds boost',
      eventLabel: 'toggle on'
    }));
  });
  describe('@updateOddsBoostCount', () => {
    const boosts = [1, 2];
    it('should update odds boost count if user is logged in', fakeAsync(() => {
      coreToolsService.getOwnDeepProperty.and.returnValue(boosts);
      userService.status = true;
      service.oddsBoostsCountListener.subscribe(expectedValue => {
        expect(expectedValue).toEqual(2);
      });
      service['updateOddsBoostCount']();
      tick();
    }));

    it('should not update odds boost count if user is not logged in', fakeAsync(() => {
      coreToolsService.getOwnDeepProperty.and.returnValue(boosts);
      userService.status = false;
      service.oddsBoostsCountListener.subscribe(expectedValue => {
        expect(expectedValue).toBeUndefined();
      });
      service['updateOddsBoostCount']();
      tick();
    }));
  });

  describe('useDailyBoost', () => {
    it('no daily boosts', () => {
      const bets: any = [{
        oddsBoost: null,
        params: {
          oddsBoosts: [
            {},
            {
              freebetOfferType: 'DBL'
            },
            {
              tokenPossibleBets: [{ betLevel: 'CATEGORY' }]
            }
          ]
        }
      }];

      service['useDailyBoost'](bets);
      expect(bets[0].oddsBoost).toBe(null);
    });

    it('don\'t use daily boost if Acca token selected', () => {
      const bets: any = [{
        oddsBoost: null
      }, {
        oddsBoost: {
          sorting: { type: 'DBL' },
        },
        params: {
          oddsBoosts: [
            {
              tokenPossibleBets: [{ betLevel: 'ANY' }]
            }
          ]
        }
      }];

      service['useDailyBoost'](bets);
      expect(bets[0].oddsBoost).toBe(null);
    });

    it('don\'t use daily boost if all bets boosted', () => {
      const bets: any = [
        {
          params: {
            oddsBoosts: [{
              tokenPossibleBets: [{ betLevel: 'ANY' }]
            }]
          },
          oddsBoost: { id: '1', sorting: {} }
        },
        { disabled: true },
        { params: {} }
      ];

      service['useDailyBoost'](bets);
      expect(bets[0].oddsBoost.id).toEqual('1');
    });

    it('use daily boost', () => {
      const bets: any = [{
        params: {
          oddsBoosts: [{
            id: '1',
            expiry: '2019-09-09 11:30:00',
            tokenPossibleBets: [{ betLevel: 'ANY' }]
          }, {
            id: '2',
            expiry: '2019-09-09 11:00:00',
            tokenPossibleBets: [{ betLevel: 'ANY' }]
          }]
        }
      }];

      service['useDailyBoost'](bets);
      expect(bets[0].oddsBoost).toEqual(bets[0].params.oddsBoosts[1]);
    });

    it('keep popup hidden - in keep popup timespan', () => {
      const thirtyDaysBeforeToday = new Date(Date.now() - 1000 * 60 * 60 * 24 * 30);
      cmsService.initialData.oddsBoost.allowUserToToggleVisibility = true;
      cmsService.initialData.oddsBoost.daysToKeepPopupHidden = 60;

      const storageData = {};
      storageData[`setDate-${userService.username}`] = thirtyDaysBeforeToday;
      storageService.get = jasmine.createSpy('get').and.returnValue(storageData);
      expect(service['keepPopupHidden']()).toEqual(true);
    });

    it('keep popup hidden - after keep popup timespan', () => {
      const sixtyOneDaysBeforeToday = new Date(Date.now() - 1000 * 60 * 60 * 24 * 61);
      cmsService.initialData.oddsBoost.allowUserToToggleVisibility = true;
      cmsService.initialData.oddsBoost.daysToKeepPopupHidden = 60;

      storageService.get = jasmine.createSpy('get').and.returnValue(sixtyOneDaysBeforeToday);
      expect(service['keepPopupHidden']()).toEqual(false);
    });

    it('keep popup hidden - no toggle time set', () => {
      cmsService.initialData.oddsBoost.allowUserToToggleVisibility = true;
      cmsService.initialData.oddsBoost.daysToKeepPopupHidden = 60;

      storageService.get = jasmine.createSpy('get').and.returnValue(null);
      expect(service['keepPopupHidden']()).toEqual(false);
    });

    it('keep popup hidden - user not allowed to toggle', () => {
      cmsService.initialData.oddsBoost.allowUserToToggleVisibility = false;
      cmsService.initialData.oddsBoost.daysToKeepPopupHidden = 60;

      expect(service['keepPopupHidden']()).toEqual(false);
    });
  });

  it('should send GTM data', () => {
    service.sendGTM('quickbet', 'Ok thanks', 'click', 'trackEvent');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      'event': 'Event.Tracking',
      'component.CategoryEvent': 'bets boost',
      'component.LabelEvent': 'free bet alert',
      'component.ActionEvent': 'click',  
      'component.PositionEvent': 'quickbet',
      'component.LocationEvent': 'free bet alert',
      'component.EventDetails': 'Ok thanks',
      'component.URLClicked': 'not applicable'
    });
  });
});
