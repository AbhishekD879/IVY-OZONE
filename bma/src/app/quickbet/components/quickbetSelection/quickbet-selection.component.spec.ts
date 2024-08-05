import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf, of } from 'rxjs';
import { commandApi } from '@app/core/services/communication/command/command-api.constant';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { QuickbetSelectionComponent } from './quickbet-selection.component';
import { SELECTED_CONTEST_CHANGE } from '@app/fiveASideShowDown/constants/constants';
import { extraPlaceData, extraPlaceSelection, selection } from '@app/quickbet/components/quickbetSelection/mockData/quickbet-selection.mock';

describe('QuickbetSelectionComponent', () => {
  let pubSubService;
  let userService;
  let localeService;
  let filtersService;
  let quickbetDepositService;
  let quickbetService;
  let quickbetUpdateService;
  let freeBetsService;
  let quickbetNotificationService;
  let commandService;
  let cmsService;
  let component: QuickbetSelectionComponent;
  let loginCb;
  let gtmService;
  let windowRef;
  let cdr;
  let timeService;
  let bppProviderService;
  let fiveASideContestSelectionService;
  let serviceClosureService;
  let sessionStorageService;
  let bonusSuppressionService;
  let storageService;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'SET_ODDS_FORMAT') {
            callback('frac');
          } else if (method === 'SUCCESSFUL_LOGIN') {
            loginCb = callback;
          }  else if (method === 'ODDS_BOOST_CHANGE') {
            callback(true);
          } else if (method === 'QUICKBET_OPENED') {
            callback({
              freebet: {
                name: 'freebet'
              }
            });
          }  else if (method === 'QUICKBET_COUNTDOWN_TIMER') {
            timeService = callback;
          } else if (method === 'EACHWAY_FLAG_UPDATED') {
            callback('N');
          } else {
            callback();
          }
      }),
      unsubscribe: jasmine.createSpy()
    };
    timeService = jasmine.createSpyObj(['countDownTimer']);
    userService = {
      status: true,
      currencySymbol: '$',
      isInShopUser: jasmine.createSpy('isInShopUser'),
      username:'test'
    };
    localeService = {
      getString: jasmine.createSpy().and.returnValue('test_str')
    };
    filtersService = {
      getComplexTranslation: jasmine.createSpy().and.returnValue(jasmine.any(String)),
      filterPlayerName: jasmine.createSpy('filterPlayerName'),
      filterAddScore: jasmine.createSpy('filterAddScore'),
      setCurrency: jasmine.createSpy('setCurrency')
    };
    quickbetDepositService = {
      update: jasmine.createSpy()
    };
    quickbetService = {
      saveQBStateInStorage: jasmine.createSpy()
    };
    quickbetUpdateService = {
      fillDisableMap: jasmine.createSpy(),
      isHandicapChanged: jasmine.createSpy('isHandicapChanged')
    };
    freeBetsService = {
      getFreeBetsState: jasmine.createSpy('getFreeBetsState').and.returnValue({
        data: [{ freebetTokenValue: '14', tokenPossibleBets: [] , freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1"}],
        betTokens: [{ freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
        fanZone: [{freebetTokenId: 78, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }, { freebetTokenId: 99 , freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
        available: true
      }),
      groupByName: jasmine.createSpy('groupByName').and.returnValue(of({})),
      isBetPack:jasmine.createSpy('isBetPack').and.returnValue(false),
      isFanzone:jasmine.createSpy('isFanzone').and.returnValue(false),
    };
    quickbetNotificationService = {
      saveErrorMessage: jasmine.createSpy()
    };
    commandService = {
      API: commandApi,
      execute: jasmine.createSpy(),
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(() => observableOf({}))
    };
    cmsService = {
      getOddsBoost: jasmine.createSpy().and.returnValue(observableOf({})),
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(
        {
          maxPayOut: {
            maxPayoutFlag: true, maxPayoutMsg: 'returns capped.',
            link: 'https://qa2.sports.ladbrokes.com/', click: 'click'
          },
          FreeBets: {
            header: 'FB Available',
            description: 'Fb default desc',
            boostEnabled: 'Fb desc when boost available',
            boostActive: 'Fb desc when boost selected'
          },
          eachWayTooltip: {
            Delay: 1000,
            Message: 'Back your selection to win or place. Please note: This doubles your stake.',
            Enable: true
          }
        })
      )
    };
    fiveASideContestSelectionService = {
      defaultContestId: null
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    cdr = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    bppProviderService = {
      quickBet: jasmine.createSpy('quickBet').and.returnValue(of({ bets: [{ maxPayout: '200' ,
      freebet:[{
        "id": "177568097",
        "offerName": "Any Sports Free Bet",
        "value": "0.10",
        "expiry": "2023-06-19T10:04:06.000Z",
        "type": "SPORTS1",
        "freebetOfferType": "",
        "tokenPossibleBets": [
            {
                "name": "Football Any",
                "betLevel": "CATEGORY",
                "betType": "",
                "betId": "16"
            }
        ]
    },
    {
      "id": "177568094",
      "offerName": "Any Sports Free Bet1",
      "value": "0.10",
      "expiry": "2023-06-19T10:04:06.000Z",
      "type": "SPORTS",
      "freebetOfferType": "",
      "tokenPossibleBets": [
          {
              "name": "Football Any",
              "betLevel": "CATEGORY",
              "betType": "",
              "betId": "16"
          }
      ]
  }
]
  }],
  outcomeDetails:[{eachWayPlaces:'4',previousOfferedPlaces:'3'}] }))
    };
    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };

    sessionStorageService = {
      get: jasmine.createSpy('get')
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    }

    component = new QuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
      quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
      cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService, storageService, bonusSuppressionService);
  });

  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      component.selection = {
        eventId: 345,
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: false,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234',
        categoryName: 'HORSE_RACING',
        categoryId: '21'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      loginCb('quickbet');

      expect(component['formBodyParamforBuildBet']).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
          'QuickbetSelectionController',
          pubSubService.API.SUCCESSFUL_LOGIN,
          jasmine.any(Function)
      );
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetSelectionController',
        pubSubService.API.QUICKBET_OPENED,
        jasmine.any(Function)
      );
      expect(pubSubService.subscribe).toHaveBeenCalledWith(345, 'SET_ODDS_FORMAT', jasmine.any(Function));
      expect(component['getFreebetsList']).toHaveBeenCalledTimes(2);
      expect(quickbetUpdateService.fillDisableMap).toHaveBeenCalledWith(jasmine.any(Object));
      expect(filtersService.getComplexTranslation).toHaveBeenCalledWith(
        'quickbet.singleDisabled',
        '%1',
        undefined
      );
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(
        jasmine.any(String),
        'warning',
        'bet-status'
      );
      expect(component['onFreebetChange']).toHaveBeenCalledWith({
        output: 'selectedChange', value: {
          name: 'freebet'
        } });
      expect(quickbetDepositService.update)
        .toHaveBeenCalledWith(component.selection.stake, component.selection.isEachWay);
    });

    it('should call addEventListeners method', () => {
      component.selection = {
        eventId: 345,
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();

      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledTimes(2);
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('online', jasmine.any(Function));
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('offline', jasmine.any(Function));
    });

    it('should call addEventListeners method', () => {
      component.selection = {
        eventId: 345,
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy();      
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();

      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledTimes(2);
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('online', jasmine.any(Function));
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('offline', jasmine.any(Function));
    });

    it('ngOnInit with selection disabled', () => {
      component.selection = {
        disabled: false,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        hasSP: false,
        oddsBoost: {},
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component.isBoostEnabled = true;

      component['getFreebetsList'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      loginCb('quickbet');

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetSelectionController',
        pubSubApi.GET_QUICKBET_SELECTION_STATUS,
        jasmine.any(Function)
      );

      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
          'QuickbetSelectionController',
          pubSubService.API.SUCCESSFUL_LOGIN,
          jasmine.any(Function)
      );
      expect(component['getFreebetsList']).toHaveBeenCalledTimes(2);
      expect(component['initOddsBoost']).toHaveBeenCalledTimes(3);
      expect(quickbetUpdateService.fillDisableMap).toHaveBeenCalledWith({
        event: false,
        market: false,
        selection: false
      });
    });


    it('ngOnInit else cases', () => {
      component.selection = {
        eventStatusCode: 'S',
        isYourCallBet: false,
        disabled: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();
      cmsService = {
        getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(
          {
            maxPayOut: null
          })
        )
      };
      component.ngOnInit();

      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
          'QuickbetSelectionController',
          pubSubService.API.SUCCESSFUL_LOGIN,
          jasmine.any(Function)
      );
      expect(component['getFreebetsList']).toHaveBeenCalled();
      expect(quickbetUpdateService.fillDisableMap).toHaveBeenCalledWith({
        event: true,
        market: false,
        selection: false
      });
      expect(filtersService.getComplexTranslation).toHaveBeenCalledWith(
        'quickbet.singleDisabled', '%1', jasmine.any(String)
      );
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(
        jasmine.any(String),
        'warning',
        'bet-status'
      );
      expect(component['initOddsBoost']).toHaveBeenCalled();
    });

    it('ngOnInit without config Data', () => {
      cmsService = {
        getOddsBoost: jasmine.createSpy().and.returnValue(observableOf({})),
        getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(''))
      };
      component = new QuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
        quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
        cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService,storageService,
        bonusSuppressionService);
        component.selection = {
          eventStatusCode: 'S',
          isYourCallBet: false,
          disabled: true,
          price: {
            priceNum: 22,
            priceDen: 1,
            priceTypeRef: { id: '123' }
          },
          outcomeId: '1234',
          onStakeChange: jasmine.createSpy('onStakeChange')
        } as any;
        component.canBoostSelection=true;
        component.selectionAmountClasses={"dummy":true};
        component.isUserLoggedIn=true;
        component.disablePlaceBet = true;
        component.getPlaceBetText = "test";
      component.ngOnInit();
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalled();
    });
    
    it ('should reload freebets list on successful login', () => {
      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      spyOn<any>(component, 'getFreebetsList');
      component['onFreebetChange'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();

      component.ngOnInit();
      loginCb('test');

      expect(component['getFreebetsList']).toHaveBeenCalledTimes(2);
      expect(component['initOddsBoost']).toHaveBeenCalled();
    });

    it ('should reload showeach list on successful login', () => {
      pubSubService.subscribe.and.callFake((file, method, callback) => {
        if (method === 'SUCCESSFUL_LOGIN') {
          callback('test');
        }
      });
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['buildBetCall'] = jasmine.createSpy();
      spyOn<any>(component, 'getFreebetsList');
      component['onFreebetChange'] = jasmine.createSpy();
      component['initOddsBoost'] = jasmine.createSpy();
      component['showEachWay'] = jasmine.createSpy();

      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        isEachWayAvailable: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component.ngOnInit();
      expect(component['showEachWay']).toHaveBeenCalled();
    });

    it('ngOnInit (false)', () => {
      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy('getFreebetsList');
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      loginCb('test');

      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(component['getFreebetsList']).toHaveBeenCalledTimes(2);
      expect(quickbetUpdateService.fillDisableMap).toHaveBeenCalledWith(jasmine.any(Object));
      expect(filtersService.getComplexTranslation).toHaveBeenCalledWith(
        'quickbet.singleDisabled',
        '%1',
        'event'
      );
    });

    it('ngOnInit (false) (suspensionMap)', () => {
      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        marketStatusCode: 'S',
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy('getFreebetsList');
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      loginCb('test');

      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(component['getFreebetsList']).toHaveBeenCalledTimes(2);
      expect(quickbetUpdateService.fillDisableMap).toHaveBeenCalledWith({
        event: true,
        market: true,
        selection: false
      });
      expect(filtersService.getComplexTranslation).toHaveBeenCalledWith(
        'quickbet.singleDisabled',
        '%1',
        'selection'
      );
    });

    it('ngOnInit no freebets in selectionData', () => {
      pubSubService.subscribe.and.callFake((file, method, callback) => {
        if (method === 'SET_ODDS_FORMAT') {
          callback('frac');
        } else if (method === 'SUCCESSFUL_LOGIN') {
          loginCb = callback;
        } else if (method === 'QUICKBET_OPENED') {
          callback({});
        } else {
          callback();
        }
      });
      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        marketStatusCode: 'S',
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy('getFreebetsList');
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      expect(component['onFreebetChange']).not.toHaveBeenCalled();
    });

    it('ngOnInit no selectionData', () => {
      pubSubService.subscribe.and.callFake((file, method, callback) => {
          if (method === 'SET_ODDS_FORMAT') {
            callback('frac');
          } else if (method === 'SUCCESSFUL_LOGIN') {
            loginCb = callback;
          } else if (method === 'QUICKBET_OPENED') {
            callback(null);
          } else {
            callback();
          }
        });
      component.selection = {
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isYourCallBet: true,
        eventStatusCode: 'S',
        marketStatusCode: 'S',
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet'] = jasmine.createSpy().and.returnValue(component.body);
      component['getFreebetsList'] = jasmine.createSpy('getFreebetsList');
      component['initOddsBoost'] = jasmine.createSpy();
      component['onFreebetChange'] = jasmine.createSpy();

      component.ngOnInit();
      expect(component['onFreebetChange']).not.toHaveBeenCalled();
    });
  });

  it('get canBoostSelection', () => {
    component.isBoostEnabled = true;
    component.selection = {
      disabled: false,
      hasSP: false,
      oddsBoost: {}
    } as any;
    expect(component.canBoostSelection).toBeTruthy();
  });

  it('ngOnDestroy', () => {
    const notifyTimeout = 10;
    component.selection = { eventId: '1' } as any;
    component.countDownTimer = jasmine.createSpyObj(['stop']);
    component['freebetsSubscription']  =  <any>{unsubscribe: jasmine.createSpy('unsubscribe')};
    component['betPackSubscription']  =  <any>{unsubscribe: jasmine.createSpy('unsubscribe')};
    component['fanzoneSubscription']  =  <any>{unsubscribe: jasmine.createSpy('unsubscribe')};
    component['notifyTimeout'] = notifyTimeout;
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('QuickbetSelectionController');
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('1');
    expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledTimes(2);
    expect(component['freebetsSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['betPackSubscription'].unsubscribe).toHaveBeenCalled();
    expect(component['fanzoneSubscription'].unsubscribe).toHaveBeenCalled();
    expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledWith('online', jasmine.any(Function));
    expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledWith('offline', jasmine.any(Function));
    expect(component.countDownTimer.stop).toHaveBeenCalled();
    expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
  });

  it('onStakeChange', () => {
    component['handleOddsBoostSP'] = jasmine.createSpy();
    component.selection = {
      stake: '19',
      isEachWay: false,
      isLP: true,
      hasSPLP: true,
      price: {},
      onStakeChange: jasmine.createSpy()
    } as any;
    quickbetService.selectionData = {};

    component.onStakeChange();

    expect(component.selection.onStakeChange).toHaveBeenCalled();
    expect(quickbetDepositService.update).toHaveBeenCalledWith(
      component.selection.stake,
      component.selection.isEachWay
    );
    expect(quickbetService.saveQBStateInStorage).toHaveBeenCalledWith({
      userStake: component.selection.stake,
      userEachWay: component.selection.isEachWay,
      isLP: component.selection.isLP,
      freebet: undefined,
      isBoostActive: undefined,
      isLuckyDip: undefined
    });
    expect(component['handleOddsBoostSP']).toHaveBeenCalled();
  });

  it('onStakeChange (max stake)', () => {
    component.selection = {
      stake: '10',
      isBoostActive: true,
      onStakeChange: jasmine.createSpy()
    } as any;

    component.onStakeChange();
    expect(commandService.execute).toHaveBeenCalledWith(
      commandService.API.ODDS_BOOST_MAX_STAKE_EXCEEDED,
      [10]
    );
  });

  it('getFreebetsList for QB optimisation(userService.status = true', () => {
    component.selection = {
      isYourCallBet: false,
      freebetList: [
        {
          id: "154016588",
          offerName: "10GBP Champions League Free Bet",
          value: "10.00",
          freebetTokenValue: "10.00",
          expiry: "2023-01-23T07:19:31.000Z",
          type: "SPORTS",
          freebetOfferType: "",
          tokenPossibleBets: [
            {
              name: "Football Any",
              betLevel: "CATEGORY",
              betType: "",
              betId: "16"
            }
          ]
        },
        {
          id: "154016511",
          offerName: "10GBP Champions League Free Bet",
          value: "11.00",
          freebetTokenValue: "11.00",
          expiry: "2023-01-23T07:19:31.000Z",
          type: "SPORTS",
          freebetOfferType: "",
          tokenPossibleBets: [
            {
              name: "Football Any",
              betLevel: "CATEGORY",
              betType: "",
              betId: "16"
            }
          ]
        }
      ]
    } as any;

  component['mapFreebets'] = jasmine.createSpy().and.returnValue(component.selection.freebetList);

    userService.status = true;
    component['getFreebetsList']();
    expect(component.freebetsList as any).toEqual(component.selection.freebetList);
 
  });

  it('getFreebetsList (userService.status = false', () => {
    userService.status = false;
    component['getFreebetsList']();
    expect(component.freebetsList as any).toEqual([]);
  });
  it('getFreebetsList with freebetOfferCategories (userService.status = true)', () => {
    component.selection = {isYourCallBet : true} as any;
    freeBetsService.isBetPack.and.returnValue(true);
    freeBetsService.isFanzone.and.returnValue(true);
    localeService.getString.and.returnValues('BetPacks', 'FreeBets','Fanzone')
    component['mapFreebets'] = jasmine.createSpy().and.returnValue([
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09', freebetOfferCategories: {freebetOfferCategory: 'bet pack'} },
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09'},
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09', freebetOfferCategories: {freebetOfferCategory: 'fan zone'} },
    ]
  );
    component['getFreebetsList']();
    expect(component.betPackList.length).toEqual(3);
    expect(component.freebetsList.length).toEqual(0);
    expect(component.fanzoneList.length).toEqual(0);
  });

  it('getFreebetsList with freebetOfferCategories', () => {
    component.selection = {isYourCallBet : true} as any;
    localeService.getString.and.returnValues('BetPacks', 'FreeBets','Fanzone');
    freeBetsService.isBetPack.and.returnValue(false);
    freeBetsService.isFanzone.and.returnValue(false);
    component['mapFreebets'] = jasmine.createSpy().and.returnValue([
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09', freebetOfferCategories: {freebetOfferCategory: 'bet pack'} },
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09'}]
  );
    component['getFreebetsList']();
    expect(component.betPackList.length).toEqual(0);
    expect(component.freebetsList.length).toEqual(2);
    expect(component.fanzoneList.length).toEqual(0);

  });
  it('getFreebetsList with freebetOfferCategories fanzone', () => {
    component.selection = {isYourCallBet : true} as any;
    localeService.getString.and.returnValues('BetPacks', 'FreeBets','Fanzone');
    freeBetsService.isFanzone.and.returnValue(true);
    component['mapFreebets'] = jasmine.createSpy().and.returnValue([
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09', freebetOfferCategories: {freebetOfferCategory: 'Fanzone'} },
      { id: 16, freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2023 09:09:09'}]
  );
    component['getFreebetsList']();
    expect(component.fanzoneList.length).toEqual(2);
    expect(component.betPackList.length).toEqual(0);
    expect(component.freebetsList.length).toEqual(0);
  });
  it('getFreebetsList with empty list (userService.status = true', () => {
    component['mapFreebets'] = jasmine.createSpy().and.returnValue([]);
    component['getFreebetsList']();
    expect(component.betPackList.length).toEqual(0);
    expect(component.fanzoneList.length).toEqual(0);
    expect(component.freebetsList.length).toEqual(0);
    expect(component.fanzoneList.length).toEqual(0);
  });

  it('onFreebetChange', () => {
    component.selection = {
      stake: null,
      isEachWay: false
    } as any;
    component['setFreebet'] = jasmine.createSpy();
    component['handleOddsBoostFreeBet'] = jasmine.createSpy();
    component['onStakeChange'] = jasmine.createSpy();

    component.onFreebetChange({
      output: 'selectedChange',
      value: null
    });

    expect(component.setFreebet).toHaveBeenCalled();
    expect(quickbetDepositService.update).toHaveBeenCalledWith(null, false);
    expect(component['handleOddsBoostFreeBet']).toHaveBeenCalled();
    expect(component['onStakeChange']).toHaveBeenCalled();
  });

  it('onFreebetChange when stake has value', () => {
    component.selection = {
      stake: null,
      isEachWay: false
    } as any;
    component.setFreebet = jasmine.createSpy();
    component['handleOddsBoostFreeBet'] = jasmine.createSpy();
    component['onStakeChange'] = jasmine.createSpy();
    freeBetsService.isBetPack.and.returnValue(true);
    const fb = {name: '1', freebetOfferCategories: {freebetOfferCategory: 'Bet Pack'}, freebetTokenId: 123,} as any;
    component.onFreebetChange({
      output: 'selectedChange',
      value: fb
    });

    expect(component.selection.stake).toBe(null);
    expect(component.setFreebet).toHaveBeenCalledWith(fb, 'Bet Pack');
    expect(quickbetDepositService.update).toHaveBeenCalledWith(null, false);
    expect(component['handleOddsBoostFreeBet']).toHaveBeenCalled();
    expect(component['onStakeChange']).toHaveBeenCalled();
  });
  it('onFreebetChange when stake has value', () => {
    component.selection = {
      stake: null,
      isEachWay: false
    } as any;
    component.setFreebet = jasmine.createSpy();
    component['handleOddsBoostFreeBet'] = jasmine.createSpy();
    component['onStakeChange'] = jasmine.createSpy();
    freeBetsService.isFanzone.and.returnValue(false);
    const fb = {name: '1', freebetOfferCategories: {freebetOfferCategory: 'Fanzone'}, freebetTokenId: 123,} as any;
    component.onFreebetChange({
      output: 'selectedChange',
      value: fb
    });

    expect(component.selection.stake).toBe(null);
    expect(component.setFreebet).toHaveBeenCalledWith(fb, 'Fanzone');
    expect(quickbetDepositService.update).toHaveBeenCalledWith(null, false);
    expect(component['handleOddsBoostFreeBet']).toHaveBeenCalled();
    expect(component['onStakeChange']).toHaveBeenCalled();
  });
  
  it('setFreebet', () => {
    component.selection = {
      onStakeChange: jasmine.createSpy()
    } as any;
    component.freebetsList = [
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.99$',
        value : '9.99$',
        freebetTokenId: 123
      }
    ] as any[];

    component.setFreebet(component.freebetsList[0]);

    expect(component.selection.freebetValue).toBe(9.99);
    expect(component.selection.freebet).toBe(component.freebetsList[0]);
    expect(component.selection.onStakeChange).toHaveBeenCalled();
  });

  it('setFreebet with fanzonelist', () => {
    freeBetsService.isFanzone.and.returnValue(true);
    component.selection = {
      onStakeChange: jasmine.createSpy()
    } as any;
    component.fanzoneList = [
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.99$',
        value : '9.99$',
        freebetTokenId: 123
      }
    ] as any[];

    component.setFreebet(component.fanzoneList[0], ' fan zone ');
    expect(component.selection.freebetValue).toBe(9.99);
    expect(component.selection.freeBetOfferCategory).toBe(' fan zone ');
    expect(component.selection.onStakeChange).toHaveBeenCalled();
  });
  it('setFreebet with betToken', () => {
    freeBetsService.isBetPack.and.returnValue(true);
    component.selection = {
      onStakeChange: jasmine.createSpy()
    } as any;
    component.betPackList = [
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.99$',
        value : '9.99$',
        freebetTokenId: 1235

      },
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.999$',
        freebetTokenId: 1234

      }
    ] as any[];

    component.setFreebet(component.betPackList[0], 'bet pack');

    expect(component.selection.freebetValue).toBe(9.99);
    expect(component.selection.freebet).toBe(component.betPackList[0]);
    expect(component.selection.freeBetOfferCategory).toBe('bet pack');
    expect(component.selection.onStakeChange).toHaveBeenCalled();
  });

  it('setFreebet with fanzone', () => {
    freeBetsService.isFanzone.and.returnValue(true);
    component.selection = {
      onStakeChange: jasmine.createSpy()
    } as any;
    component.fanzoneList = [
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.99$',
        value : '9.99$',
        freebetTokenId: 1235

      },
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.999$',
        freebetTokenId: 1234

      }
    ] as any[];

    component.setFreebet(component.fanzoneList[0], 'Fanzone');

    expect(component.selection.freebetValue).toBe(9.99);
    expect(component.selection.freebet).toBe(component.fanzoneList[0]);
    expect(component.selection.freeBetOfferCategory).toBe('Fanzone');
    expect(component.selection.onStakeChange).toHaveBeenCalled();
  });
  it('setFreebet ("")', () => {
    component.selection = {
      onStakeChange: jasmine.createSpy()
    } as any;
    component.freebetsList = [
      {
        name: 'Weekly freebet 9.99$',
        freebetTokenValue: '9.99$',
        freebetTokenId: 123,
        id:123
      }
    ] as any[];

    component.setFreebet(null);

    expect(component.selection.freebetValue).toBe(0);
    expect(component.selection.freebet).toBe(undefined);
    expect(component.selection.onStakeChange).toHaveBeenCalled();
  });

  it('handleSelectedContestChangeOutput (output: null, value: {id: 1123131, name: contest})', () => {
    spyOn(component, 'handleSelectedContestChangeOutput');
    spyOn(component, 'contestSelectionGATrack');
    fiveASideContestSelectionService.defaultContestId = 1123131;
    component.contestSelectionGATrack({output: null, value: {id: 1123131, name: 'contest'}});
    expect(fiveASideContestSelectionService.defaultContestId).toBe(1123131);
    expect(component['contestSelectionGATrack']).toHaveBeenCalled();
  });

  it('handleSelectedContestChangeOutput', () => {
    spyOn(component, 'handleSelectedContestChangeOutput');
    spyOn(component as any, 'contestSelectionGATrack');
    component.handleSelectedContestChangeOutput({
      output: 'selectedChange',
      value: {id: '111', name: 'contest'}
    });
    fiveASideContestSelectionService.defaultContestId = 111;
    component.contestSelectionGATrack({output: null, value: {id: 1123131, name: 'contest'}});
    expect(fiveASideContestSelectionService.defaultContestId).toBe(111);
    expect(component['contestSelectionGATrack']).toHaveBeenCalled();
  });

  it('#contestSelectionGATrack should call gtm service', () => {
    component['contestSelectionGATrack']({output: null, value: {id: 1123131, name: 'contest'}});
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('handleSelectedContestChangeOutput (output: selectedContestChange, value: {id: 1123131, name: contest})', () => {
    it('event value is selectedContestChange', () => {
      spyOn(component, 'contestSelectionGATrack');
      component.handleSelectedContestChangeOutput({
        output: SELECTED_CONTEST_CHANGE,
        value: 1123131
      });
      fiveASideContestSelectionService.defaultContestId = 1123131;
      component.contestSelectionGATrack({output: null, value: {id: 1123131, name: 'contest'}});
      expect(fiveASideContestSelectionService.defaultContestId).toEqual(1123131);
      expect(component['contestSelectionGATrack']).toHaveBeenCalled();
    });

    it('event value is not selectedContestChange', () => {
      spyOn(component as any, 'contestSelectionGATrack');
      component.handleSelectedContestChangeOutput({
        output: '',
        value: null
      });
      expect(fiveASideContestSelectionService.defaultContestId).toBe(null);
      expect(component['contestSelectionGATrack']).not.toHaveBeenCalled();
    });
  });

  describe('onBoostClick', () => {
    beforeEach(() => {
      component.placeBetPending = {} as any;
    });

    it('not LP', () => {
      component.selection = { isLP: false } as any;
      component.onBoostClick();
      expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_SHOW_SP_DIALOG);
    });

    it('freebet active', () => {
      component.selection = { isLP: true, freebet: {} } as any;
      component.onBoostClick();
      expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_SHOW_FB_DIALOG, [false, 'quickbet']);
    });

    it('reboost active', () => {
      component.selection = { isLP: true, reboost: true, requestData: {} } as any;

      component.onBoostClick();

      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.REUSE_QUICKBET_SELECTION,
        component.selection.requestData
      );
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.ODDS_BOOST_SEND_GTM, { origin: 'quickbet', state: true }
      );
    });

    it('boost available', () => {
      component.selection = { isLP: true, freebet: null, isBoostActive: true } as any;

      component.onBoostClick();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.ODDS_BOOST_CHANGE, false);
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.ODDS_BOOST_SEND_GTM, { origin: 'quickbet', state: false }
      );
    });

    it('place bets pending', () => {
      component.placeBetPending.state = true;
      component.onBoostClick();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('initOddsBoost (logged out)', () => {
    component['user'] = { status: false } as any;
    component['initOddsBoost']();
    expect(cmsService.getOddsBoost).not.toHaveBeenCalledWith();
  });

  it('initOddsBoost (logged in, boost disabled)', fakeAsync(() => {
    component['user'] = { status: true } as any;
    component.selection = {} as any;
    cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: false }));

    component['initOddsBoost']();
    tick();

    expect(cmsService.getOddsBoost).toHaveBeenCalled();
    expect(commandService.execute).not.toHaveBeenCalledWith(commandApi.GET_ODDS_BOOST_ACTIVE);
  }));

  it('initOddsBoost (logged in, boost enabled)', fakeAsync(() => {
    component['user'] = { status: true } as any;
    component.selection = {
      onStakeChange: jasmine.createSpy(),
      oddsBoost: {
        betBoostMaxStake: '10'
      }
    } as any;
    pubSubService.subscribe.and.callFake((name, api, cb) => { cb(); } );
    component.isBoostEnabled = true;
    cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
    commandService.executeAsync.and.returnValue(observableOf(true));
    component.onStakeChange = jasmine.createSpy('onStakeChange');
    component.setFreebet = jasmine.createSpy('setFreebet');

    component['initOddsBoost']();
    tick();

    expect(cmsService.getOddsBoost).toHaveBeenCalled();
    expect(commandService.executeAsync).toHaveBeenCalledWith(commandApi.GET_ODDS_BOOST_ACTIVE_FROM_STORAGE);
    expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_SET_MAX_VAL, [
      component.selection.oddsBoost.betBoostMaxStake
    ]);

    expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_OLD_QB_PRICE, [
      component.selection
    ]);
    expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_NEW_QB_PRICE, [
      component.selection
    ]);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'QuickbetSelectionController',
      pubSubApi.ODDS_BOOST_CHANGE,
      jasmine.any(Function)
    );
    expect(component.selection.reboost).toBeFalsy();
    expect(component.selection.onStakeChange).toHaveBeenCalledTimes(1);

    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'QuickbetSelectionController',
      pubSubApi.ODDS_BOOST_UNSET_FREEBETS,
      jasmine.any(Function)
    );

    expect(component.selectedFreeBet).toEqual(null);
    expect(component.onStakeChange).toHaveBeenCalled();
  }));

  it('initOddsBoost (logged in, boost enabled, oddsBoost = undefined)', fakeAsync(() => {
    component['user'] = { status: true } as any;
    component.selection = {
      onStakeChange: jasmine.createSpy(),
      stake: "1.0"
    } as any;
    component.isBoostEnabled = true;
    cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
    commandService.executeAsync.and.returnValue(observableOf(true));

    pubSubService.subscribe = jasmine.createSpy().and.callFake((file, method, callback) => {
      if (callback) {
        if (method === 'ODDS_BOOST_CHANGE') {
          callback();
        }
      }
    });

    component['initOddsBoost']();
    tick();

    expect(commandService.execute).not.toHaveBeenCalled();
    expect(component['boostButtonDisabled']).toBeFalsy();
  }));

  describe('initOddsBoost',() => {
    beforeEach(() => {
      component['user'] = { status: true } as any;
      component.isBoostEnabled = true;
      cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
      commandService.executeAsync.and.returnValue(observableOf(true));
    });
    it('initOddsBoost (selection is disabled)', fakeAsync(() => {
      component.selection = {
        onStakeChange: jasmine.createSpy(),
        oddsBoost: {
          betBoostMaxStake: '10'
        },
        disabled: true
      } as any;

      component['initOddsBoost']();
      tick();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetSelectionController',
        pubSubApi.ODDS_BOOST_CHANGE,
        jasmine.any(Function)
      );
      expect(component.selection.reboost).toBeFalsy();
      expect(component.selection.onStakeChange).toHaveBeenCalledTimes(2);
    }));

    it('should reboost on boosting selection with changed price', fakeAsync(() => {
      component.selection = {
        isLP: true,
        reboost: false,
        requestData: {},
        isBoostActive: true,
        price: {
          isPriceChanged: true
        },
        onStakeChange: jasmine.createSpy(),
        stake: "1.0",
        oddsBoost: {
          betBoostMaxStake: '10'
        },
      } as any;
      component['initOddsBoost']();
      tick();

      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.REUSE_QUICKBET_SELECTION,
        component.selection.requestData
      );
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.ODDS_BOOST_SEND_GTM, { origin: 'quickbet', state: true }
      );
    }));
  });

  it('handleOddsBoostSP', () => {
    component.isBoostEnabled = true;
    component.selection = {
      isBoostActive: true,
      isLP: false
    } as any;

    component['handleOddsBoostSP']();

    expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_SHOW_SP_DIALOG);
  });

  it('handleOddsBoostFreeBet (true)', () => {
    component.isBoostEnabled = true;
    component.selection = {
      isBoostActive: true,
      freebet: {}
    } as any;

    component['handleOddsBoostFreeBet']();
    expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_SHOW_FB_DIALOG, [
      true, 'quickbet'
    ]);
  });

  it('handleOddsBoostFreeBet (false)', () => {
    component.isBoostEnabled = false;
    component.selection = {
      isBoostActive: true,
      freebet: {}
    } as any;

    component['handleOddsBoostFreeBet']();
    expect(commandService.execute).not.toHaveBeenCalledWith(commandApi.ODDS_BOOST_SHOW_FB_DIALOG, [
      true, 'quickbet'
    ]);
  });

  it('should check if stake is typed', () => {
    const selection = {
      stake: '20'
    };
    component.selection = <any>selection;
    expect(component.isInputFilled()).toEqual(true);
  });

  it('should show spinner', () => {
    component.placeBetPending = { state: true } as any;
    component.iniTimer = jasmine.createSpy();
    expect(component.showPendingSpinner()).toEqual(true);
    component.placeBetPending.state = false;
    expect(component.iniTimer).toHaveBeenCalled();
    expect(component.showPendingSpinner()).toEqual(false);
  });

  it('should start timer triggering countdown once', () => {
    pubSubService.subscribe.and.callFake((a, b, cb) => cb(3));
    timeService.countDownTimer.and.returnValue({} as any);

    expect(component.countDownTimer).not.toBeDefined();

    component.iniTimer();

    expect(component.countDownTimer).toBeDefined();
    expect(timeService.countDownTimer).toHaveBeenCalledWith(3);
    expect(timeService.countDownTimer).toHaveBeenCalledTimes(1);
  });

  it('should filter player name', () => {
    component.filterPlayerName('name');
    expect(filtersService.filterPlayerName).toHaveBeenCalledWith('name');
  });

  it('should get logged in status', () => {
    expect(component.isUserLoggedIn).toBe(true);
  });

  it('should get place bet text', () => {
    component.selection = {} as any;
    component.placeBetPending = { state: false } as any;
    component.iniTimer = jasmine.createSpy();
    expect(component.showPendingSpinner()).toEqual(false);

    expect(component.getPlaceBetText).toBe('quickbet.buttons.placeBet');

    component.selection = {
      price: {
        isPriceChanged: true
      }
    } as any;

    expect(component.getPlaceBetText).toBe('quickbet.buttons.acceptPlaceBet');
  });

  it('should get place bet text when handicap value was changed', () => {
    component.placeBetPending = { state: false } as any;
    component.iniTimer = jasmine.createSpy();
    expect(component.showPendingSpinner()).toEqual(false);
    quickbetUpdateService.isHandicapChanged.and.returnValue(true);
    component.selection = {
      price: {
        isPriceChanged: false
      }
    } as any;

    expect(component.getPlaceBetText).toBe('quickbet.buttons.acceptPlaceBet');
  });

  it('should get place bet text when handicap value and prices were not changed', () => {
    component.placeBetPending = { state: true } as any;
    component.iniTimer = jasmine.createSpy();
    expect(component.showPendingSpinner()).toEqual(true);
    quickbetUpdateService.isHandicapChanged.and.returnValue(false);
    component.selection = {
      price: {
        isPriceChanged: false
      }
    } as any;

    expect(component.getPlaceBetText).toBe('quickbet.buttons.placeBet');
  });


  it('should get selection amount classes', () => {
    component.selection = {
      currency: 'usd'
    } as any;

    expect(component.selectionAmountClasses).toEqual(
      jasmine.objectContaining({
        'filled-input': false,
        'currency-usd': true
      })
    );
  });

  it('should get disable plecebet value', () => {
    component.selection = {
      stake: '12',
      freebet: {},
      disabled: false
    } as any;

    expect(component.disablePlaceBet).toEqual(false);
  });

  it('disablePlaceBet (true)', () => {
    component.selection = {
      stake: {},
      disabled: false
    } as any;

    expect(component.disablePlaceBet).toBeTruthy();
  });

  describe('#placeBetFnHandler', () => {
    it('should emit placeBetFn', () => {
      component['hasBeenReloaded'] = true;
      spyOn(component.placeBetFn, 'emit');
      component.placeBetFnHandler();
      expect(component.placeBetFn.emit).toHaveBeenCalled();
    });

    it('should not emit placeBetFn (hasBeenReloaded = false)', () => {
      component['hasBeenReloaded'] = false;
      spyOn(component.placeBetFn, 'emit');
      component.placeBetFnHandler();
      expect(component.placeBetFn.emit).not.toHaveBeenCalled();
    });
  });

  it('should emit closeFn', () => {
    spyOn(component.closeFn, 'emit');
    component.closeFnHandler();
    expect(component.closeFn.emit).toHaveBeenCalled();
  });

  it('should emit addToBetslipFn', () => {
    spyOn(component.addToBetslipFn, 'emit');
    component.addToBetslipFnHandler();
    expect(component.addToBetslipFn.emit).toHaveBeenCalled();
  });

  it('should emit openQuickDepositFn', () => {
    spyOn(component.openQuickDepositFn, 'emit');
    component.openQuickDepositFnHandler();
    expect(component.openQuickDepositFn.emit).toHaveBeenCalled();
  });

  it('#changeOddsFormat', () => {
    component.selection = {
      price: {
        id: '1',
        isPriceUp: true,
        isPriceChanged: true,
        isPriceDown: true
      },
      oldOddsValue: '14/5'
    } as any;

    component.ycOddsValue = () => '1/2';
    component.changeOddsFormat();

    expect(component.selection.price).toEqual({
      id: '1',
      isPriceUp: false,
      isPriceChanged: false,
      isPriceDown: false
    });
    expect(component.selection.oldOddsValue).toBe('1/2');
  });

  it('isQualifiedFreebet (true)', () => {
    component.getFreeBetName = 'Build Your Bet Free Bet';
    const selection = { outcomeId: 10 } as any;
    const tokenPossibleBets = [{ betId: 10, betLevel: 'SELECTION' }] as any;
    expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeTruthy();
  });

  it('isQualifiedFreebet (false)', () => {
    const selection = {} as any;
    const tokenPossibleBets = [] as any;
    expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeFalsy();
  });

  describe('isQualifiedFreebet', () => {
    beforeEach(() => {
      component.getFreeBetName = 'Build Your Bet Free Bet';
    });
    it('check for banach markets and banach free bets', () => {
      const selection = { outcomeId: 10, channel: 'e' } as any;
      const tokenPossibleBets = [{ betId: 10, betLevel: 'SELECTION', name: 'Build Your Bet Free Bet' }] as any;
      expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeTruthy();
    });
    it('check for banach markets and nonbanach free bets', () => {
      const selection = { outcomeId: 10, channel: 'e' } as any;
      const tokenPossibleBets = [{ betId: 10, betLevel: 'SELECTION', name: 'Free Bet' }] as any;
      expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeTruthy();
    });
    it('check for non-banach markets and banach free bets', () => {
      const selection = { outcomeId: 10 } as any;
      const tokenPossibleBets = [{ betId: 10, betLevel: 'SELECTION', name: 'Build Your Bet Free Bet' }] as any;
      expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeFalsy();
    });
    it('check for non-banach markets and nonbanach free bets', () => {
      const selection = { outcomeId: 10 } as any;
      const tokenPossibleBets = [{ betId: 10, betLevel: 'SELECTION', name: 'Free Bet' }] as any;
      expect(component['isQualifiedFreebet'](selection, tokenPossibleBets)).toBeTruthy();
    });
  });

  it('mapFreebets (freebetTokenValue: "test", tokenPossibleBet: 10)', () => {
    const selection = {} as any;
    component.selection = {isYourCallBet : true} as any;
    freeBetsService.getFreeBetsState = jasmine.createSpy('getFreeBetsState').and.returnValue({
      data: [{ freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
      betTokens: [{ freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
      fanZone: [{freebetTokenId: 78, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }, { freebetTokenId: 99 , freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
      available: true
    });
    component['isQualifiedFreebet'] = jasmine.createSpy();

    component['mapFreebets'](selection);
    expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    expect(filtersService.setCurrency).not.toHaveBeenCalled();
    expect(component['isQualifiedFreebet']).toHaveBeenCalledWith(selection, [10] as any);
  });

  it('mapFreebets bettoken(freebetTokenValue: "test", tokenPossibleBet: 10)', () => {
    const selection = {} as any;
    component.selection = {isYourCallBet : true} as any;
    freeBetsService.getFreeBetsState = jasmine.createSpy('getFreeBetsState').and.returnValue({
      data: [{ freebetTokenValue: 'test', freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1"  }],
      betTokens: [{ freebetTokenValue: 'test1', freebetTokenExpiryDate:'22-12-2023 09:09:09',freebetOfferName:"test1"  }],
      fanZone: [{freebetTokenId: 78, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1"}, { freebetTokenId: 99, freebetTokenExpiryDate:'22-12-2022 09:09:09',freebetOfferName:"test1" }],
      available: true
    });
    component['isQualifiedFreebet'] = jasmine.createSpy();

    component['mapFreebets'](selection);
    expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    expect(filtersService.setCurrency).not.toHaveBeenCalled();
    expect(component['isQualifiedFreebet']).toHaveBeenCalledWith(selection, [] as any);
  });

  it('should toggle state of quick stake', () => {
    expect(component.quickStakeVisible).toEqual(true);

    component.onKeyboardToggle(false);
    expect(component.quickStakeVisible).toEqual(false);
  });

  describe('onQuickStakeSelect', () => {
    it('should update amount from 0 and notify about change', () => {
      const newAmount = '50';

      component.selection = {
        stake: null,
        onStakeChange: jasmine.createSpy('onStakeChange')
      } as any;
      const qbDigitKeyboard = jasmine.createSpyObj("qbDigitKeyboard", ["isKeyboardShown"]);
      component.qbDigitKeyboard=qbDigitKeyboard;
      component.qbDigitKeyboard['isKeyboardShown']=false;
      component.isBrandLadbrokes=true;
      component.onQuickStakeSelect(newAmount);

      expect(component.selection.stake).toEqual('50.00');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QB_QUICKSTAKE_PRESSED, ['50.00']);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({ event: 'trackEvent', eventCategory: 'quickbet', eventAction: 'click', eventLabel: 'predefined stake', locationEvent: undefined, positionEvent: 'top', eventDetails: '50' }));

    });

    it('should update amount from old value and notify about change', () => {
      const newAmount = '50';

      component.selection = {
        stake: '10.50',
        onStakeChange: jasmine.createSpy('onStakeChange')
      } as any;
      const qbDigitKeyboard = jasmine.createSpyObj("qbDigitKeyboard", ["isKeyboardShown"]);
      component.qbDigitKeyboard=qbDigitKeyboard;
      component.onQuickStakeSelect(newAmount);

      expect(component.selection.stake).toEqual('60.50');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QB_QUICKSTAKE_PRESSED, ['60.50']);
    });

    it('#isSelectionDisabled should return true',  () => {
      component.selection = {
        stake: '10.50',
        disabled: true
      } as any;

      expect(component.isSelectionDisabled()).toBeTruthy();
    });

    it('#isSelectionDisabled should return true',  () => {
      component.selection = {
        stake: null,
        disabled: true
      } as any;

      expect(component.isSelectionDisabled()).toBeTruthy();
    });
  });

  describe('priceTypeChange', () => {
    it('priceTypeChange LP', () => {
      component.selection = {
        stake: '10.50',
        onStakeChange: jasmine.createSpy('onStakeChange'),
        isLP: false
      } as any;
      component.priceTypeChange({ output: 'test', value: 'LP' });
      expect(component.selection.isLP).toEqual(true);
    });

    it('priceTypeChange SP', () => { component.selection = {
      stake: '10.50',
      onStakeChange: jasmine.createSpy('onStakeChange'),
      isLP: true
    } as any;
      component.priceTypeChange({ output: 'test', value: 'SP' });
      expect(component.selection.isLP).toEqual(false);
    });
  });

  describe('isMaxStakeExceeded', () => {
    it('boost is not active', () => {
      component.selection = { isBoostActive: false } as any;
      component['isMaxStakeExceeded']();
      expect(commandService.execute).not.toHaveBeenCalled();
    });

    it('boost active', () => {
      component.selection = { isBoostActive: true, stake: 5 } as any;
      component['isMaxStakeExceeded']();
      expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_MAX_STAKE_EXCEEDED, [5]);
    });

    it('boost active (e/w)', () => {
      component.selection = { isBoostActive: true, isEachWay: true, stake: 5 } as any;
      component['isMaxStakeExceeded']();
      expect(commandService.execute).toHaveBeenCalledWith(commandApi.ODDS_BOOST_MAX_STAKE_EXCEEDED, [10]);
    });
  });

  it('#isIFrameLoadingInProgress should return false when iframe is shown and panel is expanded', () => {
    component.showIFrame = true;
    component.quickDepositFormExpanded = true;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  it('#isIFrameLoadingInProgress should return false when iframe is shown and panel is collapsed', () => {
    component.showIFrame = true;
    component.quickDepositFormExpanded = false;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  it('#isIFrameLoadingInProgress should return true when iframe is not shown and panel is expanded', () => {
    component.showIFrame = false;
    component.quickDepositFormExpanded = true;
    expect(component['isIFrameLoadingInProgress']()).toBeTruthy();
  });

  it('#isIFrameLoadingInProgress should return false when iframe is not shown and panel is collapsed', () => {
    component.showIFrame = false;
    component.quickDepositFormExpanded = false;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  describe('isMakeQuickDeposit', () => {
    beforeEach(() => {
      component.placeBetPending = { state: false };
    });

    it('should check if quick deposit made if amount needed', () => {
      const deposit = {
        neededAmountForPlaceBet: '20'
      };
      userService.sportBalance = '10';
      component.quickDeposit = <any>deposit;
      expect(component.isMakeQuickDeposit()).toBeTruthy();
    });

    it('should check if quick deposit made if user balance = 0 and have freeBet', () => {
      const deposit = {
        neededAmountForPlaceBet: undefined
      };
      userService.sportBalance = '0';
      component.selection = { freebetValue: 5 } as any;
      component.quickDeposit = <any>deposit;
      expect(component.isMakeQuickDeposit()).toBeFalsy();
    });

    it('should check if quick deposit disabled if user balance = 0 and do not have freeBet', () => {
      const deposit = {
        neededAmountForPlaceBet: undefined
      };
      userService.sportBalance = '0';
      component.selection = { freebetValue: 0 } as any;
      component.quickDeposit = <any>deposit;
      expect(component.isMakeQuickDeposit()).toBeTruthy();
    });

    it('should check if quick deposit disabled if user balance is exist', () => {
      const deposit = {
        neededAmountForPlaceBet: undefined
      };
      userService.sportBalance = '10';
      component.quickDeposit = <any>deposit;
      expect(component.isMakeQuickDeposit()).toBeFalsy();
    });

    it('should check if quick deposit disabled if amount not needed', () => {
      const deposit = {
        neededAmountForPlaceBet: ''
      };
      userService.sportBalance = '10';
      component.quickDeposit = <any>deposit;
      expect(component.isMakeQuickDeposit()).toBeFalsy();
    });

    it('should check if quick deposit disabled if placeBetPending', () => {
      component.placeBetPending = {
        state: true
      };

      expect(component.isMakeQuickDeposit()).toBeFalsy();
    });
  });

  it('#isSelectionDisabled should return true',  () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(true);
    component.selection = {
      stake: '10.50',
      disabled: true
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeTruthy();
  });

  it('#isSelectionDisabled should return true',  () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.selection = {
      stake: '10.50',
      disabled: true
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeTruthy();
  });

  it('#isSelectionDisabled should return false',  () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.selection = {
      stake: '0',
      disabled: false
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeFalsy();
  });

  it('#isSelectionDisabled should return false',  () => {
    component.selection = {
      stake: '20.45',
      disabled: false
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeFalsy();
  });

  it('#isSelectionDisabled should return true',  () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(true);
    component.selection = {
      stake: '20.45',
      disabled: false
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeTruthy();
  });

  it('#isSelectionDisabled should return true',  () => {
    component.selection = {
      stake: null,
      disabled: true
    } as any;
    component.placeBetPending = {
      state: false
    };

    expect(component.isSelectionDisabled()).toBeTruthy();
  });

  it('#isSelectionDisabled should return true', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.selection = {
      stake: '20.45',
      disabled: false
    } as any;
    component.placeBetPending = {
      state: true
    };

    expect(component.isSelectionDisabled()).toBeTruthy();
  });

  it('#showSpinnerOnQuickDeposit should return false', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.placeBetPending = {
      state: false
    };

    expect(component.showSpinnerOnQuickDeposit()).toBeFalsy();
  });

  it('#showSpinnerOnQuickDeposit should return true when iframe loading is in progress', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(true);

    expect(component.showSpinnerOnQuickDeposit()).toBeTruthy();
  });

  it('#showSpinnerOnQuickDeposit should return true when bet placing is in progress', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.placeBetPending = {
      state: true
    };

    expect(component.showSpinnerOnQuickDeposit()).toBeTruthy();
  });

  describe('#onlineListener', () => {
    it('should call onlineListener method', () => {
      windowRef.nativeWindow.setTimeout.and.callFake((cb) => {
        cb && cb();
      });
      component['onlineListener']();

      expect(component['hasBeenReloaded']).toEqual(true);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1500);
    });
  });

  describe('#offlineListener', () => {
    it('should call offlineListener method', () => {
      component['offlineListener']();

      expect(component['hasBeenReloaded']).toEqual(false);
    });
  });

  describe('#formBodyParamforBuildBet', () => {
    it('form Body Param for BuildBet', () => {
      component.selection = {
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet']();
      expect(component.body).not.toBeNull();
    });
    it('form Body Param for BuildBet', () => {
      component.selection = {
        outcomeId: '1234'
      } as any;
      component['formBodyParamforBuildBet']();
      expect(component.body).not.toBeNull();
    });
  });

  describe('buildBetCall', () => {
    it('buildBetCall', () => {
      component.selection = {
        markets: [
          {
            name: 'Win or Each Way',
            eachWayPlaces: '4',
            previousOfferedPlaces:'3'
          }
        ],
      } as any
      const res = { bets: [{ maxPayout: '200' }] } as any;
      component['user'] = { bppToken: true } as any;
      component['buildBetCall']();
      expect(component.isUserLogIn).toBe(true);
      expect(component.extraPlaceName).toEqual('4 places instead of 3');
    });

    it('buildBetCall2', () => {
      component.selection = {
        markets: [
          {
            name: 'Outright',
            eachWayPlaces: '4',
            previousOfferedPlaces:'3'
            
          }
        ],
      } as any
      const res = { bets: [{ maxPayout: '200' }] } as any;
      component['user'] = { bppToken: false } as any;
      component['buildBetCall']();
      expect(component.isUserLogIn).toBe(false);
      expect(component.extraPlaceName).toEqual('4 places instead of 3');
    });

    it('buildBetCall error response', () => {
      const res = { betError: [{ errorDesc: 'text' }] } as any;
      bppProviderService = {
        quickBet: jasmine.createSpy('quickBet').and.returnValue(of({ betError: [{ errorDesc: 'text' }] }))
      };
      component = new QuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
        quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
        cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService,storageService,
        bonusSuppressionService);
      component['freeBetsFromBuildBet'] = [];
      component['user'] = { bppToken: true } as any;
      component['getFreebetsList'] = jasmine.createSpy();
      component['buildBetCall']();
      expect(component['freeBetsFromBuildBet'].length).toEqual(0);
    });
    it('get freebet list after sucess login', () => {
      bppProviderService = {
        quickBet: jasmine.createSpy('quickBet').and.returnValue(of(''))
      };
      component = new QuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
        quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
        cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService,storageService,
        bonusSuppressionService);
        component.selection = {
          isYourCallBet:false,
          price: {
            priceNum: 22,
            priceDen: 1,
            priceTypeRef: { id: '123' }
          },
           onStakeChange: jasmine.createSpy('onStakeChange')
        } as any;
       component['getFreebetsList'] = jasmine.createSpy();
      component.ngOnInit()
      loginCb('quickbet');
      expect(component['getFreebetsList']).toHaveBeenCalled();
    });

  });

  describe('addItem', () => {
    it('should add Item', () => {
      component.addItem(true);
      expect(component.maxPayedOut).toBe(true);
    });
    it('should add Item', () => {
      component.addItem(false);
      expect(component.maxPayedOut).toBe(false);
    });
  });

  describe('extraPlaceCheck', () => {
    it('when extraPlaces are offered', () => {
      sessionStorageService.get = jasmine.createSpy('sessionStorageService.get');
      component.extraPlaceData = extraPlaceData;
      component.selection = extraPlaceSelection as any;
      const res = component.extraPlaceCheck();
      expect(sessionStorageService.get).toHaveBeenCalled();
      expect(res).toBe(true);
    });

    it('when extraPlaces are offered with sessionStorage', () => {
      sessionStorageService.get = jasmine.createSpy('sessionStorageService.get').and.returnValue(extraPlaceData);
      component.selection = extraPlaceSelection as any;
      const res = component.extraPlaceCheck();
      expect(sessionStorageService.get).toHaveBeenCalled();
      expect(res).toBe(true);
    });


    it('when extraPlaces are offered', () => {
      sessionStorageService.get = jasmine.createSpy('sessionStorageService.get');
      component.extraPlaceData = extraPlaceData;
      component.selection = extraPlaceSelection as any;
      const res = component.extraPlaceCheck();
      expect(sessionStorageService.get).toHaveBeenCalled();
      expect(res).toBe(true);
    });

    it('extraPlaceCheck when market name is not Outright or win or each way', () => {
      component.extraPlaceData = extraPlaceData;
      component.selection = selection as any;
      const res = component.extraPlaceCheck();
      expect(res).toBe(false);
    });
  });

  describe('#updateEachWayAvailable in ngOnInit', () => {
    it('should call updateEachWayAvailable', () => {
      freeBetsService.getFreeBetsState = jasmine.createSpy('getFreeBetsState').and.returnValue({
        data: [{ freebetTokenValue: 'test', tokenPossibleBet: 10, freebetTokenExpiryDate:"22-12-2022 09:09:09" }],
        fanZone: [{freebetTokenId: 78, freebetTokenExpiryDate:"22-12-2022 09:09:09"}, { freebetTokenId: 99, freebetTokenExpiryDate:"22-12-2022 09:09:09" }],
        available: true,
        betTokens: [{ name: 'Weekly freebet 9.99$', freebetTokenValue: '9.99$', value:'9.99$', freebetTokenId: 123, freebetTokenExpiryDate: "22-12-2022 09:09:09" }] as any[]
      });
      component.selection = {
        isYourCallBet:true,
        eventId: 345,
        stake: "1.0",
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234',
        isEachWayAvailable: true,
        onStakeChange: jasmine.createSpy('onStakeChange')
      } as any;
      spyOn(component as any, 'updateEachWayAvailable');
      component.ngOnInit();
      expect(component['updateEachWayAvailable']).toHaveBeenCalled();
    });
  });
  describe('#updateEachWayAvailable', () => {
    it('should subscribe when data is published as make isEachWayAvailable updated', () => {
      component.selection = {
        eventId: 345,
        disabled: true,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: true,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234',
        isEachWayAvailable: true
      } as any;
      pubSubService.subscribe.and.callFake((file, method, callback) => {
        if (method === 'EACHWAY_FLAG_UPDATED') {
          callback('N');
        }
      });
      component['updateEachWayAvailable']();
      expect(component.selection.isEachWay).toBeFalse();
      expect(component.selection.isEachWayAvailable).toBeFalse();
    });
  });
  it('Freebets from quickbet MS', () => {
    component.selection = {
      isYourCallBet: false,
      freebetsList : [
        {
          name: 'Weekly freebet 9.99$',
          freebetTokenValue: '9.99$',
          freebetTokenId: 123,
          id:123
        }
      ]
    } as any;
    component['mapFreebets'](component.selection);
    expect(freeBetsService.getFreeBetsState).not.toHaveBeenCalled();
    component.selection = {isYourCallBet: false} as any;
    component['mapFreebets'](component.selection);
    expect(freeBetsService.getFreeBetsState).not.toHaveBeenCalled();
  });


  describe('GATracking', () => {
    it('setFreeBetGtmData should be called on eachway checkbox click', () => {
      component.selection = {
        isEachWay: true,
        eventName: 'portman',
        categoryId: '21',
        hasSP: false,
        onStakeChange: jasmine.createSpy('onStakeChange'),
        isLP: true
      } as any;

      component.selectedFreeBet = {
        name: 'freebet'
      } as any;

      spyOn(component as any, 'setFreeBetGtmData');
      component.onStakeChange();
      expect(component['setFreeBetGtmData']).toHaveBeenCalledWith(component.selection);
    });


    it('GA tracking for checkbox checked', () => {
      const selection = {
        isEachWay: true,
        eventName: 'portman',
        categoryId: '21'
      }
      const myPrivateSpy = spyOn<any>(component, 'setFreeBetGtmData').and.callThrough();
      myPrivateSpy.call(component, selection);
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('GA tracking for checkbox unchecked', () => {
      const selection = {
        isEachWay: false,
        eventName: 'portman',
        categoryId: '21'
      }
      const myPrivateSpy = spyOn<any>(component, 'setFreeBetGtmData').and.callThrough();
      myPrivateSpy.call(component, selection);
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('#update WinOrEachWay To To Win', () => {
    it('should call To Win in filterAddScore', () => {
      const selection = {
        categoryId:'21',
        categoryName:'HORSE_RACING',
        isFCTC: true,
        marketName:'Outrights',
        outcomeName:'Win'
      }
      component.filterAddScore(selection);
      expect(filtersService.filterAddScore).toHaveBeenCalledWith('Outrights', 'Win');
    });
    it('should call To Win in filterAddScore', () => {
      const selection = {
        categoryId:'21',
        categoryName:'HORSE_RACING',
        isFCTC: false,
        marketName:'Win or Each Way',
        outcomeName:'Win'
      }
      component.filterAddScore(selection);
      expect(filtersService.filterAddScore).toHaveBeenCalledWith('Win or Each Way', 'Win' );
    });
    it('should call To Win in filterAddScore', () => {
      const selection = {
        categoryId:'21',
        categoryName:'HORSE_RACING',
        isFCTC: false,
        marketName:'Win or Each Way',
        outcomeName:'Win'
      }
      filtersService.filterAddScore=jasmine.createSpy('filterAddScore').and.returnValue('Win or Each Way')
      component = new QuickbetSelectionComponent(pubSubService, userService, localeService, filtersService,
        quickbetDepositService, quickbetService, quickbetUpdateService, freeBetsService, quickbetNotificationService, commandService,
        cmsService, gtmService, cdr, windowRef, timeService, bppProviderService, fiveASideContestSelectionService, serviceClosureService, sessionStorageService, storageService, bonusSuppressionService);
      const checkMarketName = component.filterAddScore(selection);
      expect(filtersService.filterAddScore).toHaveBeenCalledWith('Win or Each Way', 'Win' );
      expect(checkMarketName).toEqual('To Win');
    });
    it('should call WinOrEachWay in filterAddScore', () => {
      const selection = {
        categoryId:'19',
        categoryName:'GRAYHOUNDS',
        isFCTC: true,
        marketName:'OUTRIGHTS',
        outcomeName:'Win'
      }
      component.filterAddScore(selection);
      expect(filtersService.filterAddScore).toHaveBeenCalledWith('OUTRIGHTS', 'Win' );
    });
    it('should call WinOrEachWay in filterAddScore', () => {
      const selection = {
        categoryId:'19',
        categoryName:'GRAYHOUNDS',
        isFCTC: false,
        marketName:'Win or Each Way',
        outcomeName:'Win'
      }
      component.filterAddScore(selection);
      expect(filtersService.filterAddScore).toHaveBeenCalledWith('Win or Each Way', 'Win' );
    });
  });

  describe('#show tooltip for eachway checkbox', () => {
    it('should call tooltip on onload', () => {
      component.selection = {
        eventId: 345,
        disabled: false,
        newOddsValue: '11/4',
        oldOddsValue: '14/5',
        isEachWay: false,
        price: {
          priceNum: 22,
          priceDen: 1,
          priceTypeRef: { id: '123' }
        },
        outcomeId: '1234',
        categoryName: 'HORSE_RACING',
        categoryId: '19'
      } as any;
      component['storageService'].get = jasmine.createSpy('get').and.returnValue([{user:'test1'}]);
      windowRef.nativeWindow.setTimeout.and.callFake((cb) => {
        cb && cb();
      });
      component['userService'] = { username : 'test' } as any;
      component.showEachWay(component.selection);
      expect(storageService.set).toHaveBeenCalledWith('TooltipEachWay', Object({ user: 'test', displayed: true }));
      expect(storageService.get).toHaveBeenCalledWith('TooltipEachWay');
      expect(storageService.set).toHaveBeenCalledTimes(1);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000000);
    });
  });

  describe('#GA traking for eachway checkbox', () =>{
    it('#should call checked when eachWay checkbox is true', ()=>{
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'betslip',
        'component.LabelEvent': "Horse Racing",
        'component.ActionEvent': 'checked',
        'component.PositionEvent': 'EachWay.outcomeName',
        'component.LocationEvent': 'quickbet',
        'component.EventDetails': 'each way alert',
        'component.URLclicked': 'not applicable',
        'sportID': '21'
      };
     const EachWay = {
      categoryName: "Horse Racing",
      isEachWay: true,
      sportID:'21',
      outcomeName: 'EachWay.outcomeName'
      }
      component.eachWayGaTracking = true;
      component.gaTrackingOnEachWayCheckBox(EachWay);
      expect(component.eachWayGaTracking).toBeTruthy();
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
    it('#should call unchecked when eachWay checkbox is false', ()=>{
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'betslip',
        'component.LabelEvent': "Horse Racing",
        'component.ActionEvent': 'unchecked',
        'component.PositionEvent': 'EachWay.outcomeName',
        'component.LocationEvent': 'quickbet',
        'component.EventDetails': 'each way regular',
        'component.URLclicked': 'not applicable',
        'sportID': '21'
      };
     const EachWay = {
      categoryName: "Horse Racing",
      isEachWay: false,
      sportID:'21',
      outcomeName: 'EachWay.outcomeName'
      }
      component.eachWayGaTracking = false;
      component.gaTrackingOnEachWayCheckBox(EachWay);
      expect(component.eachWayGaTracking).toBeFalsy();
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
  });

  it('#getPlaceBetCTAText', ()=>{
  component.luckyDipCmsData ={
    title: '',
    desc: '',
    welcomeMessage: '',
    betPlacementTitle: '',
    betPlacementStep1: '',
    betPlacementStep2: '',
    betPlacementStep3:'',
    termsAndConditionsURL: '',
    playerCardDesc: '',
    potentialReturnsDesc: '',
    backCTAButton: '',
    depositButton: '',
    gotItCTAButton:'',
    placebetCTAButton: '{abc-123}'
  }  
    component.isLuckyDip  = true;
    
    component['getPlaceBetCTAText']();
    expect(component['getPlaceBetCTAText']).toBeTruthy();
  });

  it('#getPlaceBetCTAText return false if no luckyDip', ()=>{
    component.luckyDipCmsData ={
      title: '',
      desc: '',
      welcomeMessage: '',
      betPlacementTitle: '',
      betPlacementStep1: '',
      betPlacementStep2: '',
      betPlacementStep3:'',
      termsAndConditionsURL: '',
      playerCardDesc: '',
      potentialReturnsDesc: '',
      backCTAButton: '',
      depositButton: '',
      gotItCTAButton:'',
      placebetCTAButton: '{abc-123}'
    }  
      component.isLuckyDip  = false;
      
      component['getPlaceBetCTAText']();
      expect(component['getPlaceBetCTAText']()).toEqual('quickbet.buttons.placeBet');
    });
    it('#getPlaceBetCTAText return false if no placebetCTAButton', ()=>{
      component.luckyDipCmsData ={
        title: '',
        desc: '',
        welcomeMessage: '',
        betPlacementTitle: '',
        betPlacementStep1: '',
        betPlacementStep2: '',
        betPlacementStep3:'',
        termsAndConditionsURL: '',
        playerCardDesc: '',
        potentialReturnsDesc: '',
        backCTAButton: '',
        depositButton: '',
        gotItCTAButton:'',
        placebetCTAButton: ''
      }  
        component.isLuckyDip  = false;
        
        component['getPlaceBetCTAText']();
        expect(component['getPlaceBetCTAText']()).toEqual('quickbet.buttons.placeBet');
      });

      it('#getbackBtnCTAText return back button text configured in CMS if luckyDip', ()=>{
        component.luckyDipCmsData ={
          title: '',
          desc: '',
          welcomeMessage: '',
          betPlacementTitle: '',
          betPlacementStep1: '',
          betPlacementStep2: '',
          betPlacementStep3:'',
          termsAndConditionsURL: '',
          playerCardDesc: '',
          potentialReturnsDesc: '',
          backCTAButton: 'Back',
          depositButton: '',
          gotItCTAButton:'',
          placebetCTAButton: '{abc-123}'
        }  
          component.isLuckyDip  = true;
          
          expect(component['getbackBtnCTAText']()).toEqual(component.luckyDipCmsData.backCTAButton);
        });

        it('#getbackBtnCTAText return if not luckydip', ()=>{
            component.isLuckyDip  = false;
          
            expect(component['getbackBtnCTAText']()).toEqual('quickbet.buttons.back');
          });
});
