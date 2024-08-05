import { Observable, of, Subject, throwError, Subscription } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';

import { BetslipComponent } from '@betslip/components/betslip/betslip.component';
import { SelectionInfoDialogComponent } from '@betslip/components/selectionInfoDialog/selection-info-dialog.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IBetslipBetData } from '@betslip/models/betslip-bet-data.model';
import { IBetInfo } from '@betslip/services/bet/bet.model';
import { IBetslipDepositData } from '@app/betslip/models/betslip-deposit.models';
import Spy = jasmine.Spy;
import { ElementRef, Type } from '@angular/core';
import { IFreeBet } from '../../services/freeBet/free-bet.model';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';

describe('BetslipComponent', () => {
  const title = 'BetSlip';

  let component: BetslipComponent,
    userService,
    overAskService,
    cmsService,
    windowRefService,
    betslipLiveUpdateService,
    betslipService,
    toteBetReceiptService,
    resolveService,
    betReceiptService,
    localeService,
    quickDepositService,
    betInfoDialogService,
    infoDialogService,
    storageService,
    digitalSportBetsService,
    betSlipBannerService,
    deviceService,
    freeBetsService,
    sessionService,
    fracToDecService,
    gtmService,
    pubSubService,
    pubsubReg,
    commandService,
    bsFiltersService,
    betslipStorageService,
    betslipDataService,
    betslipStakeService,
    datePipe,
    filterService,
    awsService,
    router,
    routingState,
    timeService,
    bodyScrollLockService,
    toteBetslipService,
    dialogService,
    homeBetslipCb,
    clearStakeCb,
    componentFactoryResolver,
    accountUpgradeLinkService,
    quickDepositIframeService,
    changeDetectorRef,
    serviceClosureService,
    siteServerRequestHelperService,
    sessionStorageService,
    coreToolsService,
    signpostingCmsService,
    getSelectionDataService;

  const priceUpdate = new Subject();
  const clientHeight = 10;

  const liveUpdateData = {
    info: () => ({}),
    history: {
      isPriceChanged: () => false,
      isPriceChangedAndMarketUnsuspended: () => false
    }
  };

  const ssMarkets = {
    SSResponse: {
      children: [
        {
          event:{
            id: 234578765,
            startTime: '124098129857',
            typeName: '56789tyuio',
            categoryId: '21',
            children: [
              {
                market:{
                  id: 909423090,
                  maxAccumulators: 1,
                  minAccumulators: 1
                }
              }
            ]
          }
        }
      ]
    }
  };

  const ssMarketsMaxMinAccMissing = {
    SSResponse: {
      children: [
        {
          event:{
            id: 234578765,
            startTime: '124098129857',
            typeName: '56789tyuio',
            children: [
              {
                market:{
                  id: 909423090
                }
              }
            ]
          }
        }
      ]
    }
  };

  const restrictedCardMock:any = {
    restrictedRaces: ['Kempton - 21:00'],
    horseNames: ['abc'],
    eventIdDetails: ["222618797"]
  };

  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: true
  }

  beforeEach(() => {
    userService = {
      currencySymbol: '£',
      status: true,
      sportBalance: null,
      getRetailCard: jasmine.createSpy('getRetailCard'),
      username: 'test',
      oddsFormat: 'frac',
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
      getUserDepositNeededAmount: jasmine.createSpy('getUserDepositNeededAmount'),
      getUserDepositMessage: jasmine.createSpy('getUserDepositMessage')
    };
    overAskService = {
      clearStateMessage: jasmine.createSpy('clearStateMessage'),
      clearBetsData: jasmine.createSpy('clearBetsData'),
      setBetsData: jasmine.createSpy('setBetsData'),
      sortDeclinedBetsOnTop: jasmine.createSpy('sortDeclinedBetsOnTop').and.returnValue([]),
      sortLinkedBets: jasmine.createSpy('sortLinkedBets').and.returnValue([]),
      errorMessage: null,
      stateMessage: null,
      hasCustomerActionTimeExpired: null,
      hasTraderMadeDecision: null,
      isNoBetsOffered: null,
      isInProcess: null,
      isOnTradersReview: null,
      isSomeBetsDeclined: null,
      isAllBetsDeclined: null,
      isNotInProcess: null,
      acceptOffer: jasmine.createSpy('acceptOffer'),
      rejectOffer: jasmine.createSpy('rejectOffer').and.returnValue(of({})),
      isOveraskCanBePlaced: jasmine.createSpy('isOveraskCanBePlaced').and.returnValue(true),
      removeDeletedBetID: jasmine.createSpy('removeDeletedBetID'),
      collectDeletedBetID: jasmine.createSpy('collectDeletedBetID')
    };
    cmsService = {
      getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(of({})),      
      getQuickStakes : jasmine.createSpy('getQuickStakes').and.returnValue(of(['1','2','3','4'])),
      getFeatureConfig: jasmine.createSpy('getOddsBoost').and.returnValue(of({
        title: 'title',
        topMessage: 'top message',
        bottomMessage: 'bottom message',
      })),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        maxPayOut: {
          maxPayoutFlag: true,
          maxPayoutMsg: 'your return is one million'
        },
        eachWayTooltip: {
          Delay: 1000,
          Message: 'Back your selection to win or place. Please note: This doubles your stake.',
          Enable: true
        },
        restrictedHRMessages: {
          enabled: true,
          restrictedHorseMsg: 'Please beware some of your selections have been suspended',
          restrictedRaceCardMsg: 'Multiples for the following race(s) are currently suspended'
        },
        FreeBets: {
          poolBet: {
            poolType: 'UTRI'
          },
          toteBetDetails:{
            betName:'1 "REVERSE"',
            orderedOutcomes: [{}]
          }
        }
      }))
    };
    windowRefService = {
      nativeWindow: {
        location: {
          href: 'location_href'
        },
        navigator:{
          onLine :true
        },
        view: { mobile: null },
        setInterval: jasmine.createSpy('setInterval').and.callFake((callback: Function) => {
          callback();
        }),
        clearInterval: jasmine.createSpy('clearInterval'),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        vsmobile: {
          instance: {
            getAllSelectedBets: jasmine.createSpy('getAllSelectedBets'),
            deselectBet: jasmine.createSpy('deselectBet'),
          }
        },
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        })
      },
      document: {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          style: {},
          clientHeight: clientHeight
        }]),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          blur: jasmine.createSpy()
        }),
      }
    };
    betslipLiveUpdateService = {
      clearAllSubs: jasmine.createSpy('clearAllSubs'),
      subscribe: jasmine.createSpy('subscribe').and.returnValue([]),
      reconnect: jasmine.createSpy('reconnect'),
      getPriceUpdate: jasmine.createSpy('getPriceUpdate').and.returnValue(of({}))
    };
    betslipService = {
      getMultiplePotentialPayout: jasmine.createSpy('getMultiplePotentialPayout').and.returnValue('1/2'),
      isSuspended: jasmine.createSpy().and.returnValue(false),
      removeByOutcomeId: jasmine.createSpy(),
      suspendedIndexFromSelection:jasmine.createSpy('suspendedIndexFromSelection'),
      removeByOutcomeIds:jasmine.createSpy(),
      isSinglesHasOldPrice: jasmine.createSpy().and.returnValue(true),
      buildPotentialPayoutObj: jasmine.createSpy(),
      setPriceType: jasmine.createSpy(),
      isFreeBetValid: jasmine.createSpy(),
      parsePlaceBetsResponse: jasmine.createSpy('parsePlaceBetsResponse').and.returnValue({
        bets: [{
          freeBet: {}
        }]
      }),
      winOrEachWay: jasmine.createSpy('winOrEachWay'),
      fetch: jasmine.createSpy('fetch').and.returnValue(of([])),
      showSuspendedOutcomeErr: jasmine.createSpy('showSuspendedOutcomeErr').and.returnValue({
        multipleWithDisableSingle: false,
        disableBet: false,
        msg: 'Please beware that %1 of your selections has been suspended'
      }),
      placeBets: jasmine.createSpy('placeBets').and.returnValue(of({})),
      findSuspendedBetsId: jasmine.createSpy('findSuspendedBetsId'),
      getPlaceBetPending: jasmine.createSpy('getPlaceBetPending').and.returnValue(true),
      getConfig: jasmine.createSpy('getConfig').and.returnValue(of({})),
      setConfig: jasmine.createSpy(),
      isMultipleFreeBetSelected: jasmine.createSpy('isMultipleFreeBetSelected'),
      setAmount: jasmine.createSpy('setAmount'),
      countSuspendedOutcomes: jasmine.createSpy('countSuspendedOutcomes').and.returnValue(0),
      setPlaceBetPending: jasmine.createSpy('setPlaceBetPending').and.callFake(value => value),
      areBetsWithStakes: jasmine.createSpy(),
      betSlipReady: new Subject(),
      count: jasmine.createSpy('count').and.returnValue(5),
      updateLegsWithPriceChange: jasmine.createSpy('updateLegsWithPriceChange'),
      exucuteOverask: jasmine.createSpy('exucuteOverask').and.returnValue(of({})),
      getBetslipBetByResponseBet: jasmine.createSpy('getBetslipBetByResponseBet'),
      getSuspendedMessage: jasmine.createSpy('getSuspendedMessage'),
      updateAvailableFreeBets: jasmine.createSpy('updateAvailableFreeBets'),
      findBetForFreeBetTooltip: jasmine.createSpy('findBetForFreeBetTooltip'),
      closeNativeBetslipAndWaitAnimation: jasmine.createSpy('closeNativeBetslipAndWaitAnimation').and.callFake(cb => cb()),
      isBetNotPermittedError: jasmine.createSpy('isBetNotPermittedError'),
      getBetNotPermittedError: jasmine.createSpy('getBetNotPermittedError'),
      constructFreeBet: jasmine.createSpy('constructFreeBet').and.returnValue({})
    };
    toteBetReceiptService = {};
    resolveService = {
      reset: jasmine.createSpy('reset')
    };

    betReceiptService = {
      message: {
        type: undefined,
        msg: undefined
      },
      isBetSlipShown: true,
      isBonusApplicable: jasmine.createSpy('isBonusApplicable'),
      isSP: jasmine.createSpy('isSP'),
      luckyAllWinnersBonus: jasmine.createSpy('luckyAllWinnersBonus').and.returnValue('£0.00'),
      isAllWinnerOnlyApplicable: jasmine.createSpy('isAllWinnerOnlyApplicable'),
      returnAllWinner: jasmine.createSpy('returnAllWinner'),
      isLuckyBonusAvailable: true
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('')
    };
    quickDepositService = {
      getAccounts: jasmine.createSpy('getAccounts'),
      checkQuickDeposit: jasmine.createSpy('checkQuickDeposit'),
      showInsufficientFundsMessage: jasmine.createSpy('showInsufficientFundsMessage'),
      config: {
        userHasCreditCard: false
      }
    };
    betInfoDialogService = {
      multiple: jasmine.createSpy(),
      isRacing: jasmine.createSpy().and.returnValue(true)
    };
    infoDialogService = jasmine.createSpyObj(['openConnectionLostPopup', 'openInfoDialog', 'closePopUp']);
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue({user:'test', toteBet: {
        poolBet: {
          poolType: 'UTRI'
        },
        toteBetDetails:{
          betName:'1 "REVERSE"',
          orderedOutcomes: [{}]
        }
      }}),
      remove: jasmine.createSpy('remove')
    };
    digitalSportBetsService = {
      getDSBetslipCounter: jasmine.createSpy('getDSBetslipCounter').and.callFake((callback: Function) => {
        callback(1);
      })
    };
    betSlipBannerService = {
      setBetSlipOpened: jasmine.createSpy('setBetSlipOpened'),
      setIsBannerAvailable: jasmine.createSpy('setIsBannerAvailable')
    };
    deviceService = {
      parsedUA: 'test',
      browserName: '',
      isIos: true,
      osVersion: '',
      isDesktop: false,
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true),
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType)
    };
    freeBetsService = {
      getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(of(null)),
      getFreeBetsState: jasmine.createSpy('getFreeBetsState').and.returnValue({}),
      getFreeBetsData: jasmine.createSpy('getFreeBetsData').and.returnValue({}),
      store: jasmine.createSpy('store'),
      isBetPack: jasmine.createSpy('isBetPack'),
      getFreeBetInBetSlipFormat: jasmine.createSpy('getFreeBetInBetSlipFormat').and.returnValue({id: '124'} as IFreeBet),
      isFanzone : jasmine.createSpy('isFanzone')

    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve()),
      whenSession: jasmine.createSpy('whenSession').and.returnValue(Promise.resolve())
    };
    fracToDecService = {
      decToFrac: jasmine.createSpy('decToFrac').and.returnValue('1/2'),
      getDecimal: jasmine.createSpy('getDecimal').and.returnValue(5),
      getAccumulatorPrice: jasmine.createSpy('getAccumulatorPrice').and.returnValue('0.5/1'),
      getNumberWith2Decimals: jasmine.createSpy('decToFrac').and.callThrough()
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubsubReg = {};
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, cb) => {
        if (p2 === 'BS_SELECTION_LIVE_UPDATE') {
          cb(liveUpdateData);
        } else if (p2 === 'HOME_BETSLIP') {
          homeBetslipCb = cb;
        } else if (p2 === 'BETSLIP_CLEAR_STAKE') {
          clearStakeCb = cb;
        } else if (p2 === 'SESSION_LOGOUT') {
          pubsubReg[p2] = cb;
        } else if (p2 === 'SUCCESSFUL_LOGIN') {
          pubsubReg[p2] = cb;
        } else if (p2 === 'BETSLIP_UPDATED') {
          cb([]);
        } else if (p2 === 'OVERASK_CLEAN_BETSLIP' || p2 === 'OVERASK_BETS_DATA_UPDATED' || p2 === 'OPEN_QUICK_DEPOST_FROM_BETSLIP_HEADER') {
          pubsubReg[p2] = cb;
        } else if (p2 === 'BETS_COUNTER_PLACEBET') {
          pubsubReg[p2] = cb;
        } else if (p2 === 'FIRST_BET_PLACEMENT_TUTORIAL') {
          pubsubReg[p2] = cb;
        } else if (p2 === 'EACHWAY_FLAG_UPDATED') {
          pubsubReg[p2] = cb;
        } else {
          cb(true);
        }
      }),
      publishSync: jasmine.createSpy('publishSync'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish').and.callFake((channel, args) => {
        pubsubReg[channel] && pubsubReg[channel](args || true);
      })
    };
    commandService = {
      API: {
        ODDS_BOOST_SET_MAX_VAL: 'ODDS_BOOST_SET_MAX_VAL',
        BESTLIP_ERROR_TRACKING: 'BESTLIP_ERROR_TRACKING',
        ODDS_BOOST_OLD_PRICE: 'ODDS_BOOST_OLD_PRICE',
        ODDS_BOOST_NEW_PRICE: 'ODDS_BOOST_NEW_PRICE',
        ODDS_BOOST_SHOW_FB_DIALOG: 'ODDS_BOOST_SHOW_FB_DIALOG',
        GET_ODDS_BOOST_ACTIVE: 'GET_ODDS_BOOST_ACTIVE',
        ACCA_NOTIFICATION_CHANGED: 'ACCA_NOTIFICATION_CHANGED',
        ODDS_BOOST_MAX_STAKE_EXCEEDED: 'ODDS_BOOST_MAX_STAKE_EXCEEDED',
        GET_ODDS_BOOST_TOKENS: 'GET_ODDS_BOOST_TOKENS'
      },
      execute: jasmine.createSpy('execute').and.returnValue({}),
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      register: jasmine.createSpy('register')
    };
    toteBetslipService = {
      freeBetText: '',
      reload: jasmine.createSpy('reload'),
      clear: jasmine.createSpy('clear'),
      removeToteBet: jasmine.createSpy('removeToteBet'),
      placeBet: jasmine.createSpy('placeBet').and.returnValue(of({})),
      getTotalStake: jasmine.createSpy('getTotalStake'),
      isToteBetPresent: jasmine.createSpy('isToteBetPresent').and.returnValue(true),
      isToteBetWithProperStake: jasmine.createSpy('isToteBetWithProperStake').and.returnValue(true),
      setTokenValue: (token) => { return token },
      setFreeBetsConfig: (config) => { return config;},
      setToteFreeBetText: (text) => { return text},
      getToteFreeBetText: () => {return toteBetslipService.freeBetText;},
      getRoundedValue: (freebetVal) => {return freebetVal;}
    };
    bsFiltersService = {
      todayTomorrowDate: jasmine.createSpy('todayTomorrowDate'),
      multiplesSort: jasmine.createSpy('multiplesSort').and.returnValue([])
    };
    betslipStorageService = {
      restoreUserStakeData: jasmine.createSpy('restoreUserStakeData'),
      setFreeBet: jasmine.createSpy('setFreeBet'),
      clean: jasmine.createSpy('clean'),
      restore: jasmine.createSpy('restore').and.returnValue([]),
      cleanBetslip: jasmine.createSpy('cleanBetslip'),
      clearStateInStorage: jasmine.createSpy('clearStateInStorage'),
    };
    betslipDataService = {
      bets: [],
      readBets: {bets: []},
      containsRegularBets: jasmine.createSpy('containsRegularBets').and.returnValue(false)
    };
    betslipStakeService = {
      maxFlag: false,
      getStake: jasmine.createSpy('getStake'),
      getFreeBetStake: jasmine.createSpy('getFreeBetStake'),
      getFreeBetLabelText: jasmine.createSpy('getFreeBetLabelText'),
      getFreeBetImageName: jasmine.createSpy('getFreeBetImageName'),
      getTotalStake: jasmine.createSpy('getTotalStake'),
      calculateEstReturnsMultiples: jasmine.createSpy('calculateEstReturnsMultiples').and.returnValue(5),
      calculateEstReturns: jasmine.createSpy('calculateEstReturns').and.returnValue(5),
      getTotalEstReturns: jasmine.createSpy('getTotalEstReturns')
    };
    datePipe = {
      transform: jasmine.createSpy()
    };
    filterService = {
      setCurrency: jasmine.createSpy('setCurrency'),
      removeLineSymbol: jasmine.createSpy('removeLineSymbol'),
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy('routingState')
    };
    timeService = {
      getEventTime: jasmine.createSpy('getEventTime'),
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('13:20'),
      parseDateTime: jasmine.createSpy('parseDateTime')
    };
    bodyScrollLockService = {
      disableBodyScroll: jasmine.createSpy('disableBodyScroll'),
      enableBodyScroll: jasmine.createSpy('enableBodyScroll')
    };
    dialogService = <any>{
      openDialog: jasmine.createSpy('openDialog')
    };
    componentFactoryResolver = <any>{
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    accountUpgradeLinkService = {
      inShopToMultiChannelLink: '/in-shop-test-url',
      onlineToMultiChannelLink: '/online-test-url',
    };

    quickDepositIframeService = {
      isEnabled: jasmine.createSpy().and.returnValue(of(true))
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };

    signpostingCmsService = {
      getFreebetSignposting : jasmine.createSpy('getFreebetSignposting').and.returnValue(of({}))
    };

    getSelectionDataService = {
      getOutcomeData: jasmine.createSpy().and.returnValue(of(null)),
      restrictedRacecardAndSelections: jasmine.createSpy('restrictedRacecardAndSelections').and.returnValue(restrictedCardMock),
      outcomeData: ssMarkets.SSResponse.children
    };

    siteServerRequestHelperService = {
      getEventsByMarkets: jasmine.createSpy().and.returnValue(Promise.resolve(ssMarkets))
    };
    sessionStorageService = {
      get: jasmine.createSpy('').and.returnValue(null)
    };

    coreToolsService = {
      getOwnDeepProperty: jasmine.createSpy().and.returnValue(true)};

    createComponent();
    component.quickDeposit = {} as IBetslipDepositData;
  });

  function createComponent() {
    component = new BetslipComponent(
      overAskService,
      windowRefService,
      betslipLiveUpdateService,
      betslipService,
      toteBetslipService,
      userService,
      resolveService,
      betReceiptService,
      localeService,
      quickDepositService,
      betInfoDialogService,
      infoDialogService,
      storageService,
      digitalSportBetsService,
      deviceService,
      freeBetsService,
      sessionService,
      fracToDecService,
      gtmService,
      pubSubService,
      commandService,
      toteBetReceiptService,
      bsFiltersService,
      betslipStorageService,
      betslipDataService,
      cmsService,
      betslipStakeService,
      datePipe,
      filterService,
      awsService,
      router,
      routingState,
      timeService,
      bodyScrollLockService,
      dialogService,
      componentFactoryResolver,
      accountUpgradeLinkService,
      quickDepositIframeService,
      changeDetectorRef,
      serviceClosureService,
      siteServerRequestHelperService,
      sessionStorageService,
      coreToolsService,
      signpostingCmsService,
      getSelectionDataService
  );
  }

  describe('constructor', () => {

    it('component should be truthy', () => {
      spyOn(component as any, 'formatBetslipStakes');
      expect(component).toBeTruthy();
    });

    it('should ini flags', () => {
      expect(component.loadComplete).toBeFalsy();
      expect(component.loadFailed).toBeFalsy();
    });
    it('if config.maxPayOut is undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        maxPayOut: {}
      }));
      createComponent();
      expect(component.maxPayFlag).toBeUndefined();
      expect(component.maxPayMsg).toBeUndefined();
    });
    it('if config.restrictedHRMessages is undefined', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        restrictedHRMessages: {}
      }));
      createComponent();
      expect(component.restrictedHorseMsg).toBeUndefined();
      expect(component.restrictedRaceCardMsg).toBeUndefined();
    });
  });

  describe('defaultQuickDepositData', () => {
    it(`should return clear QuickDeposit Object `, () => {
      expect(component.defaultQuickDepositData).toEqual(jasmine.objectContaining({
        quickDepositPending: false,
        quickDepositFormAllowed: false,
        showQuickDepositForm: false,
        quickDepositFormExpanded: false,
        neededAmountForPlaceBet: undefined
      }));
    });
  });

  describe('@ngOnInit', () => {

    it('should call deviceService.getDeviceViewType', () =>{
      component.ngOnInit();
      expect(component.deviceViewType).toEqual(deviceViewType);
    });

    it('should set quickDepositService.config.userHasCreditCard as false', () => {
      component.ngOnInit();
      expect(component['bsButtonTitle']).toEqual('bs.betNow');
      expect(storageService.get).not.toHaveBeenCalledWith('overaskIsInProcess');
    });

    it('should call betslipSuccessfulLogin', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.reject());
      storageService.get.and.returnValue(false);
      component['betslipSuccessfulLogin'] = jasmine.createSpy();
      pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
        if (method.length && (method[0] === 'SUCCESSFUL_LOGIN' || method[1] === 'SESSION_LOGIN')) {
          callback('betslip');
        }
      });
      component.ngOnInit();
      tick();
      expect(component['betslipSuccessfulLogin']).toHaveBeenCalled();
      expect(storageService.get).toHaveBeenCalledWith('overaskIsInProcess');
      expect(betslipStorageService.cleanBetslip).not.toHaveBeenCalled();
    }));

    it('betslipSuccessfulLogin should run methods except for loginAndPlaceBets (status false)', () => {
      userService.bppToken = true;
      userService.status = false;
      component['init'] = jasmine.createSpy('component.init');
      component['activateOddsBoost'] = jasmine.createSpy('component.activateOddsBoost');
      component.quickDeposit.quickDepositFormExpanded = false;
      component.betslipSuccessfulLogin('');

      expect(component['init']).toHaveBeenCalled();
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.BETSLIP_COUNTER_UPDATE, 5);
      expect(component['activateOddsBoost']).toHaveBeenCalled();
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(component['quickDepositService']['config']['userHasCreditCard']).toBeFalsy();
      expect(component['bsButtonTitle']).toEqual('bs.betNowLogIn');
      expect(component['loginAndPlaceBets']).toBeFalsy();
    });

    it('betslipSuccessfulLogin should run methods except loginAndPlaceBets (place bet not betslip)', () => {
      userService.bppToken = true;
      userService.status = true;
      component['init'] = jasmine.createSpy('component.init');
      component['activateOddsBoost'] = jasmine.createSpy('component.activateOddsBoost');
      component.betslipSuccessfulLogin('');

      expect(component['init']).toHaveBeenCalled();
      expect(component['activateOddsBoost']).toHaveBeenCalled();
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(component['quickDepositService']['config']['userHasCreditCard']).toBeFalsy();
      expect(component['bsButtonTitle']).toEqual('bs.betNow');
      expect(component['loginAndPlaceBets']).toBeFalsy();
    });

    it('betslipSuccessfulLogin should run methods except loginAndPlaceBets (neededAmountForPlaceBet)', () => {
      userService.bppToken = true;
      userService.status = true;
      component['quickDeposit']['neededAmountForPlaceBet'] = '5';
      component['init'] = jasmine.createSpy('component.init');
      component['activateOddsBoost'] = jasmine.createSpy('component.activateOddsBoost');
      component.betslipSuccessfulLogin('betslip');

      expect(component['init']).toHaveBeenCalled();
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.BETSLIP_COUNTER_UPDATE, 5);
      expect(component['activateOddsBoost']).toHaveBeenCalled();
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(component['quickDepositService']['config']['userHasCreditCard']).toBeFalsy();
      expect(component['bsButtonTitle']).toEqual('bs.betNow');
      expect(component['loginAndPlaceBets']).toBeFalsy();
    });

    it('betslipSuccessfulLogin should run methods include loginAndPlaceBets', () => {
      userService.bppToken = true;
      userService.status = true;
      component['quickDeposit']['neededAmountForPlaceBet'] = '0.00';
      component['init'] = jasmine.createSpy('component.init');
      component['activateOddsBoost'] = jasmine.createSpy('component.activateOddsBoost');
      component.betslipSuccessfulLogin('betslip');

      expect(component['init']).toHaveBeenCalled();
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.BETSLIP_COUNTER_UPDATE, 5);
      expect(component['activateOddsBoost']).toHaveBeenCalled();
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(component['quickDepositService']['config']['userHasCreditCard']).toBeFalsy();
      expect(component['bsButtonTitle']).toEqual('bs.betNow');
      expect(component['loginAndPlaceBets']).toBeTruthy();
    });

    it('betslipSuccessfulLogin should run methods except init', () => {
      userService.bppToken = false;
      component['init'] = jasmine.createSpy('component.init');
      component['activateOddsBoost'] = jasmine.createSpy('component.activateOddsBoost');
      component.betslipSuccessfulLogin('betslip');

      expect(component['init']).not.toHaveBeenCalled();
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.BETSLIP_COUNTER_UPDATE, 5);
      expect(component['activateOddsBoost']).toHaveBeenCalled();
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(component['quickDepositService']['config']['userHasCreditCard']).toBeFalsy();
      expect(component['bsButtonTitle']).toEqual('bs.betNow');
      expect(component['loginAndPlaceBets']).toBeTruthy();
    });

    it('should call init fn firstly', () => {
      spyOn(component as any, 'init');
      component.ngOnInit();

      expect(component['init']).toHaveBeenCalled();
    });

    it('should sync with overask', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.reject());
      storageService.get.and.returnValue(true);
      userService.status = false;
      spyOn(component, 'cleanBetslip');
      component.ngOnInit();
      tick();

      pubSubService.publish('OVERASK_CLEAN_BETSLIP', {closeSlideOut: true, isOveraskCanceled: false});

      expect(component.cleanBetslip).toHaveBeenCalledWith(true, false);
      expect(storageService.get).toHaveBeenCalledWith('overaskIsInProcess');
      expect(betslipStorageService.cleanBetslip).toHaveBeenCalledWith(false, false);
      expect(betslipStorageService.clearStateInStorage).toHaveBeenCalled();
    }));

    it('should clear bet stake BETSLIP_CLEAR_STAKE', () => {
      component.ngOnInit();
      const allBets = [{
        Bet: {
          stake: {},
          betOffer: {}
        },
        id: 'SGL|100',
        stake: {
          perLine: '1'
        }
      }];
      component['getAllBets'] = () => allBets as IBetInfo[];
      component.placeSuspendedErr = {} as any;
      clearStakeCb('SGL|100');

      expect(betslipService.setAmount).toHaveBeenCalledWith(<any>allBets[0]);
    });

    it('should not clear bet stake BETSLIP_CLEAR_STAKE', () => {
      component.ngOnInit();
      const allBets = [];
      component['getAllBets'] = () => allBets as IBetInfo[];
      clearStakeCb('SGL|100');

      expect(betslipService.setAmount).not.toHaveBeenCalled();
    });

    it('should call method restoreOverask', () => {
      const spy = spyOn(component, 'restoreOveraskProcess');
      component.ngOnInit();

      expect(spy).toHaveBeenCalled();
    });

    it('should clear messages after Reload_Components', () => {
      let callback;
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'RELOAD_COMPONENTS') {
          callback = cb;
        }
      };

      component.ngOnInit();
      component.quickDeposit = {
        quickDepositPending: true
      } as IBetslipDepositData;
      callback();

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(component.quickDeposit.quickDepositPending).toBeFalsy();
      expect(component['rebuildBetslip']).toBeFalsy();
      expect(component['isAlreadyReloaded']).toBeFalsy();
    });

    it('should not do anything after Reload_Components if it is Receipt mode' , () => {
      let callback;
      component.overask.bsMode = 'Bet Receipt';
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'RELOAD_COMPONENTS') {
          callback = cb;
        }
      };

      component.ngOnInit();
      callback();

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
    });

    it('#should subscribe to events', () => {
      const estimatedReturn = 5;
      component.onCloseQuickDepositWindow = jasmine.createSpy('onCloseQuickDepositWindow');
      component.handleBetslipUpdate = jasmine.createSpy('handleBetslipUpdate');
      deviceService.isMobile = true;
      deviceService.deviceService = true;
      component['fetchedData'] = [];
      component['betslipService'].fetch = jasmine.createSpy('fetch').and.returnValue(of([]));
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => {
        // we need this condition here in order to avoid calling callbacks in superclass during test execution
        if (arg2 === 'BETSLIP_SIDE_BAR_MOTION') {
          callback(true);
        }
        if (arg2 === 'BETSLIP_UPDATED') {
          callback([]);
        }
        if (arg2 === 'show-slide-out-betslip-false' || arg2 === 'BETSLIP_COUNTER_UPDATE') {
          callback();
        }
        if (arg2 === 'BS_SELECTION_LIVE_UPDATE') {
          callback({
            info: jasmine.createSpy('info').and.returnValue({ id: 'SGL|1' }),
            history: {
              isPriceChanged: jasmine.createSpy('isPriceChanged'),
              isPriceChangedAndMarketUnsuspended: jasmine.createSpy('isPriceChangedAndMarketUnsuspended')
            }
          });
        }
      });
      component.totalEstReturns = jasmine.createSpy().and.returnValue(estimatedReturn);

      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BetSlipVanilla', [
        pubSubService.API.DIGIT_KEYBOARD_SHOWN,
        pubSubService.API['show-slide-out-betslip-false']
      ], jasmine.any(Function) );
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, pubSubService.API.BETSLIP_COUNTER_UPDATE, jasmine.any(Function));
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, pubSubService.API.BETSLIP_SIDE_BAR_MOTION, jasmine.any(Function));
      expect(component['betslipIsOpened']).toBe(true);

      priceUpdate.next(null);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(title, pubSubService.API['show-slide-out-betslip-true'], jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BetSlipVanilla', [
        pubSubService.API.DIGIT_KEYBOARD_SHOWN,
        pubSubService.API['show-slide-out-betslip-false']
      ], jasmine.any(Function) );
      expect(component.handleBetslipUpdate).toHaveBeenCalled();
    });

    it('should reload betslip after user presses "Reload"', () => {
      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, ['REFRESH_BETSLIP'], jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'SET_ODDS_FORMAT', jasmine.any(Function));
    });

    it('should set rebuildBetslip to false after calling this callback from overAsk SERVICE (totes should be fine)', () => {
      let callback;
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m[0] === 'REFRESH_BETSLIP') {
          callback = cb;
        }
      };
      component.ngOnInit();

      callback();
      expect(component['rebuildBetslip']).toBeFalsy();
    });

    it('Has panel message, no Bet data on show-slide-out-betslip-false', () => {
      let callback;
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'show-slide-out-betslip-false') {
         callback = cb;
        }
      };
      component.ngOnInit();
      component.quickDeposit = {} as any;
      component['betData'] = [{
        stake: {}
      }] as any;

      callback();
      expect(component.placeStakeErr).toBeFalsy();
    });
  });
  describe('onShowQuickDepositWindow', () => {
    beforeEach(() => {
      component.showIFrame = false;
      component['loadQuickDepositIfEnabled'] = jasmine.createSpy();
    });
    it('should open QuickDeposit iframe in case of authorized user has nullable balance and existing bets', () => {
      userService.sportBalance = '0';
      component['betData'] = [{}];
      component.isBoostEnabled = true;
      component.placeBetsPending  = false;
      const bet = {
        info: jasmine.createSpy('info').and.returnValue({ id: 'SGL|1',disabled:false }),
        oddsBoost: {}
      };
      sessionStorageService.get.and.callFake(
        (n) => {
          if(n === 'firstBetTutorial') { return {firstBetAvailable:true}} 
          else if(n === 'initialTabLoaded')  {return false}
          else if(n === 'firstBetTutorialAvailable'){ return false}
      });
      betslipDataService.bets = [{...bet}];
      component['onShowQuickDepositWindow']();

      expect(component.isZeroBalanceWithExistingBets).toBeTruthy();
      expect(component['loadQuickDepositIfEnabled']).toHaveBeenCalled();
    });
    it('should not open QuickDeposit iframe in case of authorized user has not nullable balance and existing bets', () => {
      userService.sportBalance  = '10';
      const bet = {
        info: jasmine.createSpy('info').and.returnValue({ id: 'SGL|1',disabled:false }),
        oddsBoost: {}
      };
      betslipDataService.bets = [{...bet}];
      component.placeBetsPending = false; 
      component.isBoostEnabled=true;
      sessionStorageService.get.and.callFake(
        (n) => {
          if(n === 'firstBetTutorial') { return {firstBetAvailable:true}} 
          else if(n === 'initialTabLoaded')  {return false}
          else if(n === 'firstBetTutorialAvailable'){ return false}
      });
      sessionStorageService.get.and.returnValue({firstBetAvailable:true});
      component['onShowQuickDepositWindow']();
      expect(component.isZeroBalanceWithExistingBets).toBeFalsy();
      expect(component['loadQuickDepositIfEnabled']).not.toHaveBeenCalled();
    });
    it('should not open QuickDeposit iframe in case of authorized user has not nullable balance and no bets', () => {
      userService.sportBalance  = '10';
      betslipDataService.bets = [];
      component['onShowQuickDepositWindow']();

      expect(component.isZeroBalanceWithExistingBets).toBeFalsy();
      expect(component['loadQuickDepositIfEnabled']).not.toHaveBeenCalled();
    });
    it('should not open QuickDeposit iframe in case of authorized user has nullable balance and no bets', () => {
      userService.sportBalance  = '0';
      betslipDataService.bets = [];
      component['onShowQuickDepositWindow']();

      expect(component.isZeroBalanceWithExistingBets).toBeFalsy();
      expect(component['loadQuickDepositIfEnabled']).not.toHaveBeenCalled();
    });

    it('should not open QuickDeposit iframe in case of user is not authorized', () => {
      userService.status = false;
      component['onShowQuickDepositWindow']();

      expect(component.isZeroBalanceWithExistingBets).toBeFalsy();
      expect(component['loadQuickDepositIfEnabled']).not.toHaveBeenCalled();
    });
  });
  describe('ngOnDestroy', () => {
    it('should set ca', () => {
      component.quickDeposit  = {quickDepositPending: true} as any;
      component.ngOnDestroy();

      expect(component['quickDepositService'].quickDepositCache).not.toBeUndefined();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
    });

    it('should call correct methods', () => {
      const notifyTimeout = 10;
      component.quickDeposit  = {quickDepositPending: false} as any;
      component['sub'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['quickDepositEnabledSub'] = new Subscription();
      component['quickDepositEnabledSub'].unsubscribe = jasmine.createSpy();
      component['notifyTimeout'] = notifyTimeout;
      component.ngOnDestroy();

      expect(component['quickDepositService'].quickDepositCache).toBeUndefined();
      expect(resolveService.reset).toHaveBeenCalledWith('betslip');
      expect(overAskService.clearBetsData).toHaveBeenCalled();
      expect(betslipLiveUpdateService.clearAllSubs).toHaveBeenCalled();
      expect(toteBetslipService.clear).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
      expect(component['quickDepositEnabledSub'].unsubscribe).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
    });
  });

  it('setFocusIndex', () => {
    component.setFocusIndex('test');

    expect(component['betType']).toEqual('test');
    expect(component.changedFromAllStakeField).toEqual(false);
  });

  it('debouncePlaceBets', fakeAsync(() => {
    component.placeBets = jasmine.createSpy().and.returnValue(of(null));
    component.ngOnInit();

    component.debouncePlaceBets();
    component.debouncePlaceBets();
    component.debouncePlaceBets();
    tick(1000);
    expect(component.placeBets).toHaveBeenCalledTimes(1);
  }));

  it('should call method restoreOveraskProcess', () => {
    const spyOnRestoreOverask = spyOn(component, 'restoreOveraskProcess');

    component.ngOnInit();

    expect(spyOnRestoreOverask).toHaveBeenCalled();
  });

  describe('callCallbackOpenLoginDialog', () => {
    it('isStake = false', () => {
      component['callCallbackOpenLoginDialog'](false);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, {
        placeBet: false, moduleName: 'betslip', action: jasmine.any(Function)
      });
    });
    it('isStake = true', () => {
      component['callCallbackOpenLoginDialog'](true);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, {
        placeBet: 'betslip',
        moduleName: 'betslip',
        action: jasmine.any(Function)
      });
    });
  });

  it('afterLoginHandler', () => {
    component['betslipSuccessfulLogin'] = jasmine.createSpy();
    component['afterLoginHandler']();
    expect(component['betslipSuccessfulLogin']).toHaveBeenCalledWith('betslip');
  });

  describe('pubSub LOGIN_POPUPS_END', () => {
    beforeEach(() => {
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((a, b, cb) => b === 'LOGIN_POPUPS_END' && cb && cb());
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['freeBetsService'].getFreeBetsState = jasmine.createSpy().and.returnValue({ available: true });

      component.loginAndPlaceBets = false;
      component['isLoginAndPlaceBetsInterrupted'] = true;
    });

    it('loginAndPlaceBets true', fakeAsync(() => {
      component.loginAndPlaceBets = true;
      component['onShowQuickDepositWindow'] = jasmine.createSpy();
      component.ngOnInit();
      tick();
      expect(component['popupsShown']).toBeFalsy();
      expect(component.loginAndPlaceBets).toBeFalsy();
      expect(component.placeBets).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalledWith('betSlipComponent=>placeBetRequest=>LOGIN_AND_PLACE_BET');
      expect(component['onShowQuickDepositWindow']).toHaveBeenCalled();
    }));

    it('loginAndPlaceBets false', fakeAsync(() => {
      component['init'] = jasmine.createSpy().and.returnValue(true);
      component.isShowQuickDepositBtnShown = jasmine.createSpy('isShowQuickDepositBtnShown').and.returnValue(false);

      component.ngOnInit();
      tick();
      expect(component['isLoginAndPlaceBetsInterrupted']).toBeFalsy();
      expect(component['init']).toHaveBeenCalled();
    }));

    it('loginAndPlaceBets and isShowQuickDepositBtnShown are false', fakeAsync(() => {
      component['init'] = jasmine.createSpy().and.returnValue(true);
      component.isShowQuickDepositBtnShown = jasmine.createSpy('isShowQuickDepositBtnShown').and.returnValue(true);

      component.ngOnInit();
      tick();
      expect(component['isLoginAndPlaceBetsInterrupted']).toBeTruthy();
    }));

    it('infoDialogComponent', () => {
      expect(component.infoDialogComponent).toEqual(SelectionInfoDialogComponent);
    });

    it('openSelectionInfoDialog', () => {
      const stake = <any>{
        price: {
          oldPrice: '1/11',
          priceDec: 1.123,
          priceNum: '1',
          priceDen: '11',
        }
      };
      component.openSelectionInfoDialog(stake);
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalled();
      expect(dialogService.openDialog).toHaveBeenCalledWith('selectionInfoDialog', undefined, true, jasmine.objectContaining({
        stake,
        odds: '1/11'
      }));
    });

    it('getFreeBetsState false', fakeAsync(() => {
      component['freeBetsService'].getFreeBetsState = jasmine.createSpy().and.returnValue({ available: false });

      component.ngOnInit();
      tick();
      expect(component['isLoginAndPlaceBetsInterrupted']).toBeTruthy();
    }));

    it('loginAndPlaceBets false', fakeAsync(() => {
      component['isLoginAndPlaceBetsInterrupted'] = false;
      component.ngOnInit();
      tick();
      expect(component['isLoginAndPlaceBetsInterrupted']).toBeFalsy();
    }));
  });

  describe('@init', () => {
    it('init(rebuildBetslip true, placeBetsPending true, overaskData - undefined)', fakeAsync(() => {
      component['clearOverlayMessage'] = jasmine.createSpy('clearOverlayMessage');
      component['storageService'].get = jasmine.createSpy('get').and.returnValue(['123']);
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betId'] = '123';
      component['rebuildBetslip'] = true;
      component.placeBetsPending = true;
      component['isAlreadyReloaded'] = true;

      component['init'](undefined, undefined, undefined);
      tick();

      expect(component['storageService'].remove).toHaveBeenCalledTimes(3);
      expect(component.placeBets).toHaveBeenCalled();
      expect(component['rebuildBetslip']).toBeFalsy();
      expect(component['clearOverlayMessage']).toHaveBeenCalled();
      expect(component['isAlreadyReloaded']).toBeFalsy();
    }));

    it('init(rebuildBetslip true, placeBetsPending false, overaskData - undefined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betslipService'].setPlaceBetPending(false);
      component['betslipService'].fetch = jasmine.createSpy('fetch').and.returnValue(of([]));

      component['rebuildBetslip'] = true;
      const getSpy = jasmine.createSpy().and.returnValue(false);
      Object.defineProperty(component['betslipService'], 'getPlaceBetPending', { get: getSpy });

      component['init'](undefined, undefined, undefined);
      tick();

      expect(component['rebuildBetslip']).toBeTruthy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('init(rebuildBetslip false, placeBetsPending true, overaskData - undefined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['rebuildBetslip'] = false;
      component['init'](undefined, undefined, undefined);
      tick();

      expect(component['rebuildBetslip']).toBeFalsy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('init(rebuildBetslip true, placeBetsPending true, overaskData - defined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betslipService'].setPlaceBetPending(true);
      component['rebuildBetslip'] = true;
      component['init'](undefined, undefined, { someOverAskData: 'someOverAskData' });
      tick();

      expect(component['rebuildBetslip']).toBeTruthy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('init(rebuildBetslip false, placeBetsPending false, overaskData - defined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betslipService'].setPlaceBetPending(false);
      component['rebuildBetslip'] = false;
      component['init'](undefined, undefined, { someOverAskData: 'someOverAskData' });
      tick();

      expect(component['rebuildBetslip']).toBeFalsy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('init(rebuildBetslip false, placeBetsPending true, overaskData - defined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betslipService'].setPlaceBetPending(true);
      component['rebuildBetslip'] = false;
      component['init'](undefined, undefined, { someOverAskData: 'someOverAskData' });
      tick();

      expect(component['rebuildBetslip']).toBeFalsy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('init(rebuildBetslip true, placeBetsPending false, overaskData - defined)', fakeAsync(() => {
      component.placeBets = jasmine.createSpy().and.returnValue(of(null));
      component['betslipService'].setPlaceBetPending(false);
      component['rebuildBetslip'] = true;
      component['init'](undefined, undefined, { someOverAskData: 'someOverAskData' });
      tick();

      expect(component['rebuildBetslip']).toBeTruthy();
      expect(component.placeBets).not.toHaveBeenCalled();
    }));

    it('should unsubscribe if subscription exist', fakeAsync(() => {
      const mockFetch = jasmine.createSpyObj('fetch', ['unsubscribe']);
      component['fetchSubscription'] = mockFetch;
      component['init']();
      expect(mockFetch.unsubscribe).toHaveBeenCalled();
    }));
    it('should not call unsubscribe if subscription not exist', fakeAsync(() => {
      const mockFetch = jasmine.createSpyObj('fetch', {
        unsubscribe: jasmine.createSpy(),
        closed: true
      });
      component['fetchSubscription'] = mockFetch;
      component['init']();
      expect(mockFetch.unsubscribe).not.toHaveBeenCalled();
    }));
    it('should handle if there are initialData and placeSuspendedErr', () => {
      component.isSelectionSuspended = true;
      pubSubService.subscribe.and.callFake((p1, p2, callback) => {
        if (p2 === 'BETSLIP_UPDATED') {
          callback([{
            legs: [{
              parts: [{
                outcome: {
                  prices: []
                }
              }]
            }],
            info: jasmine.createSpy().and.returnValue({
              type: '',
              stake: {
                perLine: '10',
                min: 1,
                params: { min: 1 }
              },
              errorMsg: ''
            }),
          }] as any);
        }
      });
      component.ngOnInit();
      expect(component.isSelectionSuspended).toBeTruthy();
    });

    it('should change component suspended state to false if there is not placeSuspendedErr', fakeAsync(() => {
      component['isSelectionSuspended'] = true;
      component['firstRunOfBetSlip'] = false;
      spyOn(component as any, 'core');
      component['placeSuspendedErr'] = null;
      component['isAlreadyReloaded'] = true;

      component['init']([]);
      tick();

      expect(component['isSelectionSuspended']).toBeFalsy();
      expect(component['isAlreadyReloaded']).toBeFalsy();
    }));

    it('should change component suspended state to false if there is not placeSuspendedErr msg', fakeAsync(() => {
      component['isSelectionSuspended'] = true;
      component['firstRunOfBetSlip'] = false;
      spyOn(component as any, 'core');
      component['placeSuspendedErr'] = {
        msg: '',
        disableBet: false,
        multipleWithDisableSingle: []
      };

      component['init']([]);
      tick();

      expect(component['isSelectionSuspended']).toBeFalsy();
    }));

    it('should check for stake status on suspended state', () => {
      component['checkStakeStatus'] = jasmine.createSpy('checkStakeStatus');
      component['firstRunOfBetSlip'] = false;

      component['init']([]);

      expect(component['checkStakeStatus']).toHaveBeenCalled();
    });
  });

  describe('pubSubService.API.HOME_BETSLIP', () => {
    it('should not reset quick deposit msg when open betslip receipt', () => {
      component.ngOnInit();
      homeBetslipCb('bet receipt');
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.HOME_BETSLIP, jasmine.any(Function));
      expect(component.hideEmptyBetslip).toBeFalsy();
    });
  });

  it('getAccatype', () => {
    localeService.getString.and.callFake(a => `${a} message`);

    expect(component.getAccatype({ type: 'test' } as any)).toEqual('bs.test message');
    expect(localeService.getString).toHaveBeenCalledWith('bs.test');
  });

  it('areToteBetsInBetslip', () => {
    expect(component.areToteBetsInBetslip()).toBeTruthy();
    expect(betslipDataService.containsRegularBets).toHaveBeenCalled();
    expect(toteBetslipService.isToteBetPresent).toHaveBeenCalled();
  });

  it('accaTemplate', () => {
    component.betSlipSingles = [];
    expect(component.accaTemplate(3, 3)).toEqual('acca-notification-3');
    expect(component.accaTemplate(0, 0)).toEqual('acca-notification-2');
    component.betSlipSingles = [{}, {}, {}];
    expect(component.accaTemplate(0, 5)).toEqual('acca-notification-1');
  });

  it('isSuccess', () => {
    expect(component.isSuccess(5, 0)).toBeTruthy();
    expect(component.isSuccess(5, 3)).toBeFalsy();
  });

  describe('getRunnerNumber', () => {
    beforeEach(() => {
      component.placeStakeErr = 'test';
      component['emptyStake'] = false;
    });

    it('truhy case #1', () => {
      component['betData'] = [{ handicapError: 1 }] as any;
      expect(component.hasErrors()).toBeTruthy();
      expect(component.placeStakeErr).toEqual(null);
      expect(component['emptyStake']).toBeFalsy();
    });

    it('truhy case #2', () => {
      component['betData'] = [{ handicapErrorMsg: 'test' }] as any;
      expect(component.hasErrors()).toBeTruthy();
      expect(component.placeStakeErr).toEqual(null);
      expect(component['emptyStake']).toBeFalsy();
    });

    it('truhy case #3', () => {
      component['betData'] = [{ error: 1 }] as any;
      expect(component.hasErrors()).toBeTruthy();
      expect(component.placeStakeErr).toEqual(null);
      expect(component['emptyStake']).toBeFalsy();
    });

    it('truhy case #4', () => {
      component['betData'] = [{ errorMsg: 'test' }] as any;
      expect(component.hasErrors()).toBeTruthy();
      expect(component.placeStakeErr).toEqual(null);
      expect(component['emptyStake']).toBeFalsy();
    });

    it('truhy case #5', () => {
      component.placeSuspendedErr = { msg: 'test' } as any;
      expect(component.hasErrors()).toBeTruthy();
      expect(component.placeStakeErr).toEqual(null);
      expect(component['emptyStake']).toBeFalsy();
    });

    it('falsy case', () => {
      component.placeSuspendedErr = { msg: 'test' } as any;
      component['emptyStake'] = true;
      expect(component.hasErrors()).toBeFalsy();
    });
  });

  
  it("should replace comma stakePerLine", () => {
    component.toteBetSlip = {
      toteBet: {
        poolBet: {stakePerLine: "12"}
      } 
    } as any
      component.toteBetSlip.toteBet.poolBet.stakePerLine = "1.2";
      component.setStake();
      expect(component.toteBetSlip.toteBet.poolBet.stakePerLine).toEqual("1.2");
  })

  it("should replace comma stakePerLine", () => {
    component.allStakes.value = "1.2";
    component.setSingleStake();
    expect(component.allStakes.value).toEqual("1.2");
})

  describe('calculateIsBetsSelected', () => {
    it('should set true', () => {
      component.isOveraskCanBePlaced = undefined;
      const bets = [{ isSelected: true }, { isSelected: false }] as any;
      component['getAllBets'] = jasmine.createSpy('getAllBets').and.returnValue(bets);
      component['calculateIsBetsSelected']();

      expect(component.isBetsSelected).toEqual(true);
      expect(component.isOveraskCanBePlaced).toEqual(true);
      expect(overAskService.isOveraskCanBePlaced).toHaveBeenCalled();
    });

    it('should set false if no selected bets', () => {
      component.isOveraskCanBePlaced = undefined;
      const bets = [{ isSelected: null }] as any;
      component['getAllBets'] = jasmine.createSpy('getAllBets').and.returnValue(bets);
      component['calculateIsBetsSelected']();

      expect(component.isBetsSelected).toEqual(false);
    });

    it('should set false if selected bets are disabled', () => {
      component.isOveraskCanBePlaced = undefined;
      const bets = [{ isSelected: true, disabled: true }] as any;
      component['getAllBets'] = jasmine.createSpy('getAllBets').and.returnValue(bets);
      component['calculateIsBetsSelected']();

      expect(component.isBetsSelected).toEqual(false);
    });
  });

  describe('@ngOnInit', () => {

    it('should create BetslipComponent instance', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.LOGIN_POPUPS_START, jasmine.any(Function));
    });

    it('should hide overask message after another user is logged in (quickDeposit.quickDepositPending should be false)', () => {
      component.ngOnInit();
      component.quickDeposit.quickDepositPending = true;

      expect(component.quickDeposit.quickDepositPending).toBeTruthy();
      pubSubService.publish(pubSubService.API.SESSION_LOGOUT);
    });

    it('should re-set firstRunOfBetSlip after login', () => {
      // @ts-ignore
      component['userService'].status = false;
      pubSubService.subscribe = jasmine.createSpy().and.callFake((p1, p2, callback) => {
        callback();
      });
      expect(component['firstRunOfBetSlip']).toBe(true);
    });

    it('should call this.init() after login', () => {
      spyOn(component as any, 'init');
      component.ngOnInit();
      pubSubService.publish(pubSubService.API.SUCCESSFUL_LOGIN);
      expect(component['init']).toHaveBeenCalled();
    });

    it('should call this.init() after logout', () => {
      spyOn(component as any, 'init');
      component.ngOnInit();
      pubSubService.publish(pubSubService.API.SESSION_LOGOUT);
      expect(component['init']).toHaveBeenCalled();
    });

    it('@init - should init quick deposit when first run of betslip', () => {
      betslipStakeService.getStake.and.returnValue(0);
      betslipStakeService.getFreeBetStake.and.returnValue(0);
      betslipService.fetch.and.returnValue(of(null));
      const getSpy = jasmine.createSpy().and.returnValue('false');
      Object.defineProperty(component['betslipService'], 'getPlaceBetPending', { get: getSpy });
      component['firstRunOfBetSlip'] = true;

      component['init'](false);
      expect(component['firstRunOfBetSlip']).toBeTruthy();
      expect(quickDepositService.checkQuickDeposit).not.toHaveBeenCalled();
    });

    it('@init - should not init quick deposit when deposit registered page is opened', () => {
      betslipStakeService.getStake.and.returnValue(0);
      betslipStakeService.getFreeBetStake.and.returnValue(0);
      betslipService.fetch.and.returnValue(of(null));
      const getSpy = jasmine.createSpy().and.returnValue('false');
      Object.defineProperty(component['betslipService'], 'getPlaceBetPending', { get: getSpy });
      component['firstRunOfBetSlip'] = true;
      component['routingState'].getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('deposit.registered');

      component['init'](false);
      expect(component['firstRunOfBetSlip']).toBeTruthy();
    });

    it('@init - should not init quick deposit when withdraw page is opened', () => {
      betslipStakeService.getStake.and.returnValue(0);
      betslipStakeService.getFreeBetStake.and.returnValue(0);
      betslipService.fetch.and.returnValue(of(null));
      const getSpy = jasmine.createSpy().and.returnValue('false');
      Object.defineProperty(component['betslipService'], 'getPlaceBetPending', { get: getSpy });
      component['firstRunOfBetSlip'] = true;
      component['routingState'].getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('withdraw');

      component['init'](false);
      expect(component['firstRunOfBetSlip']).toBeTruthy();
    });

    describe('SESSION_LOGOUT', () => {
      const testStr = 'TestString';

      it(`should remove 'betReceiptService.message' if it's deposit related msg`, () => {
        component['betReceiptService'].message.msg = testStr;
        localeService.getString.and.returnValue(testStr);
        component.ngOnInit();
        pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

        expect(component['betReceiptService'].message.msg).not.toBeDefined();
      });

      it(`should Not remove 'betReceiptService.message' if it's Not deposit related msg`, () => {
        component['betReceiptService'].message.msg = testStr;
        localeService.getString.and.returnValue('str');

        component.ngOnInit();

        expect(component['betReceiptService'].message.msg).toEqual(testStr);
      });

      describe('skip logic', () => {

        beforeEach(() => {
          component.ngOnInit();
          spyOn(component as any, 'init');
        });

        it('first run', () => {
          component['firstRunOfBetSlip'] = true;
          component.loadComplete = false;
          component.loadFailed = false;
          pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

          expect(component['init']).not.toHaveBeenCalled();
        });

        it('failed load', () => {
          component['firstRunOfBetSlip'] = true;
          component.loadComplete = false;
          component.loadFailed = true;
          pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

          expect(component['init']).toHaveBeenCalledTimes(1);
        });

        it('successfully loaded', () => {
          component['firstRunOfBetSlip'] = true;
          component.loadComplete = true;
          component.loadFailed = false;
          pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

          expect(component['init']).toHaveBeenCalledTimes(1);
        });

        it('failed but finished load', () => {
          component['firstRunOfBetSlip'] = true;
          component.loadComplete = true;
          component.loadFailed = true;
          pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

          expect(component['init']).toHaveBeenCalledTimes(1);
        });

        it('loading in progress (first run)', () => {
          component['firstRunOfBetSlip'] = false;
          component.loadComplete = false;
          component.loadFailed = false;
          pubSubService.publish(pubSubService.API.SESSION_LOGOUT);

          expect(component['init']).toHaveBeenCalledTimes(1);
        });
      });
    });

    describe('OVERASK_BETS_DATA_UPDATED subscription', () => {

      beforeEach(() => {
        component.ngOnInit();

        spyOn(component as any, 'core');
        spyOn(component as any, 'scrollToActionButtons');
      });

      it('should skip data update if not yet initialized', () => {
        pubSubService.publish('OVERASK_BETS_DATA_UPDATED');

        expect(component['core']).not.toHaveBeenCalled();
      });

      it('should process data update', () => {
        component['fetchedData'] = [{}] as any;
        pubSubService.publish('OVERASK_BETS_DATA_UPDATED');

        expect(component['core']).toHaveBeenCalledWith([{}]);
      });
      it('should process data update', () => {
        component['overaskMessage'] = true;
       
      });
    });

  });

  it('should get sport event time/date', () => {
    component.getStakeTime('testTime');
    expect(timeService.getEventTime).toHaveBeenCalledWith('testTime');
  });

  describe('@removeToteBet', () => {
    it('should call toteBetslipService.removeToteBet with params', () => {

      component.removeToteBet(true, false);
      expect(toteBetslipService.removeToteBet).toHaveBeenCalledWith(true, false);
    });

    it('should set null for toteBetGeneralError', () => {
      component.toteBetGeneralError = {};
      component.removeToteBet();
      expect(component.toteBetGeneralError).toBeNull();
    });
  });

  describe('@placeBets', () => {
    it('should set PlaceBetsPending to false ', fakeAsync(() => {
      component.placeBetsPending = true;
      component.toteBetGeneralError = true;
      // @ts-ignore
      component['userService'].status = true;
      component['isFreeBetApplied'] = false;
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.placeBet.and.returnValue(throwError({ msg: 'error message' }));
      component.placeBets().subscribe(null, () => {
        expect(toteBetslipService.placeBet).toHaveBeenCalled();
        expect(component.toteBetGeneralError).toEqual(null);
        expect(betslipService.setPlaceBetPending).toHaveBeenCalledWith(false);
        expect(component.placeBetsPending).toEqual(false);
      });

      flush();
    }));

    it('should set isBetSlipEmpty as true', fakeAsync(() => {
      
      const betPlacementResponse = {
        betPlacement: [{ betId: '123' }]
      };
      storageService.get = (key) => {
        if(key === 'toteFreeBets') {
          return [
            {freebetTokenId: 1}
          ]
        } else if(key === 'toteBetPacks') {
          return [
            {freebetTokenId: 1}
          ]
        } else{
          return {
            poolBet: { freebetTokenId: 1}
          }
        }
      };
      component['freeBetsService'].getFreeBetsState = jasmine.createSpy().and.returnValue({data: [],betTokens: [], fanZone: []});
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.placeBet.and.returnValue(of(betPlacementResponse));
      component.betSlipSingles = [];
      component.usedTotefreebetsList = [];
      component.hideEmptyBetslip = false;
      component.placeBets().subscribe();
      component['isFreeBetApplied'] = true;
      tick(1000);
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(component.isBetSlipEmpty).toBe(true);
      expect(component.hideEmptyBetslip).toBe(true);
      storageService.get = (key) => {
        if(key === 'toteBetPacks') {
          return [
            {freebetTokenId: 1}
          ]
        } else if(key === 'toteFreeBets') {
          return [];
        } else {
          return {
            freebetTokenId: 1,
            poolBet: {
              freebetTokenId: 1,
              betType: 'BET TOKEN'
            }
          }
        }
      };
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.placeBet.and.returnValue(of(betPlacementResponse));
      component.betSlipSingles = [];
      component.hideEmptyBetslip = false;
      component.placeBets().subscribe();
      component['isFreeBetApplied'] = true;
      tick(1000);
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(component.isBetSlipEmpty).toBe(true);
      expect(component.hideEmptyBetslip).toBe(true);
      storageService.get = (key) => {
        if(key === 'toteBetPacks') {
          return [
            {freebetTokenId: 1}
          ]
        } else if(key === 'toteFreeBets') {
          return [];
        } else {
          return {
            freebetTokenId: 1,
            poolBet: {
              freebetTokenId: 1,
              betType: 'BET TOKEN'
            }
          }
        }
      };
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.placeBet.and.returnValue(of(betPlacementResponse));
      component.betSlipSingles = [];
      component.hideEmptyBetslip = false;
      component.placeBets().subscribe();
      component['isFreeBetApplied'] = true;
      tick(1000);
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(component.isBetSlipEmpty).toBe(true);
      expect(component.hideEmptyBetslip).toBe(true);
    }));

    it('should do reboost', fakeAsync(() => {
      component['betslipErrorTracking'] = jasmine.createSpy('betslipErrorTracking');
      component['toteBetCanBePlaced'] = jasmine.createSpy().and.returnValue(false);
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      component['checkAmount'] = jasmine.createSpy().and.returnValue(true);
      component['updatePlaceBetsPending'] = jasmine.createSpy('updatePlaceBetsPending');
      component['clearUserValueForDisabledBets'] = jasmine.createSpy('clearUserValueForDisabledBets');
      component['placeBetsResponseProcess'] = jasmine.createSpy('placeBetsResponseProcess');
      component.quickDeposit = component.defaultQuickDepositData;
      component.betSlipSingles = [];
      component.lottobetslipData = [];
      component['isFreeBetApplied'] = true;
      component.placeBets().subscribe();
      tick(1000);

      expect(awsService.addAction).toHaveBeenCalledWith('betSlipComponent=>placeBetResponse=>Success', { result: {} });
      expect(component['updatePlaceBetsPending']).toHaveBeenCalled();
      expect(component['clearUserValueForDisabledBets']).toHaveBeenCalled();
    }));

    it('should quit because of reboost', fakeAsync(() => {
      component['toteBetCanBePlaced'] = jasmine.createSpy().and.returnValue(false);
      component['checkAmount'] = jasmine.createSpy().and.returnValue(true);
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      component['init'] = jasmine.createSpy('init');
      component.quickDeposit = component.defaultQuickDepositData;
      component.betSlipSingles = [];
      component['isFreeBetApplied'] = true;
      component['rebuildBetslip'] = true;
      component.isBoostActive = true;
      component.showPriceChangeNotification = () => true;

      component.placeBets().subscribe();
      tick(1000);

      expect(component['init']).toHaveBeenCalled();
    }));

    it('no reboost isBoostActive false', fakeAsync(() => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      component['betslipErrorTracking'] = jasmine.createSpy('betslipErrorTracking');
      component['toteBetCanBePlaced'] = jasmine.createSpy().and.returnValue(false);
      component['checkAmount'] = jasmine.createSpy().and.returnValue(true);
      component['init'] = jasmine.createSpy('init');
      component.quickDeposit = component.defaultQuickDepositData;
      component.betSlipSingles = [];
      component['isFreeBetApplied'] = true;
      component['rebuildBetslip'] = true;
      component.isBoostActive = false;
      component.lottobetslipData = [];
      component.placeBets().subscribe();
      tick(1000);

      expect(component['init']).not.toHaveBeenCalled();
    }));

    it('no reboost rebuildBetslip false', fakeAsync(() => {
      component['toteBetCanBePlaced'] = jasmine.createSpy().and.returnValue(false);
      toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
      component['checkAmount'] = jasmine.createSpy().and.returnValue(true);
      component['init'] = jasmine.createSpy('init');
      component.quickDeposit = component.defaultQuickDepositData;
      component.betSlipSingles = [];
      component.toteFreeBetSelected = false;

      component['rebuildBetslip'] = false;
      component.isBoostActive = true;
      component.lottobetslipData = [];
      component.placeBets().subscribe();
      tick(1000);

      expect(component['init']).not.toHaveBeenCalled();
    }));
    it('should throw default error', () => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      component['isFreeBetApplied'] = false;
      component.placeBets().subscribe(null, e => {
        expect(e).toEqual('Betslip cannot proceed with bet placement');
      });
    });

    it('should throw error when User is not logged in', () => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      userService.status = false;
      component['isFreeBetApplied'] = true;
      component.placeBets().subscribe(null, e => {
        expect(e).toEqual('Betslip cannot proceed with bet placement: Unauthorized access');
      });
    });

    it('should throw error when device is not online', () => {
      deviceService.isOnline = () => false;
      component['isFreeBetApplied'] = true;
      component.placeBets().subscribe(null, e => {
        expect(e).toEqual('Betslip cannot proceed with bet placement: Device is not online');
      });
    });

    it('check amount failed', () => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
      component.quickDeposit = {} as any;
      component['isFreeBetApplied'] = true;
      component.placeBets();
      expect(component.quickDeposit.quickDepositPending).toBeFalsy();
      expect(component.placeBetsPending).toBeFalsy();
    });

    it('check amount and delay on error', fakeAsync(() => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
      betslipService.areBetsWithStakes.and.returnValue(true);
      betslipService.placeBets.and.returnValue(of({ errs: [{}] }));
      component['isFreeBetApplied'] = true;
      component['betData'] = [{
        stake: { perLine: 2, min: 1 }
      }] as any;
      component.quickDeposit = {} as any;
      component.betSlipSingles = [];
      component.lottobetslipData = [];
      component['betslipErrorTracking'] = () => { };
      Object.defineProperty(component, 'BPP_TIMEOUT_ERROR', { value: 0 });

      component.placeBets().subscribe();
      tick();

      expect(component['firstRunOfBetSlip']).toBeTruthy();
    }));

    it('check amount and catch error', fakeAsync(() => {
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
      betslipService.areBetsWithStakes.and.returnValue(true);
      component['betData'] = [{
        stake: { perLine: 2, min: 1 }
      }] as any;
      component.quickDeposit = {} as any;
      component.betSlipSingles = [];
      component['isFreeBetApplied'] = false;
      component['betslipErrorTracking'] = () => { };
      component.lottobetslipData = [];
      betslipService.placeBets.and.returnValue(throwError(null));
      component.placeBets().subscribe(null, () => { });
      tick();

      betslipService.placeBets.and.returnValue(throwError({}));
      component.placeBets().subscribe(null, () => { });
      tick();

      expect(awsService.addAction).toHaveBeenCalledTimes(2);
    }));

    it('check amount and throwError data for lotto', fakeAsync(() => {
      component['betslipErrorTracking'] = jasmine.createSpy('betslipErrorTracking');
      component['toteBetCanBePlaced'] = jasmine.createSpy().and.returnValue(false);
      toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
      jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      component['checkAmount'] = jasmine.createSpy().and.returnValue(true);
      component['updatePlaceBetsPending'] = jasmine.createSpy('updatePlaceBetsPending');
      component['clearUserValueForDisabledBets'] = jasmine.createSpy('clearUserValueForDisabledBets');
      component['placeBetsResponseProcess'] = jasmine.createSpy('placeBetsResponseProcess');
      component.quickDeposit = component.defaultQuickDepositData;
      component['betData'] = [{isLotto:true,accaBets:[{stake:0.01}]}] as any;
      component.betSlipSingles = [];
      component.lottobetslipData = component['betData'];
      component['isFreeBetApplied'] = true;
      component.toteFreeBetSelected = true;
      component.placeBets().subscribe();
      tick(1000);

      expect(awsService.addAction).toHaveBeenCalledWith('betSlipComponent=>placeBetResponse=>Success', { result: {} });
      expect(component['updatePlaceBetsPending']).toHaveBeenCalled();
      expect(component['clearUserValueForDisabledBets']).toHaveBeenCalled();
    }));
  });

  describe('@onDidigitKeyboardInit', () => {
    it('should set isDidigitKeyboardInit as true', () => {
      component.onDidigitKeyboardInit();
      expect(component.isDidigitKeyboardInit).toEqual(true);
    });
  });

  describe('@navigateToUpgrade', () => {
    let gtmData;
    beforeAll(() => {
      gtmData = {
        event: 'trackEvent',
        eventCategory: 'cta',
        eventAction: 'upgrade account',
        eventLabel: 'yes - upgrade Account'
      };
    });

    it('when retailCard is defined', () => {
      userService.getRetailCard.and.returnValue({});
      component.navigateToUpgrade();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.UPGRADE_FROM_BETSLIP);
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });

    it('when retailCard is NOT defined', () => {
      userService.getRetailCard.and.returnValue(null);
      component.navigateToUpgrade();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.UPGRADE_FROM_BETSLIP);
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
  });

  describe('@placeBets', () => {
    jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([{freebetTokenId:'1',freebetOfferName:'test'}]);
    it('should return Observable', () => {
      component['isFreeBetApplied'] = true;
      expect(component.placeBets()).toEqual(jasmine.any(Observable));
    });
  });

  describe('@placeBets, stakePerLine Octal fix', () => {
     jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
    it('should change stakePerLine', () => {
      component['isFreeBetApplied'] = true;
      toteBetslipService.toteBet = {poolBet: {stakePerLine: '010'}};
      component.placeBets();
      expect(toteBetslipService.toteBet.poolBet.stakePerLine).toEqual(10);
    });

    it('should Not change stakePerLine, case 1', () => {
       jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
       component['isFreeBetApplied'] = true;
      toteBetslipService.toteBet = {};
      component.placeBets();
      expect(toteBetslipService.toteBet.poolBet).toBeUndefined();
    });

    it('should Not change stakePerLine, case 2', () => {
     jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
     component['isFreeBetApplied'] = false;
      toteBetslipService.toteBet = {poolBet: {}};
      component.placeBets();
      expect(toteBetslipService.toteBet.poolBet.stakePerLine).toBeUndefined();
    });

    it('should Not change stakePerLine, case 3', () => {
      component['freeBetsStoreUpdate'] = jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService = {};
      component['isFreeBetApplied'] = false;
      component.placeBets();
      expect(toteBetslipService.toteBet).toBeUndefined();
    });

    it('should Not change stakePerLine, case 4', () => {
      component['freeBetsStoreUpdate'] = jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
      toteBetslipService = undefined;
      component['isFreeBetApplied'] = false;
      component.placeBets();
      expect(toteBetslipService).toBeUndefined();
    });
  });

  describe('@placeBetsResponseProcess', () => {
    beforeEach(() => {
      component.quickDeposit = component.defaultQuickDepositData;
      component['stakeErrorParser'] = jasmine.createSpy('stakeErrorParser');
      component['betslipErrorTracking'] = jasmine.createSpy('betslipErrorTracking');
    });

    it('placeBetsResponseProcess with error and without error - rebuildBetslip should be false', () => {
      component['placeBetsResponseProcess']({});
      expect(component['rebuildBetslip']).toBeFalsy();

      component['placeBetsResponseProcess']({ errs: [] });
      expect(component['rebuildBetslip']).toBeFalsy();
    });

    it('placeBetsResponseProcess no error', () => {
      component['placeBetsResponseProcess']({});

      expect(component['betslipErrorTracking']).not.toHaveBeenCalled();
      component['placeBetsResponseProcess']({ errs: [] });
      expect(component['betslipErrorTracking']).not.toHaveBeenCalled();
      component['placeBetsResponseProcess']({ errs: [{ subCode: '', errorDesc: '' }] });
      expect(component['betslipErrorTracking']).toHaveBeenCalled();
      expect(localeService.getString).not.toHaveBeenCalledWith('bs.depositAndPlacebetSuccessMessage');
      expect(component.quickDeposit.showQuickDepositForm).toBeFalsy();
      expect(component.hideEmptyBetslip).toBeTruthy();
    });

    it('after quick deposit call', () => {
      component['placeBetsResponseProcess']({}, true);

      expect(localeService.getString).toHaveBeenCalledWith('bs.depositAndPlacebetSuccessMessage');
      expect(component.quickDeposit.showQuickDepositForm).toBeTruthy();
    });

    describe('check claimedOffers', () => {
      beforeEach(() => {
        component['hasClaimedOffersForBIRBets'] = jasmine.createSpy('hasClaimedOffersForBIRBets').and.returnValue(true);
      });

      it('should call getFreeBets iff bets provider equals BIR', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "11"}]}],
            id: 3
          }]
        };
        storageService.get = jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
        

        component['placeBetsResponseProcess'](result);
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });

      it('should call getFreeBets if bets has claimedOffers', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "11"}]}]
          }]
        };
        storageService.get = jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
        component['placeBetsResponseProcess'](result);
        expect(component['hasClaimedOffersForBIRBets']).toHaveBeenCalled();
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });

      it('should call getFreeBets if event Id is undefined', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "5"}]}]
          }]
        };
        storageService.get = jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
        component['placeBetsResponseProcess'](result);
        expect(component['hasClaimedOffersForBIRBets']).toHaveBeenCalled();
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });

      
      it('should call if local storage does not exist', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "11"}]}]
          }]
        };
        storageService.get = jasmine.createSpy().and.returnValue(false);
        component['placeBetsResponseProcess'](result);
        expect(component['hasClaimedOffersForBIRBets']).toHaveBeenCalled();
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });

      it('should call if local storage is empty', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "11"}]}]
          }]
        };
        storageService.get = jasmine.createSpy().and.returnValue([]);
        component['placeBetsResponseProcess'](result);
        expect(component['hasClaimedOffersForBIRBets']).toHaveBeenCalled();
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });

      it('should call if local storage is null', () => {
        const result = {
          bets: [{
            leg: [ {'part':[{eventId: "11"}]}]
          }]
        };
        storageService.get = jasmine.createSpy().and.returnValue(null);
        component['placeBetsResponseProcess'](result);
        expect(component['hasClaimedOffersForBIRBets']).toHaveBeenCalled();
        expect(component['freeBetsService'].getFreeBets).toHaveBeenCalled();
      });
    });

    describe('should not update betCounter', () => {
      it('should not update betCounter, when result does not contain bets', () => {
        component['placeBetsResponseProcess']({ });
        expect(pubSubService.publish).toHaveBeenCalledWith('HOME_BETSLIP', '');
      });
      it('when result is errorsome', () => {
        component['placeBetsResponseProcess']({ errs: [{ code: 'code' }] });
        expect(pubSubService.publish).not.toHaveBeenCalled();
      });
    });
  });

  it('isStakeBoostAvailable', () => {
    component['userService'] = { status: true } as any;
    component.isBoostEnabled = true;
    component.isBoostActive = true;
    const stake: any = {
      isSP: false,
      isSPLP: false,
      price: {
        priceType: 'LP'
      },
      pricesAvailable: false,
      disabled: false,
      Bet: { oddsBoost: true }
    };

    expect(component.isStakeBoostAvailable(stake)).toBeTruthy();

    stake.disabled = true;
    expect(component.isStakeBoostAvailable(stake)).toBeFalsy();

    stake.disabled = false;
    stake.isSP = true;
    expect(component.isStakeBoostAvailable(stake)).toBeFalsy();

    stake.disabled = false;
    stake.isSP = false;
    stake.Bet.oddsBoost = false;
    expect(component.isStakeBoostAvailable(stake)).toBeFalsy();

    stake.disabled = false;
    stake.isSP = false;
    stake.Bet.oddsBoost = true;
    stake.isSPLP = true;
    stake.price.priceType = 'SP';
    expect(component.isStakeBoostAvailable(stake)).toBeFalsy();

    stake.disabled = false;
    stake.isSP = false;
    stake.Bet.oddsBoost = true;
    stake.isSPLP = true;
    stake.price.priceType = 'Lp';
    stake.pricesAvailable = true;
    expect(component.isStakeBoostAvailable(stake)).toBeTruthy();
    
  });

  it('getBoostedOldPrice', () => {
    const stake: any = {}, type = 'single';
    component.getBoostedOldPrice(stake, type);
    expect(commandService.execute).toHaveBeenCalledWith(commandService.API.ODDS_BOOST_OLD_PRICE, [stake, type]);
  });

  it('getBoostedNewPrice', () => {
    const stake: any = {}, type = 'single';
    component.getBoostedNewPrice(stake, type);
    expect(commandService.execute).toHaveBeenCalledWith(commandService.API.ODDS_BOOST_NEW_PRICE, [stake, type]);
  });

  describe('@subscribeToOddsBoostChange', () => {

    it('(default)', fakeAsync(() => {
      component['maxStakeExceeded'] = () => false;
      component['isFreeBetSelected'] = () => true;
      component.betSlipSingles = [{
        Bet: {
          oddsBoost: {
            betBoostMaxStake: '10'
          }
        }
      }];
      commandService.execute['calls'].reset();
      component.betSlipMultiples = [];
      component.isBoostActive = true;
      component['subscribeToOddsBoostChange']();

      tick();

      expect(commandService.execute['calls'].argsFor(0)).toEqual(['ODDS_BOOST_SET_MAX_VAL', ['10']]);
      expect(commandService.execute['calls'].argsFor(1)).toEqual(['ODDS_BOOST_SHOW_FB_DIALOG', [false, 'betslip']]);

      expect(component.isBoostActive).toBeTruthy();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'ODDS_BOOST_CHANGE', jasmine.any(Function));

      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'ADDTOBETSLIP_PROCESS_FINISHED', jasmine.any(Function));
    }));

    it('subscribeToOddsBoostChange (boost deactivated)', fakeAsync(() => {
      component.betSlipSingles = [];
      component.isBoostActive = true;
      component['isFreeBetSelected'] = jasmine.createSpy().and.returnValue(false);
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((p1, p2, cb) => cb(false));
      component['pubSubService'].subscribe['calls'].reset();
      commandService.execute['calls'].reset();

      component['subscribeToOddsBoostChange']();
      tick();

      expect(component.isBoostActive).toBeFalsy();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'ODDS_BOOST_CHANGE', jasmine.any(Function));
      expect(commandService.execute).not.toHaveBeenCalledWith(
        'ODDS_BOOST_SHOW_FB_DIALOG', [false, 'betslip']
      );
    }));

    it('should decrement oddsboost counter for vanilla menu after betplacement', fakeAsync(() => {
      component.isBoostActive = true;
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((componentName, event, callback) => {
        if (event === pubSubService.API.BETS_COUNTER_PLACEBET) {
          callback();

          expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.ODDS_BOOST_DECREMENT_COUNTER);
        }
      });

      component['subscribeToOddsBoostChange']();
      tick();
    }));

    it('should not decrement oddsboost counter for vanilla menu after betplacement if oddsboost was not used', fakeAsync(() => {
      component.isBoostActive = false;
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((componentName, event, callback) => {
        if (event === pubSubService.API.BETS_COUNTER_PLACEBET) {
          callback();

          expect(pubSubService.publish).not.toHaveBeenCalled();
        }
      });

      component['subscribeToOddsBoostChange']();
      tick();
    }));

    it('subscribeToOddsBoostChange no odds boost', () => {
      component.betSlipSingles = [{ Bet: { oddsBoost: null } }];
      component.betSlipMultiples = [];
      pubSubService.publish['calls'].reset();

      component['subscribeToOddsBoostChange']();

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('(reboost)', fakeAsync(() => {
      component.isBoostActive = true;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((p1, p2, cb) => p2 === 'ODDS_BOOST_REBOOST' && cb(false));

      component['subscribeToOddsBoostChange']();
      tick();

      expect(component['rebuildBetslip']).toBeTruthy();
      expect(component['reboost']).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith('bs.reboostPriceChangeBannerMsg');
    }));

    it('subscribeToOddsBoostChange (reboost false)', fakeAsync(() => {
      component.isBoostActive = false;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((p1, p2, cb) => p2 === 'ODDS_BOOST_REBOOST' && cb(false));
      component['subscribeToOddsBoostChange']();
      tick();

      expect(component['rebuildBetslip']).toBeTruthy();
      expect(component['reboost']).toBeFalsy();
      expect(localeService.getString).not.toHaveBeenCalled();
    }));

    it('activateOddsBoost (logged out)', () => {
      component['cmsService'].getOddsBoost = jasmine.createSpy();
      component['userService'] = { status: false } as any;
      component.activateOddsBoost();
      expect(component['cmsService'].getOddsBoost).not.toHaveBeenCalled();
    });

    it('activateOddsBoost (logged in, boost disalbed)', fakeAsync(() => {
      component['cmsService'].getOddsBoost = jasmine.createSpy().and.returnValue(of({ enabled: false }));
      component['userService'] = { status: true } as any;

      component.activateOddsBoost();
      tick();

      expect(cmsService.getOddsBoost).toHaveBeenCalled();
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    }));

    it('activateOddsBoost (logged in, boost enabled)', fakeAsync(() => {
      component['unsetFreeBets'] = jasmine.createSpy();
      component['cmsService'].getOddsBoost = jasmine.createSpy().and.returnValue(of({ enabled: true }));
      component['userService'] = { status: true } as any;
      component['subscribeToOddsBoostChange'] = jasmine.createSpy();

      component.activateOddsBoost();
      tick();

      expect(cmsService.getOddsBoost).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_ODDS_BOOST_ACTIVE');
      expect(component['subscribeToOddsBoostChange']).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'ODDS_BOOST_UNSET_FREEBETS', jasmine.any(Function));
    }));

    it('setFreebet (freebet selected)', () => {
      component['clearSingleBetPriceChangeErr'] = jasmine.createSpy();
      component['setMultipleSuspendedErrMsg'] = jasmine.createSpy();
      component['priceChangeCount'] = 1;
      component['commandService'].execute = jasmine.createSpy();
      component.isBoostActive = true;

      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      };
      component.setFreebet(bet);

      expect(component.placeStakeErr).toBeNull();
      expect(bet.errorMsg).toBeNull();
      expect(bet.handicapErrorMsg).toBeNull();
      expect(bet.Bet.freeBet).toBe(bet.selectedFreeBet);
      expect(component['clearSingleBetPriceChangeErr']).toHaveBeenCalledWith(bet);
      expect(component['setMultipleSuspendedErrMsg']).toHaveBeenCalledWith(bet);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SET_FREE_BET);
      expect(betslipStorageService.setFreeBet).toHaveBeenCalledWith(bet);
      expect(component['commandService'].execute).toHaveBeenCalledWith(
        'ODDS_BOOST_SHOW_FB_DIALOG', [true, 'betslip']
      );
    });

    it('setFreebet (freebet not selected)', () => {
      component['clearSingleBetPriceChangeErr'] = jasmine.createSpy();
      component['setMultipleSuspendedErrMsg'] = jasmine.createSpy();
      component['priceChangeCount'] = 1;
      component['commandService'].execute = jasmine.createSpy();
      component.isBoostActive = true;

      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: null,
        stake: {}
      };
      component.setFreebet(bet);

      expect(component.placeStakeErr).toBeNull();
      expect(bet.errorMsg).toBeNull();
      expect(bet.handicapErrorMsg).toBeNull();
      expect(bet.Bet.freeBet).toBe(bet.selectedFreeBet);
      expect(component['clearSingleBetPriceChangeErr']).toHaveBeenCalledWith(bet);
      expect(component['setMultipleSuspendedErrMsg']).toHaveBeenCalledWith(bet);
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(betslipStorageService.setFreeBet).toHaveBeenCalledWith(bet);
      expect(component['commandService'].execute).not.toHaveBeenCalledWith(
        'ODDS_BOOST_SHOW_FB_DIALOG', [true, 'betslip']
      );
    });

    it('should set amount on change', () => {
      const bet = {
        stake: {
          perLine: {}
        },
        Bet: {
          stake: {},
          betOffer: {
            offer: {}
          }
        }
      };
      component.placeSuspendedErr = { multipleWithDisableSingle: false } as any;
      component.isBoostActive = true;
      component.setAmount(bet, "10");
      expect(betslipService.setAmount).toHaveBeenCalledWith(bet);
    });

    it('handleDefaultError (error with code)', () => {
      component['outcomesErrorParser'] = jasmine.createSpy();
      component['updatePlaceBetsPending'] = jasmine.createSpy();
      localeService.getString.calls.reset();
      localeService.getString.and.returnValue('Bet not found');

      const result: any = {
        errs: [{
          subCode: 'BET_NOT_FOUND',
          code: 'BET_ERROR',
          outcomeRef: { id: '1' }
        }]
      };

      component['handleDefaultError'](result);

      expect(component.placeStakeErr).toBe('Bet not found');
      expect(component['outcomesErrorParser']).toHaveBeenCalledTimes(1);
      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(component['updatePlaceBetsPending']).toHaveBeenCalledWith(false);
    });

    it('handleDefaultError (error without code)', () => {
      component['outcomesErrorParser'] = jasmine.createSpy();
      component['updatePlaceBetsPending'] = jasmine.createSpy();
      localeService.getString.calls.reset();
      localeService.getString.and.returnValue('Betting limit exceeded!');

      const result: any = {
        errs: [{
          outcomeRef: { id: '1' }
        }]
      };

      component['handleDefaultError'](result);

      expect(component.placeStakeErr).toBe('Betting limit exceeded!');
      expect(component['outcomesErrorParser']).toHaveBeenCalledTimes(1);
      expect(localeService.getString).toHaveBeenCalledTimes(1);
      expect(component['updatePlaceBetsPending']).toHaveBeenCalledWith(false);
    });

    it('handleDefaultError (unknown code)', () => {
      component['outcomesErrorParser'] = jasmine.createSpy();
      component['updatePlaceBetsPending'] = jasmine.createSpy();
      localeService.getString.calls.reset();
      localeService.getString.and.returnValue('KEY_NOT_FOUND');

      const result: any = {
        errs: [{
          outcomeRef: { id: '1' },
          code: 'DONT_BET_YOU_WILL_LOSE'
        }]
      };

      component['handleDefaultError'](result);

      expect(component['outcomesErrorParser']).toHaveBeenCalledTimes(1);
      expect(localeService.getString).toHaveBeenCalledTimes(3);
      expect(awsService.addAction).toHaveBeenCalledWith(
        'betSlipComponent=>placeBetResponse=>undefined_errors', jasmine.any(Object)
      );
      expect(component['updatePlaceBetsPending']).toHaveBeenCalledWith(false);
    });

    it('handleDefaultError (boost active)', () => {
      component['outcomesErrorParser'] = jasmine.createSpy();
      component['updatePlaceBetsPending'] = jasmine.createSpy();
      component.isBoostActive = true;
      localeService.getString.calls.reset();

      const result: any = {
        errs: [{
          outcomeRef: { id: '1' },
          subCode: 'BAD_FREEBET_TOKEN'
        }]
      };

      component['handleDefaultError'](result);

      expect(localeService.getString).toHaveBeenCalledWith('bs.oddsBoostExpiredOrRedeemed');
    });

    it('handleDefaultError (price changed)', () => {
      component.betSlipSingles = component.betSlipMultiples = [];
      const result: any = {
        errs: [{ subCode: 'PRICE_CHANGED' }]
      };
      expect(component['handleDefaultError'](result)).toBeFalsy();
    });

    it('handleDefaultError (bet not permitted)', () => {
      betslipService.isBetNotPermittedError.and.returnValue(true);
      component['handleDefaultError']({ errs: [{}] } as any);
      expect(betslipService.getBetNotPermittedError).toHaveBeenCalled();
    });

    it('get totalStakeIsPresent', () => {
      component.toteFreeBetSelected = true;
      component.areToteBetsInBetslip = () => true;
      toteBetslipService.getTotalStake.and.returnValue('1.00');
      expect(component.totalStakeIsPresent).toBeTruthy();

      component.areToteBetsInBetslip = () => false;
      betslipStakeService.getTotalStake.and.returnValue('2.00');
      expect(component.totalStakeIsPresent).toBeTruthy();

      // component.toteFreeBetSelected = true;
      // expect(component.toteFreeBetSelected).toBeTrue();

      betslipStakeService.getTotalStake.and.returnValue('0.00');
      expect(component.totalStakeIsPresent).toBeFalsy();

      betslipStakeService.getTotalStake.and.returnValue('');
      expect(component.totalStakeIsPresent).toBeFalsy();
    });

    it('should expect isLiveEvent to be true or false', () => {
      component['betData'] = [{
        'Bet': {
          'legs': [
            {
              'selection': { 'docId': '1' }
            }]
        },
        'stake': {
          'stakePerLine': ''
        }
      }] as any;
      const c1 = component['totalStakeIsPresent'];
      component.areToteBetsInBetslip = () => true;
      toteBetslipService.getTotalStake.and.returnValue('1.00');
      expect(component.isLiveEvent).toBeFalsy();
      expect(component.totalStakeIsPresent).toBeTruthy();
      expect(c1).toBeUndefined();

      component['betData'] = [{
        'Bet': {
          'legs': [
            {
              'selection': { 'docId': '1', 'eventIsLive': true }
            }]
        },
        'stake': {
          'stakePerLine': '0.01'
        }
      }] as any;
      const c2 = component['totalStakeIsPresent'];
      component.areToteBetsInBetslip = () => false;
      betslipStakeService.getTotalStake.and.returnValue('2.00');
      expect(component.totalStakeIsPresent).toBeTruthy();
      expect(component.isLiveEvent).toBeTruthy();
      expect(c2).toBeTruthy();

      component['betData'] = [{
        'Bet': {
          'legs': [
            {
              'selection': { 'docId': '1', 'eventIsLive': true }
            }]
        },
        'stake': {
          'stakePerLine': ''
        },
        'selectedFreeBet' : {
          'value': 10
        }
      }] as any;
      const c3 = component['totalStakeIsPresent'];
      component.areToteBetsInBetslip = () => false;
      betslipStakeService.getTotalStake.and.returnValue('2.00');
      expect(component.totalStakeIsPresent).toBeTruthy();
      expect(component.isLiveEvent).toBeTruthy();
      expect(c3).toBeTruthy();
    });

    it('totalStake (regular bets)', fakeAsync(() => {
      betslipStakeService.getFreeBetStake.calls.reset();
      betslipStakeService.getFreeBetStake.and.returnValue(1);
      betslipStakeService.getStake.and.returnValue(0);
      quickDepositService.checkQuickDeposit.calls.reset();
      component.isSelectionSuspended = true;

      Object.defineProperty(component['userService'], 'sportBalance', { value: 10 });
      component.quickDeposit = component.defaultQuickDepositData;
      component['areRegularBetsInBetslip'] = () => true;
      component['handleQuickDepositState'] = jasmine.createSpy('handleQuickDepositState');
      component.betSlipSingles = [{}] as any[];

      component.totalStake();
      tick();

      expect(component['isToteBets']).toBeFalsy();
      expect(component['currentStake']).toEqual(0);
      expect(component['currentStakeWithoutDisabledBets']).toEqual(0);
      expect(betslipStakeService.getStake).toHaveBeenCalledTimes(2);
      expect(betslipStakeService.getFreeBetStake).toHaveBeenCalledWith(component['betData'], true);
      expect(betslipStakeService.getFreeBetStake).toHaveBeenCalledTimes(1);
      expect(quickDepositService.checkQuickDeposit).toHaveBeenCalledTimes(1);
      expect(quickDepositService.checkQuickDeposit).toHaveBeenCalledWith(0, 1, 10, 1, false, true, false);
      expect(betslipStakeService.getTotalStake).toHaveBeenCalledWith(component['betData']);
      expect(component['handleQuickDepositState']).toHaveBeenCalled();
    }));

    it('totalStake (regular bets): when quick deposit should not be shown', fakeAsync(() => {
      betslipStakeService.getFreeBetStake.calls.reset();
      betslipStakeService.getFreeBetStake.and.returnValue(1);
      betslipStakeService.getStake.and.returnValue(2);
      quickDepositService.checkQuickDeposit.calls.reset();

      Object.defineProperty(component['userService'], 'sportBalance', { value: 5 });
      component.quickDeposit = component.defaultQuickDepositData;
      component['areRegularBetsInBetslip'] = () => true;
      component.betSlipSingles = [{}] as any[];

      component.totalStake();
      tick();

      expect(quickDepositService.checkQuickDeposit).toHaveBeenCalledTimes(1);
      expect(quickDepositService.checkQuickDeposit).toHaveBeenCalledWith(2, 1, 5, 1, false, false, false);
    }));

    it('totalStake (tote bets)', () => {
      component['areRegularBetsInBetslip'] = () => false;
      component['areToteBetsInBetslip'] = () => true;
      component.totalStake();
      expect(toteBetslipService.getTotalStake).toHaveBeenCalled();
      expect(component['isToteBets']).toBeTruthy();
    });

    it('totalStake: quick deposit should be shown', fakeAsync(() => {
      betslipStakeService.getStake.and.returnValue(15);
      quickDepositService.checkQuickDeposit.calls.reset();

      Object.defineProperty(component['userService'], 'sportBalance', { value: 10 });
      component.quickDeposit = component.defaultQuickDepositData;
      component['areRegularBetsInBetslip'] = () => true;
      component.quickDeposit.showQuickDepositForm = true;
      component.betSlipSingles = [{}] as any[];
      component.totalStake();
      tick();

      expect(component['currentStake']).toEqual(15);
      expect(component.quickDeposit.showQuickDepositForm).toBeTruthy();
    }));

    it('templatePlaceBet', () => {
      component.debouncePlaceBets = jasmine.createSpy('debouncePlaceBets');
      component.templatePlaceBet();
      expect(component.placeStakeErr).toBeFalsy();
      expect(component.debouncePlaceBets).toHaveBeenCalledTimes(1);
    });

    it('should clear place stake error when betslip hidden', () => {
      component['pubSubService'].subscribe = (n, m, cb) => {
        m === 'show-slide-out-betslip-false' && cb();
      };
      component.placeStakeErr = 'The error';
      component.ngOnInit();
      expect(component.placeStakeErr).toBeFalsy();
    });

    it('overask getter', () => {
      expect(component.overask).toEqual(overAskService);
    });

    describe('ngOnInit: callbacks', () => {
      it('BESTLIP_ERROR_TRACKING', () => {
        commandService.execute = jasmine.createSpy().and.callFake((p1, p2, callback: Function) => {
          callback();
        });

        component.ngOnInit();
        expect(commandService.execute).toHaveBeenCalled();
      });

      it('bsButtonTitle when not logged in, and dsBetsCounter setting', () => {
        userService.status = false;
        component.ngOnInit();
        expect(component.bsButtonTitle).toEqual('bs.betNowLogIn');
        expect(component['dsBetsCounter']).toEqual(1);
      });

      it('Apply calculations for events which is from cache each/way.', () => {
        component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
        component.betSlipSingles = [{
          isEachWayAvailable: true,
          selectedFreeBet: {
            value: 10
          },
          stakeMultiplier: 2,
          Bet: {
            isEachWay: true
          },
          stake: {}
        }];

        component.ngOnInit();
        expect(betslipService.winOrEachWay).toHaveBeenCalled();
      });

      it('placeBets: error flow', () => {
        component.placeBets = jasmine.createSpy().and.returnValue(throwError('err'));

        component.ngOnInit();
        component.templatePlaceBet();
        expect(awsService.addAction).toHaveBeenCalledWith('betSlipComponent=>placeBetRequest=>COMMON');
      });

      describe('USER_BALANCE_UPD', () => {

        beforeEach(() => {
          quickDepositService.getAccounts = jasmine.createSpy('getAccounts').and.returnValue(of([]));
          pubSubService.subscribe = jasmine.createSpy().and.callFake((p1, p2, callback) => {
            if (p2 === 'USER_BALANCE_UPD') {
              component.loadComplete = true;
              component['firstRunOfBetSlip'] = false;
              component['previousBalance'] = {};
              callback();
            }
          });
          spyOn(component as any, 'handleInsufficientFunds').and.returnValue(of(null));
        });
        it('component should be truthy', () => {
          expect(component).toBeTruthy();
        });
      });

      it('BETSLIP_UPDATED', () => {
        component['init'] = jasmine.createSpy();
        pubSubService.subscribe = jasmine.createSpy('sync');
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'BS_SELECTION_LIVE_UPDATE') {
            callback(liveUpdateData);
          } else {
            callback();
          }
        });
        pubSubService.subscribe = jasmine.createSpy('sync');
        component.ngOnInit();
        expect(component['init']).toHaveBeenCalled();
      });

      it('BETSLIP_UPDATED with data', () => {
        component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
        component['init'] = jasmine.createSpy();
        component.betSlipSingles = [{
          outcomeId: '1234',
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey'
        }];
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'BS_SELECTION_LIVE_UPDATE') {
            callback(liveUpdateData);
          } else {
            callback({
              selectionId: '1234'
            });
          }
        });
        component.ngOnInit();

        expect(component['init']).toHaveBeenCalled();
      });

      it('BETSLIP_BET_DATA with data', () => {
        const outcomeDetail = {
          outcomeDetails: [{
            categoryId : '21',
            marketId: 12345,
            name : 'ieuehokeo',
            eventDesc : 'wertyuio',
            accMax : 1,
            accMin: 1
          }],
          bets: [{
            leg: [{'part':[{eventId: "11"}]}],
            betTypeRef: {id: 'L15'},
            availableBonuses :{
              availableBonus:{
                multiplier:'2'
              }
            }
          }]
        }
        storageService.get = jasmine.createSpy('storageService.get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
        component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
        component['init'] = jasmine.createSpy();
        component.betSlipSingles = [{
          outcomeId: '1234',
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey',
         
        }];
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'BS_SELECTION_LIVE_UPDATE') {
            callback(liveUpdateData);
          } else {
            callback(outcomeDetail);
          }
        });
        component.ngOnInit();
       expect(component.betResponseData).toEqual(outcomeDetail);
      });

      it('checkHRRestrictionsIfAny method call for odds selection', () => {
        spyOn(component as any, 'checkHRRestrictionsIfAny').and.callThrough();
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'SET_RESTRICTED_RACECARD') {
            callback(ssMarkets);
          }
        });
        component.ngOnInit();
        expect(component['checkHRRestrictionsIfAny']).toHaveBeenCalledWith(ssMarkets);
      });

      it('checkHRRestrictionsIfAny method  call for tricast forecast add to betslip selection', () => {
        spyOn(component as any, 'checkHRRestrictionsIfAny').and.callThrough();
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'SET_RESTRICTED_RACECARD') {
            callback(null);
          }
        });
        component.ngOnInit();
        expect(component['checkHRRestrictionsIfAny']).toHaveBeenCalledWith(null);
      });

      it('checkHRRestrictionsIfAny method  call for tricast forecast add to betslip selection for false case', () => {
        spyOn(component as any, 'checkHRRestrictionsIfAny').and.callThrough();
        getSelectionDataService['restrictedRacecardAndSelections'] = jasmine.createSpy('restrictedRacecardAndSelections').and.returnValue({horseNames : [], restrictedRaces: [],eventIdDetails : []});
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'SET_RESTRICTED_RACECARD') {
            callback(null);
          }
        });
        component.ngOnInit();
        expect(component['checkHRRestrictionsIfAny']).toHaveBeenCalledWith(null);
      });

      it('checkHRRestrictionsIfAny method  call with undefined betresponse data', () => {
        spyOn(component as any, 'checkHRRestrictionsIfAny').and.callThrough();
        pubSubService.subscribe.and.callFake((tag, channel, callback) => {
          if (channel === 'SET_RESTRICTED_RACECARD') {
            component.betResponseData = {
              outcomeDetails:{
                id: '6543234567',
                name: 'outcome',
                marketId: '222618797',
                accMin: '1',
                accMax: '1'
              }};
            callback(null);
          }
        });
        component.ngOnInit();
        expect(component['checkHRRestrictionsIfAny']).toHaveBeenCalledWith(null);
      });
    });

    it('stake', () => {
      component.stake();
      expect(betslipStakeService.getStake).toHaveBeenCalled();
    });

    it('freeBetStake', () => {
      component.freeBetStake();
      expect(betslipStakeService.getFreeBetStake).toHaveBeenCalled();
    });

    it('getFreeBetLabelText with availableToteBetPacks undefined', () => {
      component.availableToteBetPacks = [];
      component.availableToteFreeBets = [{
        freebetTokenId: 1
      }] as any;
      component.areToteBetsInBetslip = () => {
        return true;
      };
      storageService.get.and.returnValue({
        poolBet: {
          betType: 'BET TOKEN'
        }
      });
      expect(component.getFreeBetLabelText()).toEqual('');
    });

    it('getFreeBetLabelText with availableToteFreeBets undefined', () => {
      component.availableToteBetPacks = [{
        freebetTokenId: 1
      }] as any;
      component.availableToteFreeBets = [];
      component.areToteBetsInBetslip = () => {
        return true;
      };
      storageService.get.and.returnValue({
        poolBet: {
          betType: 'BET TOKEN'
        }
      });
      expect(component.getFreeBetLabelText()).toEqual('');
    });

    it('getFreeBetLabelText', () => {
      component.availableToteBetPacks = [{
        freebetTokenId: 1
      }] as any;
      component.availableToteFreeBets = [{
        freebetTokenId: 1
      }] as any;
      component.areToteBetsInBetslip = () => {
        return true;
      };
      storageService.get.and.returnValue({
        poolBet: {
          betType: 'BET TOKEN'
        }
      });
      expect(component.getFreeBetLabelText()).toEqual('');
    });

    it('getFreeBetLabelText', () => {
      component.availableToteBetPacks = [{
        freebetTokenId: 1
      }] as any;
      component.availableToteFreeBets = [{
        freebetTokenId: 1
      }] as any;
      component.areToteBetsInBetslip = () => {
        return true;
      };
      storageService.get.and.returnValue({
        poolBet: {
        }
      });
      expect(component.getFreeBetLabelText()).toEqual('');
    });

    it('getFreeBetLabelText', () => {
      component.areToteBetsInBetslip = () => {
        return false;
      };
      component.availableToteBetPacks = [{}] as any;
      component.availableToteFreeBets = [{}] as any;
      component.getFreeBetLabelText();
      expect(betslipStakeService.getFreeBetLabelText).toHaveBeenCalled();
    });

    it('getFreeBetLabelText', () => {
      component.getFreeBetLabelText(true);
      expect(betslipStakeService.getFreeBetLabelText).toHaveBeenCalled();
    });

    describe('#totalStakeWithOutFreeBets', () => {
      it('should return totalStake related to Totes', () => {
        toteBetslipService.isToteBetPresent.and.returnValue(true);
        toteBetslipService.getTotalStake.and.returnValue('0.01');

        const result = component.totalStakeWithOutFreeBets();

        expect(component['isToteBets']).toBeTruthy();
        expect(result).toEqual('0.01');
      });

      it('should return regular stake if no Tote Bets', () => {
        betslipStakeService.getStake.and.returnValue(1.56);
        toteBetslipService.isToteBetPresent.and.returnValue(false);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toEqual('1.56');
        expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return regular stake if there are regular bets', () => {
        betslipStakeService.getStake.and.returnValue(1.53);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toEqual('1.53');
        expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return regular stake if there are regular bets and there are freebets and there is total stake', () => {
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue('1.00');
        betslipStakeService.getStake.and.returnValue(1.53);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toEqual('1.53');
        expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return NULL if there are regular bets and there are freebets and there is NO total stake', () => {
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue('1.00');
        betslipStakeService.getStake.and.returnValue(0);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toBeNull();
        expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return regular stake if there are regular bets and there ara NO freebets and there is total stake', () => {
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue(null);
        betslipStakeService.getStake.and.returnValue(1.53);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toEqual('1.53');
        expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return totalStake related to Totes1', () => {
        component.areToteBetsInBetslip = () => {
          return true;
        };
        component.toteBetSlip.toteBet = {
          poolBet: {
            stakePerLine: ''
          }
      } as any;
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue('1.00');
        betslipStakeService.getStake.and.returnValue(0);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toBeUndefined();
        //expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return totalStake related to Totes2', () => {
        component.areToteBetsInBetslip = () => {
          return true;
        };
        component.toteBetSlip.toteBet = {
          poolBet: {
            stakePerLine: '1'
          }
      } as any;
        component['selectedToteFreeBetValue'] = 10;
        component['updatedToteFreeBetValue'] = 5;
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue('1.00');
        betslipStakeService.getStake.and.returnValue(0);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toBeUndefined();
        //expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });

      it('should return totalStake related to Totes3', () => {
        component.areToteBetsInBetslip = () => {
          return true;
        };
        component.toteBetSlip.toteBet = {
          poolBet: {
            stakePerLine: '1'
          }
      } as any;
        component.totalFreeBetsStake = jasmine.createSpy().and.returnValue('1.00');
        betslipStakeService.getStake.and.returnValue(0);
        betslipDataService.containsRegularBets.and.returnValue(true);

        const result = component.totalStakeWithOutFreeBets();

        expect(result).toBeUndefined();
        //expect(betslipStakeService.getStake).toHaveBeenCalledTimes(1);
      });
    });

    describe('#totalFreeBetsStake', () => {
      it('should return FreeBetStake null if FreeBetStake equals to 0.00', () => {
        component.areToteBetsInBetslip = () => {
          return false;
        };
        betslipStakeService.getFreeBetStake.and.returnValue('0.00');
        expect(component.totalFreeBetsStake()).toEqual(null);
      });

      it('should return FreeBetStake if FreeBetStake is greater then 0.00', () => {
        component.areToteBetsInBetslip = () => {
          return false;
        };
        betslipStakeService.getFreeBetStake.and.returnValue('1.00');
        expect(component.totalFreeBetsStake()).toEqual('1.00');
      });

      it('should return fetchStakePerLine', () => {
        component.areToteBetsInBetslip = () => {
          return true;
        };
        component.updatedToteFreeBetValue = 1;
        component['selectedToteFreeBetValue'] = 2;
        component['setToteSelectedId'] = 2;
        component.toteBetSlip.toteBet = {
            poolBet: {
              stakePerLine: '1'
            }
        } as any;
        expect(component.totalFreeBetsStake() as any).toEqual(2);
        component.toteBetSlip = {
          toteBet: {
            poolBet: {
              stakePerLine: ''
            }
          }
        } as any;
        expect(component.totalFreeBetsStake() as any).toEqual(1);
        component.toteBetSlip = {
          toteBet: {
            poolBet: {
              stakePerLine: null
            }
          }
        } as any;
        expect(component.totalFreeBetsStake() as any).toEqual(1);
        component.toteBetSlip = {
          toteBet: {
            poolBet: {
              stakePerLine: undefined
            }
          }
        } as any;
        expect(component.totalFreeBetsStake() as any).toEqual(1);
        component.toteBetSlip = {
          toteBet: {
            poolBet: {
              stakePerLine: '1'
            }
          }
        } as any;
        component['selectedToteFreeBetValue'] = undefined;
        component['setToteSelectedId'] = undefined;
        expect(component.totalFreeBetsStake() as any).toBeUndefined();
        component.toteBetSlip = {
          toteBet: {
            poolBet: {
              stakePerLine: '1'
            }
          }
        } as any;
        component['setToteSelectedId'] = 2;
        component['selectedToteFreeBetValue'] = 2;
        expect(component.totalFreeBetsStake() as any).toEqual(2);
      });
    });

    describe('#totalEstReturns', () => {
      it('totalEstReturns', () => {
        component.totalEstReturns();
        expect(betslipStakeService.getTotalEstReturns).toHaveBeenCalled();
      });

      it('should return undefined and in UI it will be N/A', () => {
        betslipStakeService.getTotalEstReturns.and.returnValue('N/A');
        expect(component.totalEstReturns()).toEqual(undefined);
      });
    });

    it('calculateEstReturns', () => {
      component.ngOnInit();
      component.betSlipSingles = [0];
      component.calculateEstReturns(0);
      expect(betslipStakeService.calculateEstReturns).toHaveBeenCalledWith(0,0);
      expect(filterService.setCurrency).toHaveBeenCalledWith(5, '£');

      betslipStakeService.calculateEstReturns = jasmine.createSpy().and.returnValue('5£');
      expect(component.calculateEstReturns(0)).toEqual('5£');
    });

    describe('cleanBetslip', () => {
      it('it should show-slide-out-betslip to be false', () => {
        component['dsBetsCounter'] = 0;
        component.cleanBetslip();
        expect(component['rebuildBetslip']).toBeFalsy();
        expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
      });
    });

    describe('removeFromBetslip', () => {
      it('show-slide-out-betslip to be false', () => {
        component.ngOnInit();
        component.betSlipSingles = [{
          outcomeId: '1234',
          Bet : {
            params : {lottoData :{isLotto : true}}
          },
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey'
        }];
        component['dsBetsCounter'] = 0;
        windowRefService.nativeWindow.view.mobile = true;

        component.removeFromBetslip(0);
        expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
      });
      it('no odds boost', () => {
        component.ngOnInit();
        const bet = {
          outcomeId: '1234',
          Bet : {
            params : {lottoData :{isLotto : false}}
          },
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey'
        };
        component.betSlipSingles = [bet];

        component.removeFromBetslip(0);
        expect(betslipService.removeByOutcomeId).toHaveBeenCalledWith(bet);
        expect(storageService.set).toHaveBeenCalledTimes(1);
        expect(overAskService.clearStateMessage).toHaveBeenCalled();
        expect(pubSubService.publishSync).toHaveBeenCalled();
      });

      it('with odds boost', () => {
        component.ngOnInit();
        component.isBoostEnabled = true;
        component.isBoostActive = true;
        const bet = {
          outcomeId: '1234',
          Bet : {
            params : {lottoData :{}}
          },
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey'
        };
        component.betSlipSingles = [bet];

        component.removeFromBetslip(0);
        expect(betslipService.removeByOutcomeId).toHaveBeenCalledWith(bet);
        expect(storageService.set).toHaveBeenCalledTimes(1);
        expect(overAskService.clearStateMessage).toHaveBeenCalled();
        expect(pubSubService.publishSync).toHaveBeenCalled();
        expect(pubSubService.publish).toHaveBeenCalled();
      });
      it('no odds boost with multi betslips', () => {
        component.ngOnInit();
        const bet = [
        {
          outcomeId: '12345',
          disabled:true,
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [2]
          },
          eventName: 'Liverpool1 vs Chelsey1'
         } 
      ];
        component.betSlipSingles = bet;
        component['dsBetsCounter'] = 0;
        windowRefService.nativeWindow.view.mobile = true;
        betslipService.suspendedIndexFromSelection = jasmine.createSpy().and.returnValue(bet);
        component.removeAllSuspended();
        expect(betslipService.suspendedIndexFromSelection).toHaveBeenCalledWith(bet);
        expect(storageService.set).toHaveBeenCalledTimes(1);
        expect(overAskService.clearStateMessage).toHaveBeenCalled();
        expect(pubSubService.publishSync).toHaveBeenCalled();
      });

      it('show-slide-out-betslip to be false for empty lotto data', () => {
        component.ngOnInit();
        component.betSlipSingles = [{
          outcomeId: '1234',
          Bet : {
            params : {}
          },
          time: {
            getTime: jasmine.createSpy()
          },
          eventIds: {
            eventIds: [1]
          },
          eventName: 'Liverpool vs Chelsey'
        }];
        component['dsBetsCounter'] = 0;
        windowRefService.nativeWindow.view.mobile = true;

        component.removeFromBetslip(0);
        expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
      });
    });

    it('openSelectionMultiplesDialog', () => {
      component.notAccaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.betResponseData = {bets:[{
        betTypeRef:{
          id:'L15'
        },
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]};
      component.openSelectionMultiplesDialog(0, false,false,'lucky15');
      expect(component).toBeTruthy();

      component.betResponseData = {bets:[{
        betTypeRef:{
          id:'L31'
        },
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]};
      component.notAccaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.openSelectionMultiplesDialog(0, true,false,'lucky31');
      expect(component).toBeTruthy();

      component.betResponseData = {bets:[{
        betTypeRef:{
          id:'L63'
        },
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]};
      component.accaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.openSelectionMultiplesDialog(0, true,false,'lucky63');
      expect(component).toBeTruthy();
      component.betResponseData = {bets:[{
        betTypeRef:{
          id:'L63'
        },
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]};
      component.accaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.openSelectionMultiplesDialog(0, true,false);
      expect(component).toBeTruthy();
      component.betResponseData = {bets:[{
        betTypeRef:{
          id:'L63'
        },
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]};
      component.accaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.notAccaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.openSelectionMultiplesDialog(0, true);
      expect(component).toBeTruthy();
      component.accaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.notAccaBets = [{
        stakeMultiplier: 1,
        type: 'type'
      }];
      component.openSelectionMultiplesDialog(0, true, true);
      expect(component).toBeTruthy();
    });

    it('getTime', () => {
      expect(component.getTime({ localTime: '18:40' })).toEqual('18:40');
      betInfoDialogService.isRacing = jasmine.createSpy().and.returnValue(false);
      component.getTime({ time: '18:40' });
      expect(datePipe.transform).toHaveBeenCalledWith('18:40', 'h:mm a');
    });

    it('isBetCheckboxDisabled', () => {
      overAskService.hasTraderMadeDecision = true;
      overAskService.isNoBetsOffered = true;
      expect(component.isBetCheckboxDisabled()).toBeTruthy();

      overAskService.hasTraderMadeDecision = false;
      overAskService.isNoBetsOffered = true;
      expect(component.isBetCheckboxDisabled()).toBeFalsy();

      overAskService.hasTraderMadeDecision = true;
      overAskService.isNoBetsOffered = false;
      expect(component.isBetCheckboxDisabled()).toBeFalsy();
    });

    it('getRemovedLineSymbol', () => {
      component.getRemovedLineSymbol('test');
      expect(filterService.removeLineSymbol).toHaveBeenCalledWith('test');
    });

    it('getErrorMsgLocale', () => {
      component.getErrorMsgLocale(null);
      expect(localeService.getString).not.toHaveBeenCalled();

      component.getErrorMsgLocale({ error: 'error' });
      expect(localeService.getString).toHaveBeenCalledWith('bs.error');
    });

    it('getTypeLocale', () => {
      localeService.getString.and.callFake(a => `${a} message`);

      expect(component.getTypeLocale({ type: 'type' })).toEqual('bs.type message');
      expect(localeService.getString).toHaveBeenCalledWith('bs.type');
    });

    it('getFooterWarningMsg', () => {
      component.placeSuspendedErr = <any>{
        msg: '1'
      };

      expect(component.getFooterWarningMsg()).toBeTruthy();
      component.placeSuspendedErr = null;
      toteBetslipService.toteSuspensionError = true;
      expect(component.getFooterWarningMsg()).toBeTruthy();
    });

    it('showMultipleRemoveLink', () => {
      expect(component.showMultipleRemoveLink({
        isTraderDeclined: true
      })).toBeTruthy();
    });

    describe('checkStake', () => {
      it('should return true, when stake is higher than minimum stake', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(0);
        const checkStake = component.checkStake({
          stake: {
            perLine: '5',
            min: 4,
            params: { min: '4.00' }
          }
        });

        expect(checkStake).toBeTruthy();
      });

      it('should return false, when stake is lower than minimum stake', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(0);
        const checkStake = component.checkStake({
          isLotto: false,
          stake: {
            perLine: '2',
            min: 4,
            params: { min: '4.00' }
          }
        });

        expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', ['4.00', '£']);
        expect(checkStake).toBeFalsy();
      });

      it('should return true, when stake + freebet is bigger than minAllowed', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(6);
        const checkStake = component.checkStake({
          isLotto: false,
          stake: {
            perLine: '5',
            min: 10,
            params: { min: '10.00' }
          }
        });

        expect(checkStake).toBeTruthy();
      });

      it('should return true, when stake + freebet is bigger than minAllowed', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(0);
        const checkStake = component.checkStake({
          isLotto: false,
          stake: {
            perLine: '0',
            min: 10,
            params: { min: '10.00' }
          }
        });

        expect(localeService.getString).not.toHaveBeenCalled();
        expect(checkStake).toBeTruthy();
      });

      it('should return true, when stake is higher than minimum stake', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(0);
        const checkStake = component.checkStake(null);

        expect(checkStake).toBeTruthy();
      });
    });

    it('isMultiplesEachWay', () => {
      component.betSlipSingles = [{
        isEachWayAvailable: true
      }];
      expect(component.isMultiplesEachWay()).toBeTruthy();
      component.betSlipSingles = [{
        isEachWayAvailable: true
      }, {
        isEachWayAvailable: false
      }];
      expect(component.isMultiplesEachWay()).toBeFalsy();
    });

    it('getStakeOptions', () => {
      expect(component.getStakeOptions({
        priceDec: 10
      })).toEqual([{ name: 'SP', value: 'SP' }, { name: 'LP', value: '10.00' }]);
    });

    it('isACCABetslip', () => {
     const response = component.isACCABetslip({
      'Bet': {
        'lines' : 1,
        'legs': ['abc','ab'],
      },
      outcomes: [{
        isEachWayAvailable: false
      }]
     })
     expect(response).toBeTrue();
  });

    it('toggle', () => {
      const bet = {
        expanded: true
      };
      component.toggle(bet);
      expect(bet.expanded).toBeFalsy();

      bet.expanded = false;
      component.betSlipSingles = [{
        expanded: true
      }];
      component.toggle(bet);
      expect(bet.expanded).toBeTruthy();
    });

    it('trackByIndex', () => {
      expect(component.trackByIndex(0)).toEqual(0);
    });

    it('autoScrollOff', () => {
      component.ngOnInit();
      expect(component.autoScrollOff('')).toBeFalsy();
      expect(component.autoScrollOff('PRICE_CHANGED')).toBeTruthy();
    });

    it('getStakeId', () => {
      const prefix = 'a';
      const id = '1';
      expect(component.getStakeId(prefix, id)).toEqual(`${prefix}-${id}`);
    });

    it('acceptOffer', () => {
      component.acceptOffer();
      expect(overAskService.acceptOffer).toHaveBeenCalled();
    });

    it('setPriceType', () => {
      const i = 0;
      component.betSlipSingles = [{
        isEachWayAvailable: true,
        selectedFreeBet: {
          value: 10
        },
        stakeMultiplier: 2,
        Bet: {
          isEachWay: true
        },
        stake: {},
        price: {
          priceType: 'LP'
        }
      }];

      component.setPriceType({ output: 'test', value: 'SP' }, i);
      expect(betslipService.setPriceType).toHaveBeenCalledWith({
        isEachWayAvailable: true,
        selectedFreeBet: {
          value: 10
        },
        stakeMultiplier: 2,
        Bet: {
          isEachWay: true
        },
        stake: {},
        price: {
          priceType: 'SP'
        }
      });
    });

    it('clearUserValueForDisabledBets', () => {
      component.betSlipSingles = [{
        disabled: true,
        stake: {},
        selectedFreeBet: {},
        Bet: { freeBet: {} },
        type: 'SGL'
      }];

      component.clearUserValueForDisabledBets();
      expect(betslipStorageService.setFreeBet).toHaveBeenCalled();
      expect(component.betSlipSingles[0]).toEqual({
        disabled: true,
        stake: {
          perLine: '',
          freeBetAmount: undefined
        },
        selectedFreeBet: null,
        type: 'SGL',
        Bet: { freeBet: null },
        errorMsg: null,
        handicapErrorMsg: null
      });
    });

    describe('odds', () => {
      it('priceDec', () => {
        expect(component.odds({
          priceDec: 10.2
        })).toEqual('10.20');
      });
      it('price', () => {
        expect(component.odds({
          isStarted: true,
          price: {
            oldPrice: {
              priceNum: 1,
              priceDen: 4,
              priceDec: 1.25
            }
          }
        })).toEqual('1/4');
        userService.status = false;
        expect(component.odds({
          isStarted: true,
          price: {
            priceNum: 1,
            priceDen: 5,
            priceDec: 1.25,
            oldPrice: {
              priceNum: 1,
              priceDen: 4,
              priceDec: 1.25
            }
          }
        })).toEqual('1/5');
        userService.status = true;
        userService.oddsFormat = 'dec';
        expect(component.odds({
          isStarted: true,
          price: {
            oldPrice: {
              priceNum: 1,
              priceDen: 4,
              priceDec: 1.25
            }
          }
        })).toEqual('1.25');
      });
    });

    describe('showPriceChangeNotification', () => {
      it('should show notification', () => {
        component['priceChangeBets'].add('1');
        component.placeBetsPending = false;
        component.placeSuspendedErr = { msg: '' } as any;
        component.countDownClock = '';
        expect(component.showPriceChangeNotification()).toBeTruthy();
      });

      it('should not show notification (count down)', () => {
        component['priceChangeBets'].add('1');
        component.placeBetsPending = false;
        component.placeSuspendedErr = { msg: '' } as any;
        component.countDownClock = '00:05';
        expect(component.showPriceChangeNotification()).toBeFalsy();
      });

      it('should not show notification (suspended error)', () => {
        component['priceChangeBets'].add('1');
        component.placeBetsPending = false;
        component.placeSuspendedErr = { msg: 'Error' } as any;
        component.countDownClock = '';
        expect(component.showPriceChangeNotification()).toBeFalsy();
      });

      it('should not show notification (place bet pending)', () => {
        component['priceChangeBets'].add('1');
        component.placeBetsPending = true;
        component.placeSuspendedErr = { msg: '' } as any;
        component.countDownClock = '';
        expect(component.showPriceChangeNotification()).toBeFalsy();
      });

      it('should not show notification (no proce change bets)', () => {
        component['priceChangeBets'].clear();
        component.placeBetsPending = false;
        component.placeSuspendedErr = { msg: '' } as any;
        component.countDownClock = '';
        expect(component.showPriceChangeNotification()).toBeFalsy();
      });
    });

    it('isNoSelections', () => {
      component.ngOnInit();

      component['isBetSlipEmpty'] = true;
      component.loadComplete = true;
      expect(component.isNoSelections).toBeTruthy();

      component.betSlipSingles = [1, 2, 3];
      component['isBetSlipEmpty'] = true;
      component.loadComplete = true;
      expect(component.isNoSelections).toBeFalsy();

      component.betSlipSingles = [];
      component['isBetSlipEmpty'] = false;
      component.loadComplete = true;
      expect(component.isNoSelections).toBeFalsy();

      component.betSlipSingles = [];
      component['isBetSlipEmpty'] = true;
      component.loadComplete = false;
      expect(component.isNoSelections).toBeFalsy();
    });

    describe('#oddsACCA', () => {
      it('oddsACCA NAN case', () => {
        const result = component.oddsACCA({});

        expect(betslipService.getMultiplePotentialPayout).toHaveBeenCalled();
        expect(betslipService.isSinglesHasOldPrice).toHaveBeenCalled();
        expect(betslipService.buildPotentialPayoutObj).toHaveBeenCalled();
        expect(fracToDecService.getAccumulatorPrice).not.toHaveBeenCalled();
        expect(result).toEqual(null);
      });

      it('oddsACCA valid case', () => {
        betslipService.getMultiplePotentialPayout.and.returnValue(1.5);
        const result = component.oddsACCA({});

        expect(result).toEqual('0.5/1');
      });
    });


    it('isBetForACCA', () => {
      expect(component['isBetForACCA']({
        Bet: {
          lines: 1,
          legs: [1, 2]
        },
        outcomes: [{}, {}]
      })).toBeTruthy();

      expect(component['isBetForACCA']({
        Bet: {
          lines: 1,
          legs: [1]
        },
        outcomes: [{}, {}]
      })).toBeFalsy();

      expect(component['isBetForACCA']({
        Bet: {
          lines: 2,
          legs: [1, 2]
        },
        outcomes: [{}, {}]
      })).toBeFalsy();
    });

    it('isAccaBetValid', () => {
      expect(component['isAccaBetValid'](2)).toBeTruthy();
      expect(component['isAccaBetValid'](1)).toBeFalsy();
    });

    it('addStakeError', () => {
      component['addStakeError']({
        subCode: 'DUPLICATEBET'
      }, {});
      expect(localeService.getString).toHaveBeenCalledWith(`bs.DUPLICATEBET`);

      const fakeBet = {
        bet: {
          Bet: {
            update: jasmine.createSpy()
          }
        }
      };
      component['addStakeError']({}, fakeBet);
      expect(fakeBet.bet.Bet.update).toHaveBeenCalledWith(fakeBet, 'stakeError');
    });

    it('calculateEstReturnsMultiples', () => {
      component.ngOnInit();
      component.calculateEstReturnsMultiples(0, [{}]);
      expect(betslipStakeService.calculateEstReturnsMultiples).toHaveBeenCalledWith({},0);
      expect(filterService.setCurrency).toHaveBeenCalledWith(5, '£');

      betslipStakeService.calculateEstReturnsMultiples = jasmine.createSpy().and.returnValue('5£');
      expect(component.calculateEstReturnsMultiples(0, [{}])).toEqual('5£');
    });

    describe('checkAmount', () => {
      beforeEach(() => {
        quickDepositService.getAccounts.and.returnValue(of([]));
      });

      it('same freebet selected', () => {
        component['betData'] = [{
          selectedFreeBet: { id: 1 }, stake: {}
        }, {
          selectedFreeBet: { id: 1 }, stake: {}
        }] as any;
        component.checkAmount();
        expect(betslipService.areBetsWithStakes).toHaveBeenCalledTimes(1);
      });
      
      it('checkAmount() if lotto bets avaliable', () => {
        component['betData'] = [
          {
            isLotto: true,
            details: {
              draws: ['test'],
              stake: {perLine : 1}
            },
            stake: {},
            accaBets: [{
              stake: 1,
            }],
          },        
      ] as any;
        component.checkAmount();
        expect(component['betData'][0].isLotto).toEqual(true);
      });

      it('empty stake', () => {
        component['betData'] = [{
          stake: {}
        }] as any;
        component.checkAmount();
        expect(localeService.getString).toHaveBeenCalledWith('bs.placeBetAlertMessage');
      });

      it('invalid stake', () => {
        component['freeBetStake'] = jasmine.createSpy().and.returnValue(0);
        component['betData'] = [{
          stake: { perLine: 1, min: 2, params: { min: '2.00' } }
        }] as any;
        component.checkAmount();
        expect(localeService.getString).toHaveBeenCalledWith('bs.minStake', jasmine.any(Array));
      });

      it('publishes message to BS_SHOW_OVERLAY channel', () => {
        component['betData'] = [{
          stake: { perLine: 0, min: 2, params: { min: '2.00' }, selectedFreeBet: null }
        }] as any;

        component.checkAmount();

        expect(pubSubService.publish).toHaveBeenCalledWith(
          pubSubService.API.BS_SHOW_OVERLAY,
          localeService.getString('bs.placeBetAlertMessage')
        );
      });
    });

    it('scrollToActionButtons (scrollObj found)', () => {
      const scrollObj = {
        scrollHeight: '10',
        scrollTop: null
      };

      windowRefService.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(scrollObj);

      createComponent();
      component['scrollToActionButtons']();

      expect(scrollObj.scrollTop).toEqual('10');
    });

    it('scrollToActionButtons (scrollObj null)', () => {
      const scrollObj = {
        scrollTop: null
      };

      windowRefService.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(scrollObj);

      createComponent();
      component['scrollToActionButtons']();

      expect(scrollObj.scrollTop).toBe(undefined);
    });

    it('updateBetSingles (betSlipSingles: null)', () => {
      component.betSlipSingles = null;
      expect(component['updateBetSingles']()).toBeFalsy();
    });

    it('updateBetSingles (betSlipSingles exist)', () => {
      component['findCompetition'] = jasmine.createSpy().and.returnValue(true);
      component.betSlipSingles = [{ outcomeId: '123' }];

      expect(component['updateBetSingles']()[0].competition).toBeTruthy();
      expect(component['findCompetition']).toHaveBeenCalled();
    });

    it('findCompetition', () => {
      expect(component['findCompetition'](222)).toBe(undefined);

      betslipStorageService.restore = () => [{}, { id: 'SGL|111' }, { id: 'SGL|222', typeName: 'SGL' }];
      createComponent();
      expect(component['findCompetition'](222)).toBe('SGL');
    });

    describe('birCountDownTimer', () => {
      it('(time: null, countDownValue === undefined)', () => {
        component['countDownValue'] = undefined;
        component['birCountDownTimer'](null);
        expect(component['countDownValue']).toBe(undefined);
        expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });

      it('(time: 2, countDownValue > 0)', () => {
        component['countDownValue'] = 2;
        component['birCountDownTimer'](2);
        expect(component['countDownValue']).toBe(0);
        expect(component.countDownClock).toBe(null);
        expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      });

      it('(time: null, countDownValue === 0)', () => {
        component['countDownValue'] = 0;
        component['birCountDownTimer'](0);
        expect(component.countDownClock).toBe(null);
      });
    });

    describe('clearSingleBetPriceChangeErr', () => {
      let bet;
      beforeEach(() => {
        bet = {
          Bet: {
            clearErr: jasmine.createSpy('clearErr')
          },
          disabled: false,
          errorMsg: null,
          handicapErrorMsg: null,
          error: null
        };
      });

      it('(errorMsg case)', () => {
        bet.errorMsg = 'error_text';
        component['clearSingleBetPriceChangeErr'](bet);

        expect(bet.error).toEqual(null);
        expect(bet.errorMsg).toEqual('');
        expect(bet.handicapErrorMsg).toEqual('');
        expect(bet.Bet.clearErr).toHaveBeenCalled();
      });

      it('(handicapErrorMsg case)', () => {
        bet.handicapErrorMsg = 'error_text';
        component['clearSingleBetPriceChangeErr'](bet);

        expect(bet.Bet.clearErr).toHaveBeenCalled();
      });

      it('(error case)', () => {
        bet.error = 'error_text';
        component['clearSingleBetPriceChangeErr'](bet);

        expect(bet.Bet.clearErr).toHaveBeenCalled();
      });

      it('(false case)', () => {
        component['clearSingleBetPriceChangeErr'](bet);
        expect(bet.Bet.clearErr).not.toHaveBeenCalled();

        bet.disabled = true;
        bet.errorMsg = 'error_text';
        component['clearSingleBetPriceChangeErr'](bet);
        expect(bet.Bet.clearErr).not.toHaveBeenCalled();
      });

      afterEach(() => {
        bet.errorMsg = bet.error = bet.handicapErrorMsg = null;
      });
    });

    it('noActiveSelectionsAction', () => {
      component['betData'] = [{ disabled: true }, { disabled: false }];
      expect(component['noActiveSelectionsAction']()).toBeFalsy();
    });

    it('getDefaultStakeOptions', () => {
      expect(component['getDefaultStakeOptions']()).toEqual([
        { name: 'SP', value: 'SP' },
        { name: 'LP', value: 'LP' }
      ]);
    });

    it('checkMultipleStakeBox', () => {
      component.betSlipMultiples = [{ stake: null }];
      expect(component['checkMultipleStakeBox']()).toBeFalsy();
      component.betSlipMultiples = [{ stake: {} }];
      expect(component['checkMultipleStakeBox']()).toBeFalsy();
      component.betSlipMultiples = [{ stake: { amount: 0 } }];
      expect(component['checkMultipleStakeBox']()).toBeFalsy();
      component.betSlipMultiples = [{ stake: { amount: 1 } }];
      expect(component['checkMultipleStakeBox']()).toBeTruthy();
    });

    describe('getFirstMultipleInfoForAccaNotification', () => {

      beforeEach(() => {
        spyOn(component, 'oddsACCA');
      });

      it('should call oddsACCA to update price on LS', () => {
        component['getFirstMultipleInfoForAccaNotification']({stakeMultiplier: 1, stake: {}} as any);

        expect(component.oddsACCA).toHaveBeenCalled();
      });

      it('getFirstMultipleInfoForAccaNotification (isValidMultiple: false)', () => {
        expect(component['getFirstMultipleInfoForAccaNotification']({})).toEqual({});
        expect(component['getFirstMultipleInfoForAccaNotification']({ stakeMultiplier: 2 })).toEqual({});
      });

      it('getFirstMultipleInfoForAccaNotification (isValidMultiple: true)', () => {
        const obj = jasmine.objectContaining;
        const multipleBet = {
          stakeMultiplier: 1,
          potentialPayout: 100,
          stake: { perLine: 10},
          type: 'type'
        };

        expect(component['getFirstMultipleInfoForAccaNotification'](multipleBet as any)).toEqual(obj({
          translatedType: 'type',
          potentialPayout: 100,
          stake: 10
        }));
      });

      it('getFirstMultipleInfoForAccaNotification (isValidMultiple: true and offer time expired)', () => {
        const obj = jasmine.objectContaining;
        const multipleBet = {
          stakeMultiplier: 1,
          potentialPayout: 100,
          stake: { perLine: 10},
          type: ''
        };

        component.overask.hasCustomerActionTimeExpired = true;

        expect(component['getFirstMultipleInfoForAccaNotification'](multipleBet as any)).toEqual(obj({
          translatedType: '',
          potentialPayout: 100.00,
          stake: 0
        }));
      });

      it('accaNotificationChanged', () => {
        component['getFirstMultipleInfoForAccaNotification'] = jasmine.createSpy();
        component.betSlipMultiples = [{}];
        component['accaNotificationChanged']();
        expect(component['getFirstMultipleInfoForAccaNotification']).toHaveBeenCalledWith({});
        expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.ACCA_NOTIFICATION_CHANGED, undefined);
      });
    });

    it('accaNotificationChanged(publishSync not called)', () => {
      component.betSlipMultiples = null;
      component['accaNotificationChanged']();
      expect(pubSubService.publishSync).not.toHaveBeenCalled();
    });

    it('getFormattedPrice (frac)', () => {
      userService.oddsFormat = 'frac';
      createComponent();

      component['getFormattedPrice']('100.111');
      expect(fracToDecService.getNumberWith2Decimals).not.toHaveBeenCalled();
      expect(fracToDecService.decToFrac).toHaveBeenCalledWith('100.111', true);
    });

    it('getFormattedPrice (dec)', () => {
      userService.oddsFormat = 'dec';
      createComponent();

      component['getFormattedPrice'](100.111);
      expect(fracToDecService.getNumberWith2Decimals).toHaveBeenCalledWith(100.111);
      expect(fracToDecService.decToFrac).not.toHaveBeenCalled();
    });

    it('handleInsufficientFunds', fakeAsync(() => {
      component['handleInsufficientFunds']();
      expect(component.quickDeposit.quickDepositFormAllowed).toBeTruthy();
      expect(component.quickDeposit.showQuickDepositForm).toBeTruthy();
    }));

    it('returns true (isZeroBalanceWithExistingBets is true)', () => {
      component.isZeroBalanceWithExistingBets = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeTruthy();
    });

    describe('@showBetNowBtn', () => {
      it('should return true', () => {
        component.isIFrameLoadingInProgress = jasmine.createSpy().and.returnValue(false);
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.isZeroBalanceWithExistingBets = false;
        expect(component.showBetNowBtn()).toBeTruthy();
        expect(component.isIFrameLoadingInProgress).toHaveBeenCalled();
      });

      it('should return true when using free bets', () => {
        component.overask.isInProcess = false;
        component.quickDeposit = {
          quickDepositPending: true,
          quickDepositFormExpanded: false,
          showQuickDepositForm: false,
          quickDepositFormAllowed: false
        } as any;
        component.totalStakeAmount = '';
        component.totalFreeBetsStake = () => {return ''};
        betslipStakeService.getFreeBetStake.and.returnValue('1.00');
        component.isIFrameLoadingInProgress = jasmine.createSpy().and.returnValue(false);
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.isZeroBalanceWithExistingBets = false;
        expect(component.showBetNowBtn()).toBeTruthy();
      });

      it('should return false when all method returns true', () => {
        component.isIFrameLoadingInProgress = jasmine.createSpy().and.returnValue(true);
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(true);
        component.isZeroBalanceWithExistingBets = true;
        expect(component.showBetNowBtn()).toBeFalsy();
      });

      it('should return false when iframe loading is in progress', () => {
        component.isIFrameLoadingInProgress = jasmine.createSpy().and.returnValue(true);
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.isZeroBalanceWithExistingBets = false;
        expect(component.showBetNowBtn()).toBeFalsy();
        expect(component.isIFrameLoadingInProgress).toHaveBeenCalled();
      });

      it('should return false when isZeroBalanceWithExistingBets is true', () => {
        component.isIFrameLoadingInProgress = jasmine.createSpy().and.returnValue(false);
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.isZeroBalanceWithExistingBets = true;
        expect(component.showBetNowBtn()).toBeFalsy();
        expect(component.isIFrameLoadingInProgress).toHaveBeenCalled();
      });
    });

    it('#loadQuickDepositIfEnabled should call loadQuickDepositIFrame', () => {
      component.loadQuickDepositIFrame = jasmine.createSpy();
      component['loadQuickDepositIfEnabled']();
      expect(component.loadQuickDepositIFrame).toHaveBeenCalled();
    });

    it('#loadQuickDepositIfEnabled should not call loadQuickDepositIFrame', () => {
      component.loadQuickDepositIFrame = jasmine.createSpy();
      quickDepositIframeService.isEnabled = jasmine.createSpy().and.returnValue(of(false));
      component['loadQuickDepositIfEnabled']();
      expect(component.loadQuickDepositIFrame).not.toHaveBeenCalled();
    });

    describe('outcomesErrorParser', () => {
      it('(truthy case, outcomesErrors.undefined === true, isError === true)', () => {
        component['outcomeErrorParser'] = jasmine.createSpy().and.returnValue(true);
        component['stakeErrorParser'] = (a, b, c) => true;

        expect(component['outcomesErrorParser']({ undefined: [{}, {}], error: 'test' }, [], [])).toBeTruthy();
      });

      it('(truthy case, outcomesErrors.undefined === true, isError === true)', () => {
        component['outcomeErrorParser'] = jasmine.createSpy().and.returnValue(false);

        expect(component['outcomesErrorParser']({}, [], [])).toBeFalsy();
      });
    });

    describe('stakeErrorParser', () => {
      beforeEach(() => {
        component['getAllBets'] = jasmine.createSpy();
        component['addStakeError'] = jasmine.createSpy();
      });

      it('(STAKE_TOO_HIGH, payload.bet === true)', () => {
        betslipService.getBetslipBetByResponseBet = jasmine.createSpy().and.returnValue({
          stake: {
            max: true
          }
        });
        createComponent();
        component['getAllBets'] = jasmine.createSpy();
        component['addStakeError'] = jasmine.createSpy();

        expect(component['stakeErrorParser']({
          subCode: 'STAKE_TOO_HIGH',
          betRef: '1'
        }, [{ documentId: '1', stake: {} }], [])).toBeTruthy();
        expect(betslipService.getBetslipBetByResponseBet)
          .toHaveBeenCalledWith({ documentId: '1', stake: {} }, [], undefined);
      });

      it('(STAKE_TOO_HIGH, payload.bet === false)', () => {
        component['addStakeError'] = jasmine.createSpy();

        expect(component['stakeErrorParser']({
          subCode: 'STAKE_TOO_HIGH'
        }, [{ documentId: '0' }], [])).toBeTruthy();
        expect(component['addStakeError']).toHaveBeenCalledWith({
          subCode: 'STAKE_TOO_HIGH'
        }, {
          type: 'max',
          placeBet: true,
          bet: undefined
        });
      });

      it('(STAKE_TOO_LOW, payload.bet === true)', () => {
        betslipService.getBetslipBetByResponseBet = jasmine.createSpy().and.returnValue({
          stake: {
            minAllowed: '1.00'
          }
        });
        createComponent();
        component['getAllBets'] = jasmine.createSpy();
        component['addStakeError'] = jasmine.createSpy();

        expect(component['stakeErrorParser']({
          subCode: 'STAKE_TOO_LOW',
          betRef: '1'
        }, [{ documentId: '1', stake: {} }], [])).toBeTruthy();
        expect(betslipService.getBetslipBetByResponseBet)
          .toHaveBeenCalledWith({ documentId: '1', stake: {} }, [], undefined);
        expect(component['addStakeError']).toHaveBeenCalledWith({
          subCode: 'STAKE_TOO_LOW',
          betRef: '1'
        }, {
          bet: {
            stake: {
              minAllowed: '1.00',
              min: undefined
            }
          },
          type: 'min', placeBet: true
        });
      });

      it('(STAKE_TOO_LOW, payload.bet === false)', () => {
        component['addStakeError'] = jasmine.createSpy();

        expect(component['stakeErrorParser']({
          subCode: 'STAKE_TOO_LOW'
        }, [{ documentId: '0' }], [])).toBeTruthy();
        expect(component['addStakeError']).toHaveBeenCalledWith({
          subCode: 'STAKE_TOO_LOW'
        }, {
            type: 'min',
            placeBet: true,
            bet: undefined
          });
      });

      it('(stakeHigh === false)', () => {
        expect(component['stakeErrorParser']({}, [], [])).toBeFalsy();
      });
    });

    describe('outcomeErrorParser', () => {
      beforeEach(() => {
        component['updateBetError'] = jasmine.createSpy();
      });

      it('PRICE_CHANGED & Fake error', () => {
        const outcomeId = 1234;
        const outcomeErrors = [{
          subCode: 'SOME_ERROR'
        }, {
          subCode: 'PRICE_CHANGED',
          price: [{
            priceNum: 1,
            priceDen: 2
          }],
          outcomeRef: {
            id: outcomeId
          }
        }];
        const expectedPayload = {
          lp_num: outcomeErrors[1].price[0].priceNum,
          lp_den: outcomeErrors[1].price[0].priceDen,
          status: 'A',
          placeBet: true
        };

        component.betSlipSingles = [{
          outcomeId: 12345,
          Bet: jasmine.createSpyObj('Bet', ['update'])
        }, {
          outcomeId,
          Bet: jasmine.createSpyObj('Bet', ['update'])
        }];

        expect(component['outcomeErrorParser'](outcomeErrors)).toEqual(true);
        expect(betslipService.updateLegsWithPriceChange).toHaveBeenCalledWith(expectedPayload, outcomeId);
        expect(component.betSlipSingles[1].Bet.update).toHaveBeenCalledWith(expectedPayload, 'outcome');
      });

      it('HANDICAP_CHANGED', () => {
        const outcomeErrors = [{
          subCode: 'HANDICAP_CHANGED',
          handicap: 2
        }];

        expect(component['outcomeErrorParser'](outcomeErrors)).toEqual(true);
        expect(component['updateBetError']).toHaveBeenCalledWith({
          subCode: 'HANDICAP_CHANGED',
          handicap: 2
        }, {
            raw_hcap: 2,
            hcap_values: {
              A: '-2.0',
              H: '2.0',
              L: '2.0'
            },
            status: 'A',
            placeBet: true
          }, 'outcome');
      });

      it('EVENT_STARTED', () => {
        component['updateBetError'] = jasmine.createSpy();

        const outcomeErrors = [{
          subCode: 'EVENT_STARTED'
        }];

        expect(component['outcomeErrorParser'](outcomeErrors)).toEqual(true);
        expect(component['updateBetError']).toHaveBeenCalledWith({
          subCode: 'EVENT_STARTED'
        }, {
            started: 'Y'
          }, 'event');
      });

      it('OUTCOME_SUSPENDED', () => {
        component['updateBetError'] = jasmine.createSpy();

        const outcomeErrors = [{
          subCode: 'OUTCOME_SUSPENDED'
        }];

        expect(component['outcomeErrorParser'](outcomeErrors)).toEqual(true);
        expect(component['updateBetError']).toHaveBeenCalledWith({
          subCode: 'OUTCOME_SUSPENDED'
        }, {
            status: 'S'
          }, 'outcome');
      });
    });

    afterEach(() => {
      component = null;
    });
  });

  describe('digitKeyboardShown', () => {
    it('betslip', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) =>
      p2 === 'DIGIT_KEYBOARD_SHOWN' && cb(null, null, [1,2,3,4],'slide-out-betslip'));
      component.ngOnInit();
      expect(component.isDigitKeyboardShown).toBeTruthy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('not betslip', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) =>
      p2 === 'DIGIT_KEYBOARD_SHOWN' && cb(null, null, [1,2,3,4],'quickbet-panel'));
      component.ngOnInit();
      expect(component.isDigitKeyboardShown).toBeFalsy();
    });
  });

  describe('digitKeyboardHidden', () => {
    it('betslip', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) =>
        p2 === 'DIGIT_KEYBOARD_HIDDEN' && cb('slide-out-betslip'));
      component.isDigitKeyboardShown = true;
      component.ngOnInit();
      expect(component.isDigitKeyboardShown).toBeFalsy();
    });

    it('not betslip', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) =>
        p2 === 'DIGIT_KEYBOARD_HIDDEN' && cb('quickbet-panel'));
      component.isDigitKeyboardShown = true;
      component.ngOnInit();
      expect(component.isDigitKeyboardShown).toBeTruthy();
    });
  });

  describe('@betNow btn and @quickDepositBtn states', () => {

    beforeEach(() => {
      component.quickDeposit = component.defaultQuickDepositData;
    });

    describe('@showBetNowBtn', () => {

      it('returns true if quickDepositPending and not overask', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.overask.isInProcess = false;
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.quickDepositPending = true;

        const result = component.showBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('returns false if quickDepositPending but overask active', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.overask.isInProcess = true;
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.quickDepositPending = true;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('returns true ', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.quickDeposit.quickDepositFormExpanded = false;

        const result = component.showBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('returns false when quick deposit is allowed', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(true);
        component.quickDeposit.quickDepositFormExpanded = false;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('returns false (isInProcess is true)', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.overask.isInProcess = true;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('returns false (no stake, showQuickDepositForm and quickDepositFormAllowed are true )', () => {
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;
        component.totalStake = jasmine.createSpy().and.returnValue(null);

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('returns false (totalStake is 0.00, quickDepositFormExpanded is true )', () => {
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.quickDeposit.quickDepositFormExpanded = true;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return true if quick deposit condition is met', () => {
        component.overask.isInProcess = false;
        component.isSelectionSuspended = false;
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('should return true if quick deposit condition is met and stake is not 0.00', () => {
        component.overask.isInProcess = false;
        component.isSelectionSuspended = false;
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = false;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('should return true if quick deposit condition is met and selection is suspended', () => {
        component.overask.isInProcess = false;
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.totalStake = jasmine.createSpy().and.returnValue('');
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('should return false if quick deposit condition is not met and selection is suspended', () => {
        component.overask.isInProcess = false;
        component.quickDeposit.neededAmountForPlaceBet = '0.01';
        component.isSelectionSuspended = false;
        component.totalStake = jasmine.createSpy().and.returnValue('');
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = false;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return false if quick deposit condition is not met and total stake is 0', () => {
        component.overask.isInProcess = false;
        component.quickDeposit.neededAmountForPlaceBet = '0.01';
        component.isSelectionSuspended = false;

        component.totalStake = jasmine.createSpy().and.returnValue('');
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = false;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return true if quick deposit condition is not met and quickDepositFormExpanded is false', () => {
        component.overask.isInProcess = false;
        component.quickDeposit.neededAmountForPlaceBet = '0.01';
        component.isSelectionSuspended = false;

        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;
        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return true if quick deposit condition is not met and showQuickDepositForm is false', () => {
        component.overask.isInProcess = false;
        component.quickDeposit.neededAmountForPlaceBet = '0.01';
        component.isSelectionSuspended = false;

        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        component.quickDeposit.quickDepositFormExpanded = true;
        component.quickDeposit.showQuickDepositForm = false;
        component.quickDeposit.quickDepositFormAllowed = true;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return true if quick deposit condition is not met and quickDepositFormAllowed is false', () => {
        component.overask.isInProcess = false;
        component.quickDeposit.neededAmountForPlaceBet = '0.01';
        component.isSelectionSuspended = false;

        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        component.quickDeposit.quickDepositFormExpanded = true;
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = false;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });

      it('should return false if quick deposit iframe expanded', () => {
        component.overask.isInProcess = false;
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.totalStake = jasmine.createSpy().and.returnValue('');
        component.quickDeposit.quickDepositFormExpanded = false;
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = false;
        component.quickDepositIFrameFormExpanded = true;

        const result = component.showBetNowBtn();
        expect(result).toBeFalsy();
      });
    });

    describe('@disableBetNowBtn', () => {
      it('returns true', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.toteBetSuspendedError = true;
        component.placeBetsPending = true;
        component.quickDeposit.quickDepositPending = true;
        component.loginAndPlaceBets = true;
        component.noActiveSelections = true;
        component['overask'].isOnTradersReview = true;
        component.multiplesShouldBeRebuilded = true;

        const result = component.disableBetNowBtn();
        expect(result).toBeTruthy();
      });

      it('returns false', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        component.areToteBetsInBetslip = () => true;
        toteBetslipService.getTotalStake.and.returnValue('0.01');

        const result = component.disableBetNowBtn();
        expect(result).toBeFalsy();
      });
    });

    describe('@isShowQuickDepositBtnShown', () => {

      it('returns true', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(true);
        component.isZeroBalanceWithExistingBets = true;

        const result = component.isShowQuickDepositBtnShown();
        expect(result).toBeTruthy();
      });

      it('returns false (showQuickDepositForm and quickDepositFormAllowed are falsy)', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.01');
        betslipStakeService.getFreeBetStake.and.returnValue('1.00');
        const result = component.isShowQuickDepositBtnShown();
        expect(result).toBeFalsy();
      });

      it('returns false (total Stake is 0.00)', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('0.00');
        component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;

        const result = component.isShowQuickDepositBtnShown();
        expect(result).toBeFalsy();
      });

      it('returns false (overask in progress)', () => {
        component.totalStake = jasmine.createSpy().and.returnValue('1.00');
        component.quickDeposit.showQuickDepositForm = true;
        component.quickDeposit.quickDepositFormAllowed = true;
        component['overAskService'].isInProcess = true;

        const result = component.isShowQuickDepositBtnShown();
        expect(result).toBeFalsy();
      });
    });

    describe('isShowQuickDepositBtnDisabled', () => {

      it('should disable if overask phase 1', () => {
        component['overAskService'].isOnTradersReview = true;

        expect(component.isShowQuickDepositBtnDisabled()).toBe(true);
      });

      it('should not disable if overask phase 2', () => {
        component['overAskService'].userHasChoice = true;

        expect(component.isShowQuickDepositBtnDisabled()).toBe(false);
      });

      it('should disable if NOT overask phase 2 and bet placing in progress', () => {
        component.placeBetsPending = true;

        expect(component.isShowQuickDepositBtnDisabled()).toBe(true);
      });

      it('should disable if NOT overask phase 2 and quickDeposit in progress', () => {
        component.quickDeposit.quickDepositPending = true;

        expect(component.isShowQuickDepositBtnDisabled()).toBe(true);
      });

    });
  });

  describe('@allowQuickDeposit', () => {
    it('returns true when user enter more pounds when user sport balance', () => {
      component['currentStakeWithoutDisabledBets'] = 500;
      Object.defineProperty(component['userService'], 'sportBalance', { value: 10 });

      const result = component.allowQuickDeposit();
      expect(result).toBeTruthy();
    });

    it('returns false when user enter equal pounds when user"s sport balance', () => {
      component['currentStakeWithoutDisabledBets'] = 10;
      Object.defineProperty(component['userService'], 'sportBalance', { value: 10 });

      const result = component.allowQuickDeposit();
      expect(result).toBeFalsy();
    });

    it('returns false when user enter less pounds than user"s sport balance', () => {
      component['currentStakeWithoutDisabledBets'] = 2;
      Object.defineProperty(component['userService'], 'sportBalance', { value: 10 });

      const result = component.allowQuickDeposit();
      expect(result).toBeFalsy();
    });

    it('returns false if user logged out', () => {
      userService.status = false;
      expect(component.allowQuickDeposit()).toBeFalsy();
    });

    it('always returns false if tote bets are in betslip', () => {
      component['isToteBets'] = true;
      expect(component.allowQuickDeposit()).toBeFalsy();
    });
  });

  it('getOldPrice', () => {
    const bet = {
      Bet: {
        legs: [
          {
            parts: [
              {
                outcome: {
                  oldModifiedPrice: '1/2'
                }
              }
            ]
          }
        ]
      }
    };
    expect(component.getOldPrice(bet)).toEqual('1/2');
    bet.Bet.legs[0].parts[0].outcome.oldModifiedPrice = null;
    expect(component.getOldPrice(bet)).toEqual('');
  });

  describe('setStakes', () => {
    beforeEach(() => {
      component.setAmount = jasmine.createSpy('setAmount').and.callFake(() => {});

      component.betSlipSingles = [{ disabled: false }];
    });

    it('should not set stakes if device is mobile and custom keyboard is not fired', () => {
      component.isDidigitKeyboardInit = false;
      deviceService.isMobileOnly = true;

      component.setStakes();

      expect(storageService.set).not.toHaveBeenCalled();
      expect(component.setAmount).not.toHaveBeenCalled();
    });

    it('should call storageService.set', () => {
      component.allStakes = { value: '10.00' };

      component.setStakes();

      expect(storageService.set).toHaveBeenCalledWith('all-stakes', '10.00');
    });

    it('should call setAmount', () => {
      component.allStakes = { value: '10.00' };

      component.setStakes();

      expect(component.changedFromAllStakeField).toBeTruthy();
      expect(component.setAmount).toHaveBeenCalledTimes(1);
      expect(component.setAmount).toHaveBeenCalledWith({ disabled: false }, '10.00');
    });

    it('should set allStakesAmount as empty', () => {
      component.allStakes = { value: '0.00' };

      component.setStakes();

      expect(storageService.set).toHaveBeenCalledWith('all-stakes', '');
    });
  });

  it('checkStakeStatus should check totalStake, errorMessage and amountNeeded', () => {
    component.totalStake = jasmine.createSpy('totalStake').and.returnValue('10.00');
    component.getErrorMsg = jasmine.createSpy('getErrorMsg').and.returnValue('test error Message');
    component.isAmountNeeded = jasmine.createSpy('isAmountNeeded').and.returnValue(true);

    component['checkStakeStatus']();

    expect(component.totalStake).toHaveBeenCalled();
    expect(component.getErrorMsg).toHaveBeenCalled();
    expect(component.isAmountNeeded).toHaveBeenCalled();
    expect(component.totalStakeAmount).toEqual('10.00');
    expect(component.errorMessage).toEqual('test error Message');
    expect(component.neededAmountForPlaceBetIsChanged).toBeTruthy();
  });

  describe('setAmount', () => {
    beforeEach(() => {
      component.placeSuspendedErr = {} as any;
    });

    it('set stake amount', () => {
      const bet = {
        Bet: {
          stake: {},
          betOffer: {}
        },
        stake: {}
      };

      component['checkStakeStatus'] = jasmine.createSpy('checkStakeStatus');

      component.setAmount(bet, "2");

      expect(component['checkStakeStatus']).toHaveBeenCalledWith();
    });

    describe('should set stake amount from', ()  => {
      const bet = {
        Bet: {
          stake: {
            perLine: null
          },
          betOffer: {}
        },
        stake: {}
      };

      it('single field input', () => {
        component.changedFromAllStakeField = false;
        component.setAmount(bet, "2");

        expect(bet.Bet.stake.perLine).toEqual("2");
      });

      it('allStakes field input', () => {
        component.changedFromAllStakeField = true;
        component.allStakes = {
          value: '20'
        };
        component.setAmount(bet, "10");

        expect(bet.Bet.stake.perLine).toEqual('20');
      });
    });

    it('clear error', () => {
      component['clearSingleBetPriceChangeErr'] = jasmine.createSpy('clearSingleBetPriceChangeErr');
      component.setAmount({
        Bet: {
          stake: {}, betOffer: {}
        },
        stake: {},
        error: 'PRICE_CHANGED'
      }, "2");
      component.setAmount({
        Bet: {
          stake: {}, betOffer: {}
        },
        stake: {},
        handicapError: 'HANDICAP_CHANGED'
      }, "2");
      expect(component['clearSingleBetPriceChangeErr']).toHaveBeenCalledTimes(2);
    });

    it('set acca offer validity', () => {
      let bet;
      userService.status = false;

      bet = {
        Bet: {
          stake: {},
          betOffer: { offer: {} }
        },
        stake: {}
      };
      component.setAmount(bet, "2");
      expect(bet.Bet.betOffer.isAccaValid).toBeTruthy();

      bet = {
        Bet: {
          stake: {},
          betOffer: { offer: {} }
        },
        stake: {}
      };
      component.setAmount(bet, "2");
      expect(bet.Bet.betOffer.isAccaValid).toBeTruthy();

      bet = {
        Bet: {
          stake: {},
          betOffer: { offer: {} }
        },
        stake: {}
      };
      component.setAmount(bet, "1");
      expect(bet.Bet.betOffer.isAccaValid).toBeFalsy();
    });

    it('boost active', () => {
      component.isBoostActive = true;
      component.setAmount({
        Bet: {
          stake: {}, betOffer: {}
        },
        stake: {}
      }, "1");
      expect(commandService.execute).toHaveBeenCalledWith('ODDS_BOOST_MAX_STAKE_EXCEEDED', jasmine.any(Array));
    });
  });

  it('it should call  onstakeInputChangeEvents() when output:removeFrombetList ', () => {
    const output : ILazyComponentOutput= {
      output: 'removeFrombetList',
      value: {
        lottoData:'test'
      }  
    }
    const spy3 = spyOn(component, 'removeFromBetslip');
    component.onstakeInputChangeEvents(output);
    expect(spy3).toHaveBeenCalled();
   });

 it('it should call  onstakeInputChangeEvents() when output:lottoBetsEmitter ', () => {
    const output : ILazyComponentOutput= {
      output: 'lottoBetsEmitter',
      value: {
        lottoData:'test'
      }  
    }
    component['updateBetSlipHeight'] = jasmine.createSpy().and.callThrough(); 
    component.onstakeInputChangeEvents(output);
    expect(component['updateBetSlipHeight']).toHaveBeenCalled();
  });

  it('it should call  onstakeInputChangeEvents() when lottoData Avaliable ', () => {
    const output : ILazyComponentOutput= {
      output: '',
      value: {
        lottoData:[]
      }  
    }
    component['checkStakeStatus'] = jasmine.createSpy('checkStakeStatus');
    component.onstakeInputChangeEvents(output);
    expect(component['checkStakeStatus']).toHaveBeenCalled();
  });

  it('it should call onstakeInputChangeEvents() when removeErrorMsg', () => {
    const output : ILazyComponentOutput= {
      output: 'removeErrorMsg'
    } as any;
    component['checkStakeStatus'] = jasmine.createSpy('checkStakeStatus');
    component.onstakeInputChangeEvents(output);
    expect(component['checkStakeStatus']).not.toHaveBeenCalled();
  });

  it('it should call onQuickDepositEvents case1', () => {
    const spy = spyOn(component, 'onOpenIframe');
    component. onQuickDepositEvents({ output: 'openIframeEmit'});
    expect(spy).toHaveBeenCalled(); 
  });

  it('it should call onQuickDepositEvents case2', () => {
    const spy = spyOn(component, 'handleBetslipUpdate');
    component. onQuickDepositEvents({ output: 'quickDepositStakeChange'});
    expect(spy).toHaveBeenCalled(); 
  });
  it('it should call onQuickDepositEvents case3', () => {
    const spy = spyOn(component, 'onCloseQuickDepositWindow');
    component. onQuickDepositEvents({ output: 'closeWindow'});
    expect(spy).toHaveBeenCalled(); 
  });
  it('it should call onQuickDepositEvents case4', () => {
    const spy = spyOn(component, 'closeIFrame');
    component. onQuickDepositEvents({ output: 'closeIframeEmit'});
    expect(spy).toHaveBeenCalled(); 
  });
  it('it should call onQuickDepositEvents  case default', () => {
    const spy = spyOn(component, 'closeIFrame');
    component. onQuickDepositEvents({ output: 'closeIframeEmit123'});
    expect(spy).not.toHaveBeenCalled(); 
  });

  it('it should call isLottoBet()',()=>{
    const betslipData =[
      {
        isLotto : true ,
        params :{
          lottoData : {
            isLotto : true
          }
        }
      
      }
    ]
    component.isLottoBet(betslipData);
    expect(betslipData[0].isLotto).toBeTruthy();
    expect(betslipData[0].params.lottoData).toBeTruthy();
  })



  describe('setMultipleSuspendedErrMsg', () => {
    it('should setMultipleSuspendedErrMsg', () => {
      const bet = {
        type: 'DBL'
      };
      component.placeSuspendedErr = <any>{
        multipleWithDisableSingle: false
      };
      component['suspendedOutcomesCounter'] = 2;
      component['setMultipleSuspendedErrMsg'](<any>bet);
      expect(betslipService.getSuspendedMessage).toHaveBeenCalledWith(2);
    });

    it('should setMultipleSuspendedErrMsg (suspendedOutcomesCounter = 0)', () => {
      const bet = {
        type: 'DBL'
      };
      component.placeSuspendedErr = <any>{
        multipleWithDisableSingle: false
      };
      component['suspendedOutcomesCounter'] = 0;
      component['setMultipleSuspendedErrMsg'](<any>bet);
      expect(betslipService.getSuspendedMessage).not.toHaveBeenCalled();
    });
  });

  describe('handleFreebetOutput', () => {
    beforeEach(() => {
      spyOn(component, 'setFreebet');
      spyOn(component, 'setAmount');
      spyOn(component, 'hideFreeBetNotification');
      betslipService.isFreeBetValid.and.returnValue(true);
    });

    it('should not handle not selectedChange event', () => {
      const outputEvent = {
        output: 'notSelectedChange',
        value: {
          value: 5
        }
      };
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;

      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setFreebet).not.toHaveBeenCalled();
    });

    it('should handle selectedChange event', () => {
      const outputEvent = {
        output: 'selectedChange',
        value: {
          value: 5
        }
      };
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {
          stake: {
            perLine: 1
          }
        },
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;

      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setFreebet).toHaveBeenCalledWith(bet);
      expect(betslipService.isFreeBetValid).toHaveBeenCalledWith(outputEvent.value.value, bet);
    });

    it('should handle selectedChange event', () => {
      const outputEvent = {
        output: 'selectedChange',
        value: {
          value: 5
        }
      };
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {
          stake: {
            perLine: 2
          }
        },
        selectedFreeBet: {},
        stake: {
          perLine: 2
        }
      } as IBetslipBetData;

      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setAmount).toHaveBeenCalledWith(bet, '');
    });

    it('should handle selectedChange event but not apply free bet if it is not valid', () => {
      const outputEvent = {
        output: 'selectedChange',
        value: {
          value: 5
        }
      };
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {
          stake: {
            perLine: 1
          }
        },
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;
      betslipService.isFreeBetValid.and.returnValue(false);

      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setFreebet).not.toHaveBeenCalled();
      expect(betslipService.isFreeBetValid).toHaveBeenCalledWith(outputEvent.value.value, bet);
    });

    it('should handle selectedChange event when remove freebet was clicked', () => {
      const outputEvent = {
        output: 'selectedChange',
        value: undefined
      };
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {
          stake: {
            perLine: 1
          }
        },
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;
      betslipService.isFreeBetValid.and.returnValue(false);

      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setFreebet).toHaveBeenCalledWith(bet);
      expect(bet.selectedFreeBet).toEqual(undefined);
    });

    it('should not handle toteBet event', () => {
      const numOfLines = 2
      const outputEvent = {
        output: 'toteBet',
        value: {
          freebetTokenValue: 5
        }
      };
      storageService.get.and.returnValue({
        poolBet: {
          poolType: 'UTRI'
        },
        toteBetDetails:{
          betName:'1 "REVERSE"',
          orderedOutcomes: [{ runnerNumber: '1' }]
        }
      });
      const bet1: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;
      component.toteBetSlip = {toteBet: {poolBet: {stakePerLine: ''}}} as any;
      component.handleFreebetOutput(outputEvent, bet1);
      expect(component.setFreebet).not.toHaveBeenCalled();
      storageService.get.and.returnValue({
        poolBet: {
          poolType: 'UEXA'
        },
        toteBetDetails:{
          betName:'1 REVERSE',
          orderedOutcomes: [{}]
        }
      });
      const bet2: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;
      component.toteBetSlip = {toteBet: {poolBet: {stakePerLine: ''}}} as any;
      component.handleFreebetOutput(outputEvent, bet2);
      expect(component.setFreebet).not.toHaveBeenCalled();
      storageService.get.and.returnValue({
        poolBet: {
          poolType: 'UEXA'
        },
        toteBetDetails:{
          betName:'2 REVERSE1',
          numberOfLines: 2
        }
      });
      const bet: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;

      component.toteBetSlip = {toteBet: {poolBet: {stakePerLine: ''}}} as any;
      component.handleFreebetOutput(outputEvent, bet);
      expect(component.setFreebet).not.toHaveBeenCalled();
      storageService.get.and.returnValue({
        poolBet: {
          poolType: 'UEXA1'
        },
        toteBetDetails:{
          betName:'2 REVERSE1',
          numberOfLines: 2
        }
      });
      const bet3: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;

      component.toteBetSlip = {toteBet: {poolBet: {stakePerLine: ''}}} as any;
      component.handleFreebetOutput(outputEvent, bet3);
      expect(component.setFreebet).not.toHaveBeenCalled();
      storageService.get.and.returnValue({
        poolBet: {
          poolType: 'UEXA1'
        },
        toteBetDetails:{
          betName:'2 REVERSE1',
          orderedOutcomes: [{}]
        }
      });
      const bet4: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;

      component.toteBetSlip = {toteBet: {poolBet: {stakePerLine: ''}}} as any;
      component.handleFreebetOutput(outputEvent, bet4);
      expect(component.setFreebet).not.toHaveBeenCalled();
    });

    it('should not handle removetoteFreeBet event', () => {
      const outputEvent = {
        output: 'removetoteFreeBet',
        value: {
          freebetTokenValue: 5
        }
      };
      storageService.get.and.returnValue({
        poolBet: {
          freebetTokenId: 267598,
          freebetTokenValue:1
        }
      });
      const bet1: any = {
        error: 'PRICE_CHANGED',
        Bet: {},
        selectedFreeBet: {},
        stake: {}
      } as IBetslipBetData;
  
      component.handleFreebetOutput(outputEvent, bet1);
      expect(component.setFreebet).not.toHaveBeenCalled();
    });
  });

  
  it('should init betslip after login if bpp token defined', () => {
    pubSubService.subscribe.and.callFake((p1, p2, cb) => {
      if (p2 && (p2[0] === 'SUCCESSFUL_LOGIN' || p2[1] === 'SESSION_LOGIN')) {
        cb();
      }
    });
    userService.bppToken = '123';
    component['init'] = jasmine.createSpy('init');
    component.ngOnInit();
    expect(component['init']).toHaveBeenCalled();
  });

  describe('@rejectOffer', () => {

    it('should open info dialog', () => {
      component.rejectOffer();

      expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith(
        jasmine.any(String),
        jasmine.any(String),
        'bs-overask-dialog',
        undefined,
        undefined,
        [{
          cssClass: 'btn-style4',
          caption: jasmine.any(String),
        }, {
          caption: jasmine.any(String),
          cssClass: 'btn-style2',
          handler: jasmine.any(Function)
        }]
      );
    });

    it('should get locals for all texts', () => {
      component.rejectOffer();

      expect(localeService.getString).toHaveBeenCalledTimes(4);
    });

    it('button handler should close popup and trigger overask rejecting', () => {
      infoDialogService.openInfoDialog.and.callFake((a, b, c, d, e, buttons: any[]) => {
        buttons.forEach(btn => {
          btn.handler && btn.handler();
        });
      });
      component.rejectOffer();

      expect(component.overask.rejectOffer).toHaveBeenCalledWith(false);
      expect(infoDialogService.closePopUp).toHaveBeenCalled();
    });
  });
  describe('@updateBsButtonTitle', () => {
    it('updateBsButtonTitle not logged in', () => {
      userService.status = false;
      component['updateBsButtonTitle']();
      expect(component.bsButtonTitle).toBe('bs.betNowLogIn');
    });

    it('updateBsButtonTitle logged in', () => {
      component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
      userService.status = true;
      component['updateBsButtonTitle']();
      expect(component.bsButtonTitle).toBe('bs.betNow');
    });

    it('updateBsButtonTitle Price Changed', () => {
      component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
      userService.status = true;
      component.betSlipSingles = [{ error: 'PRICE_CHANGED' }];
      component['updateBsButtonTitle']();
      expect(component.bsButtonTitle).toBe('bs.acceptBet');
    });

    it('updateBsButtonTitle Handicap changed', () => {
      component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(false);
      userService.status = true;
      component.betSlipSingles = [{ handicapError: 'HANDICAP_CHANGED' }];
      component['updateBsButtonTitle']();
      expect(component.bsButtonTitle).toBe('bs.acceptBet');
    });

    it('updateBsButtonTitle price changed(isPriceUpdate === true)', () => {
      component['isPriceUpdate'] = jasmine.createSpy('isPriceUpdate').and.returnValue(true);
      userService.status = true;
      component.betSlipSingles = [{ error: '' }];
      component['updateBsButtonTitle']();
      expect(component.bsButtonTitle).toBe('bs.acceptBet');
    });
  });

  it('isPlaceButtonShown', () => {
    component.placeBetsPending = false;
    overAskService.isInProcess = false;
    component.quickDeposit = { quickDepositPending: false } as any;
    expect(component.isPlaceButtonShown()).toBeTruthy();

    component.quickDeposit.quickDepositPending = true;
    expect(component.isPlaceButtonShown()).toBeFalsy();

    overAskService.isInProcess = true;
    expect(component.isPlaceButtonShown()).toBeFalsy();

    component.placeBetsPending = true;
    expect(component.isPlaceButtonShown()).toBeFalsy();
  });

  describe('clearStakes', () => {
    beforeEach(() => {
      component['unsetFreeBets'] = jasmine.createSpy('unsetFreeBets');
      component['clearAllStakesHolder'] = jasmine.createSpy('unsetFreeBets');
      component.setAmount = jasmine.createSpy('setAmount');
    });

    it('should clear all stakes', () => {
      component['betData'] = null;
      component['clearStakes']();

      expect(component['clearAllStakesHolder']).toHaveBeenCalled();
      expect(component.setAmount).not.toHaveBeenCalled();
      expect(component['unsetFreeBets']).not.toHaveBeenCalled();
    });

    it('should clear betData', () => {
      component['betData'] = [{}, {}];
      component['clearStakes']();

      expect(component['clearAllStakesHolder']).toHaveBeenCalled();
      expect(component.setAmount).toHaveBeenCalledTimes(2);
      expect(component['unsetFreeBets']).toHaveBeenCalledWith(component['betData']);
    });
  });

  it('placeBets catchError should handle error', fakeAsync(() => {
    component['freeBetsStoreUpdate'] = jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
    toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
    betslipService.areBetsWithStakes.and.returnValue(true);
    component['betData'] = [{
      stake: { perLine: 2, min: 1 }
    }] as any;
    component.quickDeposit = {} as any;
    component.betSlipSingles = [];
    component['handleError'] = jasmine.createSpy('handleError');
    component['isFreeBetApplied'] = true;
    const error = { error: {} };
    component.lottobetslipData =[{ isLotto :true},{}]
 
    betslipService.placeBets.and.returnValue(throwError(error));
    component.placeBets().subscribe(null, () => {});
    tick();

    expect(component['handleError']).toHaveBeenCalledWith(error);
    expect(component.lottobetslipData).toBeTruthy();
  }));

  it('placeBets catchError should handle error', fakeAsync(() => {
    component['freeBetsStoreUpdate'] = jasmine.createSpy('freeBetsStoreUpdate').and.returnValue([]);
    toteBetslipService.isToteBetWithProperStake.and.returnValue(false);
    betslipService.areBetsWithStakes.and.returnValue(true);
    component['betData'] = [{
      stake: { perLine: 2, min: 1 }
    }] as any;
    component.quickDeposit = {} as any;
    component.betSlipSingles = [];
    component['handleError'] = jasmine.createSpy('handleError');
    component['isFreeBetApplied'] = false;
    component.lottobetslipData =[];
    const error = { error: {}};
    betslipService.placeBets.and.returnValue(throwError(error));
    component.placeBets().subscribe(null, () => {});
    tick();

    expect(component['handleError']).toHaveBeenCalledWith(error);
  }));

  it('core exucuteOverask should handle error', fakeAsync(() => {
    const overaskData = {
      bets: [{}]
    };
    const error = { error: {}};
    component.quickDeposit = {
      pending: false
    } as any;
    component['handleError'] = jasmine.createSpy('handleError');
    betslipService.exucuteOverask = jasmine.createSpy().and.returnValue(throwError(error));
    component['core']([], overaskData);
    deviceService.isDesktop = false;

    tick();
    expect(betslipService.exucuteOverask).toHaveBeenCalledWith(overaskData);
    expect(component['handleError']).toHaveBeenCalledWith(error);
    expect(component.isHeightUpdated).toBeFalse();
  }));

  it('it Should call core () shouldHandicapBeUpadatd', () => {
    const spy = spyOn(component, 'checkStake');
    const data = [
      {
        isLotto: true,
        combiName: 'SCORECAST',
        params: {
          lottoData: {
            isLotto: true
          },
        },
        stake: {
          stakePerLine: ''

        },
        info: () => ({
          price: { priceNum: 3, priceDen: 4 },
          type: 'SGL',
          Bet: {
            freeBets: [],
            params: {
              lottoData: {}
            }
          },
          combiName: 'SCORECAST',
          outcomeId: '1234',
          isFCTC: true  
        }),
        updateHandicap: jasmine.createSpy(),
        legs: [
          {
            parts: [
              {
                outcome: {
                  prices: [
                    {
                      handicapValueDec: 'abc'
                    }]
                }
              }
            ]
          }
        ],
        Bet: {
          freeBets: []
        },
    },
    {
      isLotto: true,
      combiName: 'SCORECAST',
      params: {
        lottoData: {
          isLotto: false
        },
      },
      stake: {
        stakePerLine: ''

      },
      info: () => ({
        price: { priceNum: 3, priceDen: 4 },
        type: 'TBL',
        Bet: {
          freeBets: [],
          params: {
            lottoData: {}
          }
        },
        combiName: 'SCORECAST',
        outcomeId: '1234',
        isFCTC: true
      }),
     updateHandicap: jasmine.createSpy(),
      legs: [
        {
          parts: [
            {
              outcome: {
                prices: [
                  {
                    handicapValueDec: 'abc'
                  }]
              }
            }
          ]
        }
      ],
      
    }];
    const overaskData = {
      bets: [
        {
          freebet: [
            {
              id: '1234'
            }
          ]
        }
      ]
    }
     component['core'](data, overaskData);
   });

  it('should deactivate odds boost if last selection removed', fakeAsync(() => {
    component.isBoostEnabled = true;
    component.isBoostActive = true;
    deviceService.isDesktop = true;
    spyOn(component, 'checkStake');
    component['core']([]);

    tick();
    expect(pubSubService.publish).toHaveBeenCalledWith('ODDS_BOOST_CHANGE', false);
    expect(component.isHeightUpdated).toBeTrue();
  }));

  describe('handleError', () => {
    beforeEach(() => {
      spyOn<any>(component, 'init');
      component['clearStakes'] = jasmine.createSpy('clearStakes');
      component['betslipErrorTracking'] = jasmine.createSpy('betslipErrorTracking');
    });

    it('should not track error and clear stakes if no error', () => {
      component['handleError'](null);

      expect(component['init']).not.toHaveBeenCalled();
      expect(component['clearStakes']).not.toHaveBeenCalled();
      expect(component['betslipErrorTracking']).not.toHaveBeenCalled();
    });

    it('should not track error and clear stakes if no error', () => {
      const error = {
        data: {
          offerTimeExpired: '',
          status: 'LOW_FUNDS'
        },
        status: 'status',
        statusText: 'statusText',
        message: 'message',
      };
      component['handleError'](error);

      expect(component['init']).toHaveBeenCalled();
      expect(component['clearStakes']).not.toHaveBeenCalled();
    });

    it('should track error with status and statuText', () => {
      const error = {
        status: 'status',
        statusText: 'statusText',
        message: 'message',
      };

      component.betSlipSingles = [];
      component.betSlipMultiples = [{}, {}];
      component['handleError'](error);

      expect(component['init']).not.toHaveBeenCalled();
      expect(component['clearStakes']).not.toHaveBeenCalled();
      expect(component['betslipErrorTracking']).toHaveBeenCalledWith(component.betSlipSingles, component.betSlipMultiples, [error],
        'status', 'statusText');
    });

    it('should track error with message', () => {
      const error = {
        message: 'message'
      };

      component.betSlipSingles = [];
      component.betSlipMultiples = [{}, {}];
      component['handleError'](error);

      expect(component['init']).not.toHaveBeenCalled();
      expect(component['clearStakes']).not.toHaveBeenCalled();
      expect(component['betslipErrorTracking']).toHaveBeenCalledWith(component.betSlipSingles, component.betSlipMultiples, [error],
        false, 'message');
    });

    it('should track error data', () => {
      const error = {};

      component.betSlipSingles = [];
      component.betSlipMultiples = [{}, {}];
      component['handleError'](error);

      expect(component['init']).not.toHaveBeenCalled();
      expect(component['clearStakes']).not.toHaveBeenCalled();
      expect(component['betslipErrorTracking']).toHaveBeenCalledWith(component.betSlipSingles, component.betSlipMultiples, [error],
        false, false);
    });

    it('should clear stakes if offerTimeExpired', () => {
      const error = {
        data: {
          offerTimeExpired: true
        }
      };

      component.betSlipSingles = [];
      component.betSlipMultiples = [{}, {}];
      component['handleError'](error);

      expect(component['init']).toHaveBeenCalled();
      expect(component['clearStakes']).toHaveBeenCalled();
      expect(component['betslipErrorTracking']).not.toHaveBeenCalled();
    });

    it('should clear stakes if PT_ERR_AUTH', () => {
      const error = {
        data: {
          status: 'PT_ERR_AUTH'
        }
      };

      component.betSlipSingles = [];
      component.betSlipMultiples = [{}, {}];
      component['handleError'](error);

      expect(component['clearStakes']).toHaveBeenCalled();
      expect(component['betslipErrorTracking']).not.toHaveBeenCalled();
    });
  });

  describe('removeFromOffer', () => {
    it('Should remove from offer list when list length is 1', () => {
      const bet = {
        isSelected: false,
        id: 'id'
      };
      component.overask.isOveraskCanBePlaced  = jasmine.createSpy('isOveraskCanBePlaced').and.returnValue(false);
      component.betSlipSingles = [bet];

      component.removeFromOffer(bet.id);

      expect(overAskService.collectDeletedBetID).toHaveBeenCalledWith(bet.id);
      expect(component.isBetsSelected).toBe(false);
      expect(component.isOveraskCanBePlaced).toBe(false);
    });

    it('Should from offer list when list length is 2', () => {
      const bet1 = {
        isSelected: false,
        id: 'id1'
      };
      const bet2 = {
        isSelected: true,
        id: 'id2'
      };
      component.overask.isOveraskCanBePlaced  = jasmine.createSpy('isOveraskCanBePlaced').and.returnValue(true);
      component.betSlipSingles = [bet1, bet2];

      component.removeFromOffer(bet1.id);

      expect(overAskService.collectDeletedBetID).toHaveBeenCalledWith(bet1.id);
      expect(component.isBetsSelected).toBe(true);
      expect(component.isOveraskCanBePlaced).toBe(true);
    });

    it('should check if betErrors length greather than 0', () => {
      component.lottoErrorMsg = null;
      const data = {errs: [{errorCode: 'stake low'}]} as any;
      component.getLottoMessage(data);
      expect(component.lottoErrorMsg).toEqual(data.errs[0]);
    });

    it('should check if betErrors length is equal to 0', () => {
      component.lottoErrorMsg = null;
      const data = {errs: []};
      component.getLottoMessage(data);
      expect(component.lottoErrorMsg).toBe(null);
    });
  });

  describe('undoOveraskBetRemove', () => {
    it('should remove make bet selected again', () => {
      const bet = {
        isSelected: false,
        id: 'id'
      };
      component['calculateIsBetsSelected'] = jasmine.createSpy('component.calculateIsBetsSelected');
      component['undoOveraskBetRemove'](bet);

      expect(bet.isSelected).toBe(true);
      expect(component['calculateIsBetsSelected']).toHaveBeenCalled();
      expect(component.overask.removeDeletedBetID).toHaveBeenCalledWith(bet.id);
    });
  });

  describe('selectionLiveUpdate', () => {
    let bet;

    beforeEach(() => {
      bet = {
        info: jasmine.createSpy('info').and.returnValue({ id: 'SGL|1' }),
        history: {
          isPriceChanged: jasmine.createSpy('isPriceChanged'),
          isPriceChangedAndMarketUnsuspended: jasmine.createSpy('isPriceChangedAndMarketUnsuspended')
        }
      };
    });

    it('price changed', () => {
      bet.history.isPriceChanged.and.returnValue(true);
      component['selectionLiveUpdate'](bet);
      expect(component['priceChangeBets'].has('SGL|1')).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith('bs.priceChangeBannerMsg');
    });

    it('price changed (market unsuspended)', () => {
      bet.history.isPriceChangedAndMarketUnsuspended.and.returnValue(true);
      component['selectionLiveUpdate'](bet);
      expect(component['priceChangeBets'].has('SGL|1')).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith('bs.priceChangeBannerMsg');
    });

    it('price changed (reboost)', () => {
      bet.history.isPriceChanged.and.returnValue(true);
      component['reboost'] = true;
      component['selectionLiveUpdate'](bet);
      expect(localeService.getString).toHaveBeenCalledWith('bs.reboostPriceChangeBannerMsg');
    });

    it('price not changed', () => {
      component['selectionLiveUpdate'](bet);
      expect(component['priceChangeBets'].size).toBe(0);
    });
  });

  describe('restoreOveraskProcess', () => {
    it('should call getOveraskDrawerConfig if overask is inProcess and isOnTraderReview', fakeAsync(() => {
      const spy = spyOn(component as any, 'getOveraskDrawerConfig');

      component.overask.isInProcess = true;
      component.overask.isOnTradersReview = true;
      component.restoreOveraskProcess();
      tick();

      expect(spy).toHaveBeenCalled();
    }));


    it('should not call getOveraskDrawerConfig if overask inProcess is not set', fakeAsync(() => {
      const spy = spyOn(component as any, 'getOveraskDrawerConfig');

      component.overask.isInProcess = false;
      component.overask.isOnTradersReview = true;
      component.restoreOveraskProcess();
      tick();

      expect(spy).not.toHaveBeenCalled();
    }));

    it('should call getOveraskDrawerConfig if overask isOnTraderReview is not set', fakeAsync(() => {
      const spy = spyOn(component as any, 'getOveraskDrawerConfig');

      component.overask.isInProcess = true;
      component.overask.isOnTradersReview = false;
      component.restoreOveraskProcess();
      tick();

      expect(spy).not.toHaveBeenCalled();
    }));
  });

  describe('isDepositAndPlaceBets', () => {
    it('should show deposit and place bet title', () => {
      component['placeBetsPending'] = false;
      component['overask'].isNotInProcess = false;
      component['quickDeposit'] = {
        quickDepositPending: false
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeTruthy();
    });

    it('should show deposit and place bet title when only placeBetsPending', () => {
      component['placeBetsPending'] = true;
      component['overask'].isNotInProcess = false;
      component['quickDeposit'] = {
        quickDepositPending: false
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeTruthy();
    });

    it('should show deposit and place bet title when only overask is in progress', () => {
      component['placeBetsPending'] = false;
      component['overask'].isNotInProcess = true;
      component['quickDeposit'] = {
        quickDepositPending: false
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeTruthy();
    });

    it('should show deposit and place bet title when only quickDepositPending', () => {
      component['placeBetsPending'] = false;
      component['overask'].isNotInProcess = false;
      component['quickDeposit'] = {
        quickDepositPending: true
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeTruthy();
    });

    it('should not show deposit and place bet title when placeBetsPending and quickDepositPending', () => {
      component['placeBetsPending'] = true;
      component['overask'].isNotInProcess = false;
      component['quickDeposit'] = {
        quickDepositPending: true
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeFalsy();
    });

    it('should not show deposit and place bet title when overask isNotInProcess and quickDepositPending', () => {
      component['placeBetsPending'] = false;
      component['overask'].isNotInProcess = true;
      component['quickDeposit'] = {
        quickDepositPending: true
      } as IBetslipDepositData;

      expect(component.isDepositAndPlaceBets()).toBeFalsy();
    });
  });

  describe('handleOverAskProcessing', () => {
    it('should call method getOveraskDrawerConfig', () => {
      const spyOnConfig = spyOn(component as any, 'getOveraskDrawerConfig');
      (component['handleOverAskProcessing'] as any)();

      expect(spyOnConfig).toHaveBeenCalled();
    });
  });

  describe('getOveraskDrawerConfig', () => {
    it('should not call cmsService.getSystemConfig if overaskDrawerIsConfigured is true', () => {
      component.overaskDrawerIsConfigured = true;

      (component['getOveraskDrawerConfig'] as any)();

      expect(cmsService.getFeatureConfig).not.toHaveBeenCalled();
    });

    it('should get config from cms', fakeAsync(() => {
      component.overaskDrawerIsConfigured = false;

      (component['getOveraskDrawerConfig'] as any)();
      tick();

      expect(component.overaskProcessingTitle).toBe('title');
      expect(component.overaskProcessingTopMessage).toBe('top message');
      expect(component.overaskProcessingBottomMessage).toBe('bottom message');
      expect(component.overaskDrawerIsConfigured).toBe(true);
    }));
  });

  describe('isRacingOrVirtual', () => {
    it('isRacingOrVirtual (racing)', () => {
      const stake = {
        isRacingSport: true
      };
      expect(component.isRacingOrVirtual(<any>stake)).toBe(true);
    });

    it('isRacingOrVirtual (virtual)', () => {
      const stake = {
        sport: 'Virtual Sports'
      };
      expect(component.isRacingOrVirtual(<any>stake)).toBe(true);
    });

    it('isRacingOrVirtual (football)', () => {
      const stake = {
        sport: 'Football'
      };
      expect(component.isRacingOrVirtual(<any>stake)).toBe(false);
    });
  });

  describe('getEventTime', () => {
    it('getEventTime (racing)', () => {
      const stake = {
        isRacingSport: true,
        localTime: '12:23'
      };
      expect(component.getEventTime(<any>stake)).toBe('12:23 ');
    });

    it('getEventTime (virtual)', () => {
      const stake = {
        isRacingSport: false,
        localTime: '12:23'
      };
      expect(component.getEventTime(<any>stake)).toBe('13:20 ');
    });
  });

  describe('setDepositBtnTitle', () => {
    it('should set deposit btn as bs.acceptPlaceBetDeposit if there is hcap/price update', () => {
      component['isPriceOrHcapUpdate'] = jasmine.createSpy().and.returnValue(true);
      component.setDepositBtnTitle();
      expect(component.setDepositBtnTitle()).toBeTruthy();
      expect(component.depositButtonTitle).toEqual('bs.acceptPlaceBetDeposit');
    });

    it('should set deposit btn as bs.betslipDepositBtn in other cases', () => {
      component['isPriceOrHcapUpdate'] = jasmine.createSpy().and.returnValue(false);
      component.setDepositBtnTitle();
      expect(component.setDepositBtnTitle()).toBeTruthy();
      expect(component.depositButtonTitle).toEqual('bs.betslipDepositBtn');
    });
  });

  describe('tracking error on init', () => {
    it('should not track error for success flow', fakeAsync(() => {
      component['betslipService'].fetch = jasmine.createSpy().and.returnValue(of(null));
      component['init']();
      tick();

      expect(awsService.addAction).not.toHaveBeenCalled();
    }));

    it('should not track error if no events', fakeAsync(() => {
      spyOn<any>(component, 'cleanBetslip');
      component['betslipService'].fetch = jasmine.createSpy().and.returnValue(throwError({ message: 'no events' }));
      component['init']();
      tick();

      expect(awsService.addAction).not.toHaveBeenCalled();
    }));

    it('should not track error', fakeAsync(() => {
      component['betslipService'].fetch = jasmine.createSpy().and.returnValue(throwError({}));
      component['init']();
      tick();

      expect(awsService.addAction).toHaveBeenCalledTimes(2);
    }));
  });

  it('should trigger pubsub event onQuickStakeSelect', () => {
    const value = '10.00';

    component.onQuickStakeSelect(value);

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QB_QUICKSTAKE_PRESSED, [value]);
  });

  describe('onKeyboardToggle', () => {
    it('should change quick stake key to false', () => {
      expect(component.quickStakeVisible).toBeTruthy();

      component.onKeyboardToggle(false);

      expect(component.quickStakeVisible).toBeFalsy();
    });
  });

  describe('isFreebetButtonShown', () => {
    it('should return true when overask in not in progress and freebets are available', () => {
      const bet: Partial<IBetslipBetData> = { Bet: { freeBets: [1, 2, 3] } as any };
      component.overask.isInProcess = false;

      expect(component.isFreebetButtonShown(bet as IBetslipBetData)).toBe(true);
    });

    it('should return false when overask in progress', () => {
      const bet: Partial<IBetslipBetData> = { Bet: { freeBets: [1, 2, 3] } as any };
      component.overask.isInProcess = true;
      component.overask.isNoBetsOffered = false;

      expect(component.isFreebetButtonShown(bet as IBetslipBetData)).toBe(false);
    });
    it('should return false freebets are not available', () => {
      const bet: Partial<IBetslipBetData> = { Bet: { } as any };
      component.overask.isInProcess = false;

      expect(component.isFreebetButtonShown(bet as IBetslipBetData)).toBe(false);
    });
  });

  describe('checkForAvailableFreebets', () => {
    beforeEach(() => {
      component.betSlipSingles = [];
    });

    it('should checkForAvailableFreebets', () => {
      component.betSlipSingles = [{ Bet: { freeBets: [{}] } }, { Bet: {} }];
      component['checkForAvailableFreebets']();
      expect(component.freeBetAvailable).toBe(true);
    });

    it('should checkForAvailableFbettokens', () => {
      component.betSlipSingles = [{ Bet: { freeBets: [{freebetOfferCategories:{freebetOfferCategory:'Bet Pack'}}] } }
      ];
      freeBetsService['isBetPack'] = jasmine.createSpy('isBetPack').and.returnValues(true,true);
      freeBetsService['isFanzone'] = jasmine.createSpy('isFanzone').and.returnValue(false);
      component['checkForAvailableFreebets']();
      expect(component.betTokensAvailable).toBe(true);
      expect(component.freeBetAvailable).toBe(false);
    });
    it('should checkForAvailableFanzone', () => {
      component.betSlipSingles = [ { Bet: { freeBets: [{freebetOfferCategories:{freebetOfferCategory:'Fanzone'}}] } }];
      freeBetsService['isFanzone'] = jasmine.createSpy('isFanzone').and.returnValue(true);
      component['checkForAvailableFreebets']();
      expect(component.betTokensAvailable).toBe(false);
      expect(component.freeBetAvailable).toBe(false);
      expect(component.fanZoneAvailable).toBe(true);

    });

    it('should checkForAvailableFreebets (no freebets)', () => {
      component.betSlipSingles = [{ Bet: {} }];
      component['checkForAvailableFreebets']();
      expect(component.freeBetAvailable).toBe(false);
    });

    it('should checkForAvailableFreebets (no bets)', () => {
      component['getAllBets'] = jasmine.createSpy('getAllBets').and.returnValue(null);
      component['checkForAvailableFreebets']();
      freeBetsService.getFreeBetsData = jasmine.createSpy().and.returnValue([{ freebetTokenId: 123 }, { freebetTokenId: 143 }]);
      expect(component.freeBetAvailable).toBe(false);
      expect(component.hideAvailableFreeBetsMessage).toBe(false);
      expect(storageService.remove).toHaveBeenCalledWith(
        `hideAvailableFreeBetsMessage-${userService.username}`
      );
    });
  });

  it('should hideFreeBetNotification', () => {
    component.hideFreeBetNotification();
    expect(component.hideAvailableFreeBetsMessage).toBe(true);
    expect(storageService.set).toHaveBeenCalledWith(
      `hideAvailableFreeBetsMessage-${userService.username}`, true);
  });

  describe('getPriceChangeMessage', () => {
    let betslipStake;

    beforeEach(() => {
      betslipStake = {
        price: { priceType: 'LP' }
      } as any;

      spyOn(component, 'getOldPrice').and.returnValue('foo');
      spyOn(component, 'odds').and.callFake(a => a.price === 'foo' ? '1/2' : '2/1');
      localeService.getString.and.callFake((a, b) => a + b);
    });

    it('should build no message without old price', () => {
      (component.getOldPrice as Spy).and.returnValue('');

      expect(component.getPriceChangeMessage(betslipStake)).toBe('');
      expect(component.getOldPrice).toHaveBeenCalledWith(betslipStake);
      expect(component.odds).not.toHaveBeenCalled();
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should build no message for SP price-change', () => {
      betslipStake.price.priceType = 'SP';

      expect(component.getPriceChangeMessage(betslipStake)).toBe('');
      expect(component.getOldPrice).toHaveBeenCalledWith(betslipStake);
      expect(component.odds).not.toHaveBeenCalled();
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should build no message if odds are same', () => {
      (component.getOldPrice as Spy).and.returnValue('not_foo');

      expect(component.getPriceChangeMessage(betslipStake)).toBe('');
      expect(component.getOldPrice).toHaveBeenCalledWith(betslipStake);
      expect(component.odds).toHaveBeenCalledTimes(2);
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should build price-change message for different odds', () => {
      expect(component.getPriceChangeMessage(betslipStake)).toBe('bs.stakePriceChangeMsg1/2,2/1');
      expect(component.odds).toHaveBeenCalledTimes(2);
      expect(localeService.getString).toHaveBeenCalledWith('bs.stakePriceChangeMsg', ['1/2', '2/1']);
    });
  });

  describe('getAllBets', () => {
    it('should return empty array if no singles', () => {
      component.betSlipSingles = null;
      component.betSlipMultiples = null;

      expect(component['getAllBets']()).toEqual([]);
    });

    it('should return empty array if singles are empty', () => {
      component.betSlipSingles = [];
      component.betSlipMultiples = null;

      expect(component['getAllBets']()).toEqual([]);
    });

    it('should return only singles if no multiples', () => {
      component.betSlipSingles = [{id: 1}];
      component.betSlipMultiples = null;

      expect(component['getAllBets']()).toEqual(component.betSlipSingles);
    });

    it('should return only singles if multiples are empty', () => {
      component.betSlipSingles = [{id: 1}];
      component.betSlipMultiples = [];

      expect(component['getAllBets']()).toEqual(component.betSlipSingles);
    });

    it('should combine singles and multiples', () => {
      component.betSlipSingles = [{id: 1}];
      component.betSlipMultiples = [{id: 2}];

      expect(component['getAllBets']()).toEqual([{id: 1}, {id: 2}] as any);
    });
  });

  it('countDownCurrentValue', () => {
    component['quickDepositService'].countDownCurrentValue = 23 as any;
    component.countDownCurrentValue = 23 as any ;
    expect(component.countDownCurrentValue).toEqual(23 as any);
  });
  it('overask  setter', () => {
    component.overask = {}as any;
    component.scrollWrapper = { nativeElement: true } as ElementRef;
    component.totalStakeIsPresent = {} as any;
    component.defaultQuickDepositData = {} as any;
    component.infoDialogComponent = {} as Type<SelectionInfoDialogComponent>;
    expect(component.overask).toBeTruthy();
    expect(component.defaultQuickDepositData).toBeTruthy;
  });

  describe('checkMaxStakeError', () => {
    let data: any;

    beforeEach(() => {
      data = [
        {
          error: 'STAKE_TOO_HIGH',
          errorMsg: 'some message',
          Bet: {
            error: 'STAKE_TOO_HIGH',
          },
          stake: {
            stakePerLine: 3,
            freeBetAmount: 0,
            max: 50
          },
        }
      ];
    });

    it('should not clear error from bet when stakePerLine < maxBet && (stakePerLine + freeBet) < maxBet', () => {
      data[0].stake.stakePerLine = 1;
      data[0].stake.freeBetAmount = 5;
      data[0].stake.max = 3;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(typeof component['betData'][0].error).toEqual('string');
      expect(typeof component['betData'][0].errorMsg).toEqual('string');
    });

    it('should remove error from betData item', () => {
      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
      expect(component['betData'][0].errorMsg).toBeNull();
    });

    it('should remove error from Bet', () => {
      data[0].error = null;
      data[0].errorMsg = null;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
      expect(component['betData'][0].errorMsg).toBeNull();
    });

    it('should not clear error from bet if freeBet is higher than max stake', () => {
      data[0].stake.freeBetAmount = 51;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(typeof component['betData'][0].error).toEqual('string');
    });

    it('should clear error from bet when freeBet is lower than max stake', () => {
      data[0].stake.freeBetAmount = 49;
      data[0].stake.stakePerLine = 0;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
    });

    it('should clear error from bet when freeBet is falsy and stake correct', () => {
      data[0].stake.freeBetAmount = '';

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
    });

    it('should clear error from bet when stakePerLine is falsy', () => {
      data[0].stake.stakePerLine = '';
      data[0].stake.freeBetAmount = 49;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
    });

    it('should clear error from bet when error is not STAKE_TOO_HIGH', () => {
      data[0].error = 'STAKE';
      data[0].Bet.error = 'STAKE';
      data[0].stake.freeBetAmount = 49;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(typeof component['betData'][0].error).toEqual('string');
    });

    it('should not clear error from bet when stekPerLine is higher than max bet', () => {
      data[0].stake.stakePerLine = 51;
      data[0].stake.freeBetAmount = 49;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(typeof component['betData'][0].error).toEqual('string');
    });

    it('should clear error when stakePerLine is equal max stake', () => {
      data[0].stake.stakePerLine = 50;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
    });

    it('should clear error when freeBet is equal max stake', () => {
      data[0].stake.freeBetAmount = 50;
      data[0].stake.stakePerLine = 0;

      component['betData'] =  data;
      component['checkMaxStakeError']();

      expect(component['betData'][0].error).toBeNull();
    });
  });

  describe('setQuickDepositInitialData', () => {
    it('should set data from deposit service', () => {
      component['quickDepositService'].quickDepositCache = {a: 2} as any;
      component['setQuickDepositInitialData']();

      expect((component.quickDeposit as any).a).toEqual(2);
    });

    it('should set default data', () => {
      component['quickDepositService'].quickDepositCache = null as any;
      component['setQuickDepositInitialData']();
      expect(component.quickDeposit).toEqual(component.defaultQuickDepositData);
    });
  });

  describe('setFreeBet', () => {
    it('should calculate correct stake for 4 fold acca and 5x multiplier', () => {
      const stakeMultiplier = 5;
      const freeBetToken = 5.6;
      const bet = {
        selectedFreeBet : { value: freeBetToken },
        stakeMultiplier : stakeMultiplier,
        stake: {},
        Bet: { isBetEachWay: true }
      } as any;
      component.ngOnInit();
      component.placeSuspendedErr = {} as any;

      component.setFreebet(bet);

      expect(typeof bet.stake.freeBetAmount).toEqual('number');
      const stakeResult = Math.floor(Number(bet.stake.freeBetAmount) * stakeMultiplier * 100) / 100;
      expect(stakeResult).toEqual(freeBetToken);
    });
  });

  describe('winOrEachWay', () => {
    it('should handle win or e/w bet', () => {
      component.winOrEachWay({
        Bet: {}
      } as any);
      expect(betslipService.winOrEachWay).toHaveBeenCalledTimes(1);
    });

    it('should set freebet amount (e/w = true)', () => {
      betslipService.isFreeBetValid.and.returnValue(true);
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: false }
      };
      component.winOrEachWay(bet);
      expect(bet.stake.freeBetAmount).toBe(5);
    });

    it('should set freebet ammount (e/w = false)', () => {
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: true }
      };
      component.winOrEachWay(bet);
      expect(bet.stake.freeBetAmount).toBe(10);
    });

    it('return true if sport is horseracing', () => {
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: true },
        sportId : '21',
        sport: 'HORSE_RACING',
        disabled: false
      };
      component.winOrEachWay(bet);
      expect(component).toBeTruthy();
    });

    it('should check if max stake exceeded', () => {
      component.isBoostActive = true;
      component.winOrEachWay({
        Bet: {
          isEachWay: true
        }
      } as any);
      expect(commandService.execute).toHaveBeenCalledTimes(1);
    });
    it('if freebet is not valid', () => {
      betslipService.isFreeBetValid.and.returnValue(false);
      component['showUnvalidFreeBetPopup'] = jasmine.createSpy();
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: false }
      };
      const clickEvent = {
        preventDefault: jasmine.createSpy()
      } as any;
      component.winOrEachWay(bet, clickEvent);
      expect(clickEvent.preventDefault).toHaveBeenCalled();
      expect(component['showUnvalidFreeBetPopup']).toHaveBeenCalled();
      expect(bet.Bet.isEachWay).toEqual(false);
    });
  });

  it('#showUnvalidFreeBetPopup', () => {
    infoDialogService.openInfoDialog.and.callFake((a, b, c, d, e, buttons: any[]) => {
      buttons.forEach(btn => {
        btn.handler && btn.handler();
      });
    });
    component['showUnvalidFreeBetPopup']();
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    expect(infoDialogService.closePopUp).toHaveBeenCalled();
  });

  it('@reloadComponent()', () => {
    component['isAlreadyReloaded'] = false;
    component['init'] = jasmine.createSpy();
    component.reloadComponent();
    expect(component['init']).toHaveBeenCalled();
  });

  it('@reloadComponent() - should not reinit betslip when it was already reloaded before', () => {
    component['isAlreadyReloaded'] = true;
    component['init'] = jasmine.createSpy();
    component.reloadComponent();
    expect(component['init']).not.toHaveBeenCalled();
  });

  describe('totalStake', () => {

    beforeEach(() => {
      spyOn(component, 'areToteBetsInBetslip').and.returnValue(false);
    });

    it('should extract stakes', () => {
      component.totalStake();

      expect(betslipStakeService.getStake).toHaveBeenCalledTimes(2);
    });

    it('should extend quickDeposit with data from service', () => {
      component.totalStake();

      expect(quickDepositService.checkQuickDeposit).toHaveBeenCalled();
    });

    /* disabled until BMA-46323, don't remove.
    it('should pass placeBetsPending as true', () => {
      component.placeBetsPending = true;
      component.totalStake();

      const args = quickDepositService.checkQuickDeposit.calls.argsFor(0);
      expect(args[4]).toBe(true);
    });

    it('should pass placeBetsPending as false - phase 2', () => {
      component.placeBetsPending = true;
      component.overask.userHasChoice = true;
      component.totalStake();

      const args = quickDepositService.checkQuickDeposit.calls.argsFor(0);
      expect(args[4]).toBe(false);
    });

    it('should pass placeBetsPending as false', () => {
      component.placeBetsPending = false;
      component.totalStake();

      const args = quickDepositService.checkQuickDeposit.calls.argsFor(0);
      expect(args[4]).toBe(false);
    });
    */
  });

  describe('isPriceUpdate', () => {
    beforeEach(() => {
      component.betSlipSingles = [{ disabled: false }];
    });

    it('should check if some of selections has price changed', () => {
      spyOn(component, 'getPriceChangeMessage').and.returnValue(true as any);
      const actualResult = component['isPriceUpdate']();

      expect(actualResult).toBeTruthy();
    });

    it('should check if some of selections has price changed(price was not changed)', () => {
      spyOn(component, 'getPriceChangeMessage').and.returnValue(false as any);
      const actualResult = component['isPriceUpdate']();

      expect(actualResult).toBeFalsy();
    });

    it('should check if some of selections has price changed(some of bets is suspended)', () => {
      component.betSlipSingles[0].disabled = true;
      spyOn(component, 'getPriceChangeMessage').and.returnValue(true as any);
      const actualResult = component['isPriceUpdate']();

      expect(actualResult).toBeFalsy();
    });

    it('should check if some of selections has price changed(some of bets is suspended)', () => {
      component.betSlipSingles = undefined;
      spyOn(component, 'getPriceChangeMessage');
      const actualResult = component['isPriceUpdate']();

      expect(actualResult).toBeUndefined();
    });
  });

  it('#isIFrameLoadingInProgress should return false when iframe is shown and panel is expanded', () => {
    component.showIFrame = true;
    component.quickDepositIFrameFormExpanded = true;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  it('#isIFrameLoadingInProgress should return false when iframe is shown and panel is collapsed', () => {
    component.showIFrame = true;
    component.quickDepositIFrameFormExpanded = false;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  it('#isIFrameLoadingInProgress should return true when iframe is not shown and panel is expanded', () => {
    component.showIFrame = false;
    component.quickDepositIFrameFormExpanded = true;
    expect(component['isIFrameLoadingInProgress']()).toBeTruthy();
  });

  it('#isIFrameLoadingInProgress should return false when iframe is not shown and panel is collapsed', () => {
    component.showIFrame = false;
    component.quickDepositIFrameFormExpanded = false;
    expect(component['isIFrameLoadingInProgress']()).toBeFalsy();
  });

  it('should hide iframe and close window with addSelection', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    storageService.get.and.returnValue([{addSelection:{}}]);
    component.onCloseQuickDepositWindow();
    expect(component.showIFrame).toBeFalsy();
    expect(component.quickDepositIFrameFormExpanded).toBeFalsy();
    expect(component.iframeLoadingInProgress).toBeFalsy();
    expect(component['isIFrameLoadingInProgress']).toHaveBeenCalled();
  });

  it('should hide iframe and close window with empty array', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    storageService.get.and.returnValue([]);
    component.onCloseQuickDepositWindow();
    expect(component.showIFrame).toBeFalsy();
    expect(component.quickDepositIFrameFormExpanded).toBeFalsy();
    expect(component.iframeLoadingInProgress).toBeFalsy();
    expect(component['isIFrameLoadingInProgress']).toHaveBeenCalled();
  });

  it('should hide iframe', () => {
    component.templatePlaceBet = jasmine.createSpy();
    component['closeIFrame']();
    expect(component.showIFrame).toBeFalsy();
    expect(component.templatePlaceBet).toHaveBeenCalled();
  });

  it('should show iframe', () => {
    component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(false);
    component.onOpenIframe();
    expect(component.showIFrame).toBeTruthy();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TOGGLE_QUICK_DEPOSIT_IFRAME, true);
    expect(component.iframeLoadingInProgress).toBeFalsy();
    expect(component['isIFrameLoadingInProgress']).toHaveBeenCalled();
  });

  it('isAmountNeeded should return true', () => {
    component.quickDeposit.neededAmountForPlaceBet = '10';
    expect(component.isAmountNeeded()).toBeTruthy();
  });

  it('isAmountNeeded should return flase', () => {
    component.quickDeposit.neededAmountForPlaceBet = '0';
    expect(component.isAmountNeeded()).toBeFalsy();
  });

  it('should return correct error message', () => {
    localeService.getString.and.callFake((token, args) => `test string ${args[0]}`);
    userService.getUserDepositNeededAmount.and.returnValue('7');
    component['quickDeposit'].neededAmountForPlaceBet = '7';
    expect(component.getErrorMsg()).toBe('test string £7');
  });

  it('should not call onCloseQuickDepositWindow when user does have enough money', () => {
    component.isAmountNeeded = jasmine.createSpy().and.returnValue(true);
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.handleBetslipUpdate();
    expect(component.onCloseQuickDepositWindow).not.toHaveBeenCalled();
  });

  it('should not call onCloseQuickDepositWindow when iframe is closed', () => {
    component.isAmountNeeded = jasmine.createSpy().and.returnValue(false);
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.showIFrame = false;
    component.iframeLoadingInProgress = false;
    component.handleBetslipUpdate();
    expect(component.onCloseQuickDepositWindow).not.toHaveBeenCalled();
  });

  it('should call onCloseQuickDepositWindow if iframe is open', () => {
    component.isAmountNeeded = jasmine.createSpy().and.returnValue(false);
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.showIFrame = true;
    component.iframeLoadingInProgress = false;
    component.handleBetslipUpdate();
    expect(component.onCloseQuickDepositWindow).toHaveBeenCalled();
  });

  it('should call onCloseQuickDepositWindow if iframe is loading', () => {
    component.isAmountNeeded = jasmine.createSpy().and.returnValue(false);
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.showIFrame = false;
    component.iframeLoadingInProgress = true;
    component.handleBetslipUpdate();
    expect(component.onCloseQuickDepositWindow).toHaveBeenCalled();
  });

  it('should call onCloseQuickDepositWindow', () => {
    component.isAmountNeeded = jasmine.createSpy().and.returnValue(false);
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.showIFrame = true;
    component.iframeLoadingInProgress = true;
    component.handleBetslipUpdate();
    expect(component.onCloseQuickDepositWindow).toHaveBeenCalled();
  });

  describe('vanilla callCallbackOpenLoginDialog', () => {
    it('isStake = false, callCallbacks should be called with placeBet = false', () => {
      component['callCallbackOpenLoginDialog'](false);
      expect(pubSubService.publish)
        .toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: false, moduleName: 'betslip', action: jasmine.anything() });
    });
    it('isStake = true, callCallbacks should be called with placeBet = "betslip"', () => {
      component['callCallbackOpenLoginDialog'](true);
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: 'betslip', moduleName: 'betslip', action: jasmine.anything() });
    });
  });

  it('#removeFromBetslip should call onCloseQuickDepositWindow', () => {
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.betSlipSingles = [{  Bet : {
      params : {lottoData :{isLotto : false}}
    },}, {}, {}];
    component.removeFromBetslip(0);
    expect(component.onCloseQuickDepositWindow).toHaveBeenCalled();
  });

  it('#removeToteBet should call onCloseQuickDepositWindow', () => {
    component.onCloseQuickDepositWindow = jasmine.createSpy();
    component.removeToteBet(true);
    expect(component.onCloseQuickDepositWindow).toHaveBeenCalled();
  });

  it('#removeToteBet should call totalFreeBetsStake', () => {
    component.totalFreeBetsStake = jasmine.createSpy();
    component.removeToteBet(true);
    expect(component.totalFreeBetsStake).toHaveBeenCalled();
  });

  describe('vanilla @isShowQuickDepositBtnShown', () => {

    it('returns true', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeTruthy();
    });

    it('returns true (quickDepositIFrameFormExpanded is true)', () => {
      component.quickDepositIFrameFormExpanded = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeTruthy();
    });

    it('returns false (showQuickDepositForm is falsy)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.quickDepositFormAllowed = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns false (quickDepositFormAllowed is falsy)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.showQuickDepositForm = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns false (placeBetsPending is true)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;
      component.placeBetsPending = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns false (allowQuickDeposit() is falsy)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;
      component.allowQuickDeposit = jasmine.createSpy().and.returnValue(false);

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns false (total Stake is 0.00)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.00');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns false (overask in progress)', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('1.00');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;
      overAskService.isInProcess = true;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeFalsy();
    });

    it('returns true if non of multiple bets is suspended', () => {
      component.totalStake = jasmine.createSpy().and.returnValue('0.01');
      component.quickDeposit.showQuickDepositForm = true;
      component.quickDeposit.quickDepositFormAllowed = true;
      component.multiplesShouldBeRebuilded = false;

      const result = component.isShowQuickDepositBtnShown();
      expect(result).toBeTruthy();
    });
  });

  describe('@isShowSuspendedNotification', () => {
    it('isShowSuspendedNotification return true when all true',  () => {
      component.placeSuspendedErr = {
        multipleWithDisableSingle: false,
        disableBet: true,
        msg: '',
      };
      overAskService.isNotInProcess = true;
      component.toteBetSuspendedError = true;

      const result = component.isShowSuspendedNotification();
      expect(result).toBeTruthy();
    });

    it('isShowSuspendedNotification return true when first part true',  () => {
      component.placeSuspendedErr = {
        multipleWithDisableSingle: false,
        disableBet: true,
        msg: 'return true',
      };
      overAskService.isNotInProcess = true;
      component.toteBetSuspendedError = null;

      const result = component.isShowSuspendedNotification();
      expect(result).toBeTruthy();
    });

    it('isShowSuspendedNotification return true when second part true', () => {
      component.placeSuspendedErr = {
        multipleWithDisableSingle: false,
        disableBet: true,
        msg: '',
      };
      overAskService.isNotInProcess = false;
      component.toteBetSuspendedError = true;

      const result = component.isShowSuspendedNotification();
      expect(result).toBeTruthy();
    });

    it('isShowSuspendedNotification false true when all false',  () => {
      component.placeSuspendedErr = {
        multipleWithDisableSingle: false,
        disableBet: false,
        msg: '',
      };
      overAskService.isNotInProcess = false;
      component.toteBetSuspendedError = false;

      const result = component.isShowSuspendedNotification();
      expect(result).toBeFalsy();
    });

    it('loadQuickDepositIFrame', () => {
      component['isIFrameLoadingInProgress'] = jasmine.createSpy().and.returnValue(true);
      component.loadQuickDepositIFrame();
      expect(component.quickDepositIFrameFormExpanded).toBeTruthy();
      expect(component.iframeLoadingInProgress).toBeTruthy();
      expect(component['isIFrameLoadingInProgress']).toHaveBeenCalled();
    });

    it('navigates to in-shop upgrade page when user type is in-shop',  () => {
      userService.isInShopUser = jasmine.createSpy().and.returnValue(true);
      component.navigateToUpgrade();

      expect(windowRefService.nativeWindow.location.href).toEqual(accountUpgradeLinkService.inShopToMultiChannelLink);
    });

    it('navigates to online upgrade page when user type is online',  () => {
      userService.isInShopUser = jasmine.createSpy().and.returnValue(false);
      component.navigateToUpgrade();

      expect(windowRefService.nativeWindow.location.href).toEqual(accountUpgradeLinkService.onlineToMultiChannelLink);
    });
  });

  describe('checkAllSingleStakesForBetslipSingles', () => {
    beforeEach(() => {
      component.placeSuspendedErr = { multipleWithDisableSingle: false } as any;
      component.betSlipSingles = [{
        Bet: {
          betOffer: {},
          stake: {
            perLine: ''
          }
        },
        stake: {
          perLine: ''
        }
      }, {
        Bet: {
          betOffer: {},
          stake: {
            perLine: ''
          }
        },
        stake: {
          perLine: ''
        },
        disabled: true
      }, {
        Bet: {
          betOffer: {},
          stake: {
            perLine: '2.00'
          }
        },
        stake: {
          perLine: ''
        }
      }];
    });

    it('should set allStakes stake to all not disabled betslipSingles without amount', () => {
      component['allStakes'] = {
        value: '1.00'
      };

      component['checkAllSingleStakesForBetslipSingles']();
      expect(component.betSlipSingles[0].Bet.stake.perLine).toBe('1.00');
      expect(component.betSlipSingles[1].Bet.stake.perLine).toBe('');
      expect(component.betSlipSingles[2].Bet.stake.perLine).toBe('2.00');
    });

    it('should set empty stake to all not disabled betslipSingles without amount', () => {
      component['allStakes'] = {
        value: '0.000'
      };
      component['checkAllSingleStakesForBetslipSingles']();
      expect(component.betSlipSingles[0].Bet.stake.perLine).toBe('');
      expect(component.betSlipSingles[1].Bet.stake.perLine).toBe('');
      expect(component.betSlipSingles[2].Bet.stake.perLine).toBe('2.00');
    });
  });

  describe('hasClaimedOffersForBIRBets', () => {
    it('should return true', () => {
      const bets = [{
        provider: 'OpenBet',
        claimedOffers: [{status: 'claimed'}]
      }] as any;

      expect(component['hasClaimedOffersForBIRBets'](bets)).toBeTruthy();
    });

    it('should return false', () => {
      const bets = [{
        provider: 'OpenBetBir',
        claimedOffers: [{status: 'claimed'}]
      }] as any;

      expect(component['hasClaimedOffersForBIRBets'](bets)).toBeFalsy();
    });
  });

  describe('ngAfterViewChecked', () => {
    it('should call updateBetSlipHeight from ngAfterViewChecked', () => {
      component.isHeightUpdated = true;
      component['updateBetSlipHeight'] = jasmine.createSpy().and.callThrough();
      component.ngAfterViewChecked();
      expect(component['updateBetSlipHeight']).toHaveBeenCalled();
    });

    it('should not call updateBetSlipHeight from ngAfterViewChecked', () => {
      component.isHeightUpdated = false;
      component['updateBetSlipHeight'] = jasmine.createSpy().and.callThrough();
      component.ngAfterViewChecked();
      expect(component['updateBetSlipHeight']).not.toHaveBeenCalled();
    });
  });
  
  it('setBsNotificationHeight', () => {
    const singleStakesWrapperEl = 20;
    const bsScrollWrapperEl = 100;
    component['singleStakesWrapperEl'] = { clientHeight: singleStakesWrapperEl } as any;
    component['bsScrollWrapperEl'] = { scrollHeight: bsScrollWrapperEl } as any;
    component['setBsNotificationHeight']();
    expect(component.bsMaxHeightLimit).toEqual(bsScrollWrapperEl - singleStakesWrapperEl + clientHeight);
  });

  it('setBsNotificationHeight', () => {
    const singleStakesWrapperEl = 0;
    const bsScrollWrapperEl = 100;
    component['singleStakesWrapperEl'] = null;
    component['bsScrollWrapperEl'] = { scrollHeight: bsScrollWrapperEl } as any;
    component['setBsNotificationHeight']();
    expect(component.bsMaxHeightLimit).toEqual(bsScrollWrapperEl - singleStakesWrapperEl + clientHeight);
  });

  it('setBsNotificationHeight', () => {
    const singleStakesWrapperEl = 0;
    const bsScrollWrapperEl = 100;
    component['singleStakesWrapperEl'] = undefined;
    component['bsScrollWrapperEl'] = { scrollHeight: bsScrollWrapperEl } as any;
    component['setBsNotificationHeight']();
    expect(component.bsMaxHeightLimit).toEqual(bsScrollWrapperEl - singleStakesWrapperEl + clientHeight);
  });

  it('setBsNotificationHeight', () => {
    const singleStakesWrapperEl = 0;
    const bsScrollWrapperEl = 100;
    component['singleStakesWrapperEl'] = { clientHeight: singleStakesWrapperEl } as any;
    component['bsScrollWrapperEl'] = { scrollHeight: bsScrollWrapperEl } as any;
    component['setBsNotificationHeight']();
    expect(component.bsMaxHeightLimit).toEqual(bsScrollWrapperEl - singleStakesWrapperEl + clientHeight);
  });

  it('setBsNotificationHeight for lottos', () => {
    const lottoStakeWrapperEl = 0;
    const bsScrollWrapperEl = 100;
    component['lottoStakeWrapperEl'] = { clientHeight: lottoStakeWrapperEl } as any;
    component['bsScrollWrapperEl'] = { scrollHeight: bsScrollWrapperEl } as any;
    component['setBsNotificationHeight'](component['lottoStakeWrapperEl']);
    expect(component.bsMaxHeightLimit).toEqual(bsScrollWrapperEl - lottoStakeWrapperEl + clientHeight);
  });

  describe('bet slip height scroll bar display - updateBetSlipHeight', () => {
    const bsOffsetHeight = 100;
    const bsNotificationHeight = 99;
    const singleStakesWrapperEl = 20;
    beforeEach(() => {
      component.loadComplete = true;
      component['bsWrapperEl'] = { scrollHeight: bsOffsetHeight } as any;
      component['singleStakesWrapperEl'] = { clientHeight: singleStakesWrapperEl } as any;
      component.betSlipSingles = [{ data: 1 }];
      component.isHeightUpdated = true;
      component.heightChanged.emit = jasmine.createSpy().and.returnValue(0);
      component['setBsNotificationHeight'] = jasmine.createSpy().and.callFake(() => { component.bsMaxHeightLimit = bsNotificationHeight; });
    });
    it('should update isHeightUpdated', () => {
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeFalse();
    });
    it('should not update isHeightUpdated', () => {
      component.loadComplete = false;
      component['bsWrapperEl'] = null;
      component.betSlipSingles = null;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeTrue();
    });
    it('should not update isHeightUpdated - bsWrapperEl - undefined', () => {
      component['bsWrapperEl'] = undefined;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeTrue();
    });
    it('should not update isHeightUpdated - bsWrapperEl height 0', () => {
      component['bsWrapperEl'] = { scrollHeight: 0 } as any;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeTrue();
    });
    it('betSlipSingles with 4 odds selected', () => {
      component.betSlipSingles = [{ data: 1 }, { data: 2 }, { data: 3 }, { data: 4 }];
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeFalse();
      expect(component.heightChanged.emit).toHaveBeenCalledWith(0);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.bsMaxHeightLimit).toEqual(bsNotificationHeight);
    });
    it('betSlipSingles with 5 odds selected', () => {
      component.betSlipSingles = [{ data: 1 }, { data: 2 }, { data: 3 }, { data: 4 }, { data: 5 }];
      component.bsMaxHeightLimit = bsNotificationHeight;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeFalse();
      expect(component.heightChanged.emit).toHaveBeenCalledWith(bsNotificationHeight);
    });
    it('betSlipSingles with 5 odds selected - no bsMaxHeightLimit - page refresh', () => {
      component.betSlipSingles = [{ data: 1 }, { data: 2 }, { data: 3 }, { data: 4 }, { data: 5 }];
      component.bsMaxHeightLimit = 0;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeFalse();
      expect(component.heightChanged.emit).toHaveBeenCalledWith(bsNotificationHeight);
    });
    it('betSlipSingles with 5 odds selected and bsMaxHeightLimit > bsNotificationHeight', () => {
      component.betSlipSingles = [{ data: 1 }, { data: 2 }, { data: 3 }, { data: 4 }, { data: 5 }];
      component.bsMaxHeightLimit = bsNotificationHeight + 1;
      component['updateBetSlipHeight']();
      expect(component.isHeightUpdated).toBeFalse();
      expect(component.heightChanged.emit).toHaveBeenCalledWith(bsNotificationHeight);
    });
    
    it('betSlipSingles with less than 4 odds selected', () => {
      deviceService['isMobile'] = true;
      component.betSlipSingles = [{ data: 1 }, { data: 2 }];
      component['updateBetSlipHeight']({});
      expect(component.bsMaxHeight).toEqual('100%');
    });
    
  });

  it('bsWrapper', () => {
    const elementRef = {
      nativeElement: { test: 1 }
    } as any;
    component.bsWrapper = elementRef;
    expect(component['bsWrapperEl']).toEqual(elementRef.nativeElement);
  });

  it('bsWrapper', () => {
    const elementRef = undefined;
    component.bsWrapper = elementRef;
    expect(component['bsWrapperEl']).toEqual(elementRef);
  });

  it('singleStakesWrapper', () => {
    const elementRef = undefined;
    component.singleStakesWrapper = elementRef;
    expect(component['singleStakesWrapperEl']).toEqual(elementRef);
  });
  
  it('singleStakesWrapper', () => {
    const elementRef = {
      nativeElement: { test: 1 }
    } as any;
    component.singleStakesWrapper = elementRef;
    expect(component['singleStakesWrapperEl']).toEqual(elementRef.nativeElement);
  });

  describe('#freeBetsStoreUpdate', () => {
    it('should call freeBetsStoreUpdate method no bets error res', () => {
     const result = component['freeBetsStoreUpdate']([]);
     expect(freeBetsService.getFreeBetsState).not.toHaveBeenCalled();
    });
    it('should call freeBetsStoreUpdate method with freebet & btes res', () => {
      freeBetsService.getFreeBetsState = jasmine.createSpy().and.returnValue({
          availble: true, 
          data: [{ freebetTokenId: 123 }, { freebetTokenId: 143 }],
          betTokens: [{freebetTokenId: 56}, { freebetTokenId: 78 }],
          fanZone: [{freebetTokenId: 78}, { freebetTokenId: 99 }],

        });
      component['freeBetsStoreUpdate']([{betId:1,freebet:[{id: 123}]}] as any);
      expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    });
    it('should call freeBetsStoreUpdate method with no freebet & btes res', () => {
      freeBetsService.getFreeBetsState = jasmine.createSpy().and.returnValue({
          availble: true, 
          data: [{ freebetTokenId: 123 }, { freebetTokenId: 143 }],
          betTokens: [{freebetTokenId: 56}, { freebetTokenId: 78 }],
          fanZone: [{freebetTokenId: 78}, { freebetTokenId: 99 }],
        });
      component['freeBetsStoreUpdate']([{betId:1}] as any);
      expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    });
    it('should call freeBetsStoreUpdate method with no freebet & btes res', () => {
      freeBetsService.getFreeBetsState = jasmine.createSpy().and.returnValue({
          availble: true, 
          data: [{ freebetTokenId: 123 }, { freebetTokenId: 143 }],
          betTokens: [{freebetTokenId: 56}, { freebetTokenId: 78 }],
          fanZone: [{freebetTokenId: 78}, { freebetTokenId: 99 }],

        });
      component['freeBetsStoreUpdate']([{betId:1,freebet:[]}] as any);
      expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    });

    it('should call freeBetsStoreUpdate method with no freebet & btes res', () => {
      freeBetsService.getFreeBetsState = jasmine.createSpy().and.returnValue({
          availble: true, 
          data: [{ freebetTokenId: 1 },{ freebetTokenId: 12 },{ freebetTokenId: 123 }, { freebetTokenId: 143 }],
          betTokens: [{freebetTokenId: 56}, { freebetTokenId: 78 }],
          fanZone: [{freebetTokenId: 78}, { freebetTokenId: 99 }],

        });
        storageService.get = (key) => {
          if(key === 'toteFreeBets') {
            return [
              {freebetTokenId: 1},
              {freebetTokenId: 12},
              {freebetTokenId: 123},
            ]
          } else {
            return [
              {freebetTokenId: 1},
              {freebetTokenId: 12},
              {freebetTokenId: 123},
            ]
          }
        };
      component['freeBetsStoreUpdate']([{betId:1,freebet:[{id: 1},{id: 12},{id:123}]}] as any,1);
      expect(freeBetsService.getFreeBetsState).toHaveBeenCalled();
    });
  });
  
  describe('#appendDrillDownTagNames with valid data', () => {

    it('should call appendDrillDownTagNames method', () => {
      localeService.getString.and.callFake(a => 'Match Result');
      const betSlipObj = {sportId: '16', marketName: 'Match Result', drilldownTagNames:''};
      const drilldownTagNames = component.appendDrillDownTagNames(betSlipObj);
      expect(drilldownTagNames).toEqual('Match Result,')
    });

    it('should call appendDrillDownTagNames method with valid data and mkt included', () => {
      localeService.getString.and.callFake(a => 'Match Result');
      const betSlipObj = {sportId: '16', marketName: 'Match Result', drilldownTagNames:'MKT_PB,'};
      const drilldownTagNames = component.appendDrillDownTagNames(betSlipObj);
      expect(drilldownTagNames).toEqual('MKT_PB,Match Result,')
    });

    it('should call appendDrillDownTagNames method with valid data and mkt included', () => {
      localeService.getString.and.callFake(a => 'Match Result');
      const betSlipObj = {sportId: '21', marketName: 'Match Result', drilldownTagNames:'MKT_PB'};
      const drilldownTagNames = component.appendDrillDownTagNames(betSlipObj);
      expect(drilldownTagNames).toEqual('');
    });
  });

  
  describe('#updateEachWayAvailable in ngOnInit', () => {
    it('should call updateEachWayAvailable', () => {
      spyOn(component as any, 'updateEachWayAvailable');
      component.ngOnInit();
      expect(component['updateEachWayAvailable']).toHaveBeenCalled();
    });
  });
  describe('#updateEachWayAvailable', () => {
    it('should subscribe when data is published as make isEachWayAvailable updated', () => {
      const betinfo = { id: 1 };
      const payload = {
        ew_avail: 'N',
        ew_fac_num : '1',
        ew_fac_den : '2'
      };
      component.betSlipSingles = [{
        id: 1,
        Bet: {
          isEachWay: true,
          params: {
            eachWayAvailable: 'Y'
          }
        },
        isEachWayAvailable: true,
      }];
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'EACHWAY_FLAG_UPDATED') {
          cb(payload, betinfo);
        }
      };
      spyOn(component,'winOrEachWay');
      component.betSlipMultiples = [{id: 2,isEachWay:true}];
      component['updateEachWayAvailable']();
      expect(component.betSlipSingles[0].Bet.params.eachWayAvailable).toEqual('N');
      expect(component.betSlipSingles[0].isEachWayAvailable).toBeFalse();
      expect(component.betSlipSingles[0].eachWayFactorNum).toBeFalsy();
      expect(component.betSlipSingles[0].eachWayFactorDen).toBeFalsy();
      expect(component.winOrEachWay).toHaveBeenCalledWith({id:2,isEachWay:true});
    });
    it('should subscribe when data is published as make isEachWayAvailable updated if id is not matching', () => {
      const betinfo = { id: 1 };
      const payload = {
        ew_avail: 'N',
        ew_fac_num : '1',
        ew_fac_den : '2'
      };
      component.betSlipSingles = [{
        id: 2,
        Bet: {
          isEachWay: true,
          params: {
            eachWayAvailable: 'Y'
          }
        },
        isEachWayAvailable: true,
      }];
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'EACHWAY_FLAG_UPDATED') {
          cb(payload, betinfo);
        }
      };
      component['updateEachWayAvailable']();
      expect(component.betSlipSingles[0].Bet.params.eachWayAvailable).not.toEqual('N');
      expect(component.betSlipSingles[0].isEachWayAvailable).not.toBeFalse();
    });
    
    it('should subscribe when data is published as make isEachWayAvailable - Y', () => {
      const betinfo = { id: 1 };
      const payload = {
        ew_avail: 'Y',
        ew_fac_num : '1',
        ew_fac_den : '2'
      };
      component.betSlipSingles = [{
        id: 1,
        Bet: {
          isEachWay: true,
          params: {
            eachWayAvailable: 'Y'
          }
        },
        isEachWayAvailable: true,
      }];
      component['pubSubService'].subscribe = (n, m, cb) => {
        if (m === 'EACHWAY_FLAG_UPDATED') {
          cb(payload, betinfo);
        }
      };
      component['updateEachWayAvailable']();
      expect(component.betSlipSingles[0].Bet.params.eachWayAvailable).toEqual('Y');
      expect(component.betSlipSingles[0].isEachWayAvailable).toBeTrue();
    });

  });

  describe('#fetchToteFreeBetsStorage in ngOnInit', () => {
    it('should call fetchToteFreeBetsStorage', () => {
      spyOn(component as any, 'fetchToteFreeBetsStorage');
      component.ngOnInit();
      expect(component['fetchToteFreeBetsStorage']).toHaveBeenCalled();
    });
  });

  describe('Freebet Signposting', () => {
    it('should call getBetInfoPrice with betslipstake', () => {
      const betInfo: any = {
        price: {
          priceNum: '0.5',
          priceDen: '1'
        },
        sportId: '21'
      }
      const betSlipStake = {
        sportId: '21'
      }
      betslipService.getMultiplePotentialPayout.and.returnValue(1.5);
      const returnBetInfo = component.getBetInfoPrice(betSlipStake);
      expect(returnBetInfo).toEqual(betInfo);
    });

    it('should return betInfo when potentialpayout is decimal', () => {
      userService = {
        oddsFormat: 'dec',
      };
      createComponent();
      const betInfo: any = {
        price: {
          priceNum: '0.5',
          priceDen: '1'
        },
        sportId: '21'
      }
      const betSlipStake = {
        sportId: '21'
      }
      betslipService.getMultiplePotentialPayout.and.returnValue(1.5);
      const returnBetInfo = component.getBetInfoPrice(betSlipStake);
      expect(returnBetInfo).toEqual(betInfo);
    });

    it('should call getBetInfoPrice without betslipstake', () => {
      const betInfo: any = {
        price: {
          priceNum: null,
          priceDen: null
        },
        sportId: undefined
      }
      const betSlipStake = null;
      
      const returnBetInfo = component.getBetInfoPrice(betSlipStake);
      expect(returnBetInfo).toEqual(betInfo);
    });

    it('GATracking on eachWay change for single bet with price', () => {
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: true },
        price: {
          priceType: 'LP'
        },
        isSPLP: true,
        localTime: '12:23',
        eventName: 'portman'
      };
      spyOn(component as any, 'setFreeBetGtmData');
      const myPrivateSpy = spyOn<any>(component, 'gaTrackingOnEachWayChange').and.callThrough();
      myPrivateSpy.call(component, bet);
      expect(component['setFreeBetGtmData']).toHaveBeenCalledWith(bet, true);
    })

    it('GATracking on eachWay change for single bet without price', () => {
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: true },
        isSPLP: true,
        localTime: '12:23',
        eventName: 'portman'
      };
      
      spyOn(component as any, 'setFreeBetGtmData');
      component.winOrEachWay(bet);
      expect(component['setFreeBetGtmData']).toHaveBeenCalledWith(bet, true);
    })

    it('gtmService should be called when setFreeBetGtmData is fired', () => {
      const bet: any = {
        stake: {},
        selectedFreeBet: { value: 10 },
        stakeMultiplier: 1,
        Bet: { isEachWay: true },
        price: {
          priceType: 'LP'
        },
        isSPLP: true,
        localTime: '12:23',
        eventName: 'portman'
      };
      const myPrivateSpy = spyOn<any>(component, 'setFreeBetGtmData').and.callThrough();
      myPrivateSpy.call(component, bet, true);
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('#update WinOrEachWay To To Win', () => {
    it('should call To Win in findWinOrEachWay', () => {
      const betslipStake = {
        sportId:'21',
        sport:'HORSE_RACING',
        isFCTC: true,
        marketName:'Outrights',
        Bet:{
          betComplexName:'Win'
        }
      }
      const returndValue = component.findWinOrEachWay(betslipStake);
      expect(returndValue).toEqual('Win');
    });
    it('should call To Win in findWinOrEachWay', () => {
      const betslipStake = {
        sportId:'21',
        sport:'HORSE_RACING',
        isFCTC: false,
        marketName:'Win or Each Way',
        Bet:{
          betComplexName:'Win'
        }
      }
      const returndValue = component.findWinOrEachWay(betslipStake);
      expect(returndValue).toEqual('To Win');
    });
    it('should call WinOrEachWay in findWinOrEachWay', () => {
      const betslipStake = {
        sportId:'19',
        sport:'GRAYHOUNDS',
        isFCTC: true,
        marketName:'OUTRIGHTS',
        Bet:{
          betComplexName:'Win'
        }
      }
      const returndValue = component.findWinOrEachWay(betslipStake);
      expect(returndValue).toEqual('Win');
    });
    it('should call WinOrEachWay in findWinOrEachWay', () => {
      const betslipStake = {
        sportId:'19',
        sport:'GRAYHOUNDS',
        isFCTC: false,
        marketName:'Win or Each Way',
        Bet:{
          betComplexName:'Win'
        }
      }
      const returndValue = component.findWinOrEachWay(betslipStake);
      expect(returndValue).toEqual('Win or Each Way');
    });
  });

  it('should call showEachWayTooltip', () =>{
    const deviceViewType = {
      mobile: false,
      desktop: true,
      tablet: false
    }
    deviceService = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType)
    };
    createComponent();
    spyOn(component, 'showEachWayTooltip').and.callThrough();
    component.ngOnInit();
    component['core']([]);
    expect(component['showEachWayTooltip']).toHaveBeenCalled()
  });
  
  describe('#show tooltip for eachway checkbox', () => {
    it('should call tooltip on onload', () => {
      const betSlipSingles = [{
        sportId : '19',
        sport: 'HORSE_RACING',
        disabled: false,
        isEachWayAvailable: true
      }]
      component['userService'] = { username : 'test1' } as any;
      component.betSlipSingles = betSlipSingles;
      component.showEachWayTooltip();
      component.betSlipSingles.entries();
      expect(storageService.set).toHaveBeenCalledWith('BetSlipTooltipEachWay', Object({ user: 'test1', displayed: true }));
      expect(storageService.get).toHaveBeenCalledWith('BetSlipTooltipEachWay');
      expect(storageService.set).toHaveBeenCalledTimes(1);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000000);
    });
    it('should not call tooltip on onload', () => {
      const betSlipSingles = null;
      component.betSlipSingles = betSlipSingles;
      component.showEachWayTooltip();
      expect(storageService.set).not.toHaveBeenCalled();
    });
  });

  describe('#GA traking for eachway checkbox', () =>{
    
    it('#should call checked when eachWay checkbox is true', ()=>{
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'betslip',
        'component.LabelEvent': "HORSE_RACING",
        'component.ActionEvent': 'checked',
        'component.PositionEvent': 'EachWay.outcomeName',
        'component.LocationEvent': 'betslip',
        'component.EventDetails': 'each way alert',
        'component.URLclicked': 'not applicable',
        'sportID': '21'
      };
     const EachWay = {
      sport: "HORSE_RACING",
      sportId:'21',
      outcomeName: 'EachWay.outcomeName',
      Bet: { isEachWay: true }
      }
      component.eachWayGaTracking = true;
      component.gaTrackingOnEachWayCheckBox(EachWay);
      expect(component.eachWayGaTracking).toBeTruthy();
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
    it('#should call checked when eachWay checkbox is true', ()=>{
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'betslip',
        'component.LabelEvent': "HORSE_RACING",
        'component.ActionEvent': 'unchecked',
        'component.PositionEvent': 'EachWay.outcomeName',
        'component.LocationEvent': 'betslip',
        'component.EventDetails': 'each way regular',
        'component.URLclicked': 'not applicable',
        'sportID': '21'
      };
     const EachWay = {
      sport: "HORSE_RACING",
      sportId:'21',
      outcomeName: 'EachWay.outcomeName',
      Bet: { isEachWay: false }
      }
      component.eachWayGaTracking = false;
      component.gaTrackingOnEachWayCheckBox(EachWay);
      expect(component.eachWayGaTracking).toBeFalsy();
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
  });
    describe('#on load restricted hr messages', () => {
    it('should call send gtm data on click showRestrictedHRInfoTooltip ', () => {
      spyOn(component as any, 'sendGTMData');
      component.isShowHorseRestrictedInfo = false;
      const restrictionMsg = "test";
      const position = "abc";
      component.showRestrictedHRInfoTooltip(restrictionMsg,position);
      expect(component.isShowRacecardRestrictedInfo).toBeFalsy();
      expect(component['sendGTMData']).toHaveBeenCalledWith(restrictionMsg,position);
    });
    it('should not call send gtm data on click showRestrictedHRInfoTooltip', () => {
      spyOn(component as any, 'sendGTMData');
      component.isShowHorseRestrictedInfo = true;
      const restrictionMsg = "test";
      const position = "abc";
      component.showRestrictedHRInfoTooltip(restrictionMsg,position);
      expect(component.isShowRacecardRestrictedInfo).toBeFalsy();
      expect(component['sendGTMData']).not.toHaveBeenCalledWith(restrictionMsg,position);
    });

    it('should call send gtm data on click showRaceCardInfoTooltip ', () => {
      spyOn(component as any, 'sendGTMData');
      component.isShowRacecardRestrictedInfo = false;
      const restrictionMsg = "test";
      const position = "abc";
      component.showRaceCardInfoTooltip(restrictionMsg,position);
      expect(component.isShowHorseRestrictedInfo).toBeFalsy();
      expect(component['sendGTMData']).toHaveBeenCalledWith(restrictionMsg,position);
    });
    it('should not call send gtm data on click showRaceCardInfoTooltip', () => {
      spyOn(component as any, 'sendGTMData');
      component.isShowRacecardRestrictedInfo = true;
      const restrictionMsg = "test";
      const position = "abc";
      component.showRaceCardInfoTooltip(restrictionMsg,position);
      expect(component.isShowHorseRestrictedInfo).toBeFalsy();
      expect(component['sendGTMData']).not.toHaveBeenCalledWith(restrictionMsg,position);
    });

    it('should call on load restricted hr messages', () => {
      spyOn(component as any, 'sendGTMDataOnLoad');
      component.restrictedHorseMsg='test';
      component.isRestrictedHorsesLoaded=false;
      component.validateRestrictedHRs();
      expect(component.isRestrictedHorsesLoaded).toBeTruthy();
      expect(component['sendGTMDataOnLoad']).toHaveBeenCalledWith(component.restrictedHorseMsg,'restricted Horses');
    });

    it('should call on load restricted racecard messages', () => {
      spyOn(component as any, 'sendGTMDataOnLoad');
      component.restrictedRaceCardMsg='test';
      component.isRestrictedRacecardLoaded=false;
      component.validateRestrictedRacecards();
      expect(component.isRestrictedRacecardLoaded).toBeTruthy();
      expect(component['sendGTMDataOnLoad']).toHaveBeenCalledWith(component.restrictedRaceCardMsg,'restricted Racecards');
    });
  });
  describe('#GA tracking on click on tooltip to load restricted hr messages', () => {
    it('should call GA tracking on click on tooltip for restricted hr messages', () => {
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'betslip',
        'component.LabelEvent': 'restriction messages',
        'component.ActionEvent': 'click',
        'component.PositionEvent': 'abc',
        'component.LocationEvent': 'test',
        'component.EventDetails': 'info icon',
        'component.URLClicked': 'not applicable'
      }
      component.sendGTMData("test","abc");
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData)
    });
    it('should call GA tracking on load for restricted hr messages', () => {
      const gtmData = {
        event: 'contentView',
      'component.CategoryEvent': 'betslip',
      'component.LabelEvent': 'restriction messages',
      'component.ActionEvent': 'load',
      'component.PositionEvent': 'positionEvent',
      'component.LocationEvent': 'betslip',
      'component.EventDetails': 'message',
      'component.URLClicked': 'not applicable'
      }
      const myPrivateSpy = spyOn<any>(component, 'sendGTMDataOnLoad').and.callThrough();
      myPrivateSpy.call(component, 'message','positionEvent');
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData)
    });
  });

  describe('#checkHRRestrictionsIfAny', () => {
    it('should checkHRRestrictionsIfAny with array og args', () => {
      getSelectionDataService['restrictedRacecardAndSelections'] = jasmine.createSpy('restrictedRacecardAndSelections').and.returnValue({});
      spyOn(component as any, 'initRestrictedSelections');
      const res = [1,2,3, {categoryId: '21'}, {categoryId: '32'}];
      component['checkHRRestrictionsIfAny'](res);
      const res1 = [1,2,3, {categoryId: '32'}]
      component['checkHRRestrictionsIfAny'](res1);
      expect(component['initRestrictedSelections']).toHaveBeenCalled();
    })
  });
  describe('formatBetslipStakes' , () => {
    it('more than 2 decimal', () => {
      component.formatBetslipStakes(['10.223']);
      expect(component.quickStakeItems.length).toBe(1)
    })
    it('less than 2 decimal', () => {
      component.formatBetslipStakes(['10'])
      expect(component.quickStakeItems.length).toBe(1)
    })
  })

  describe('getAllSingleStakeOutcomeIds', () => {
    it('getAllSingleStakeOutcomeIds', () => {
      component.betSlipSingles = [{outcomeId: '1'}, {outcomeId: '2'}]
      component.getAllSingleStakeOutcomeIds();
    })
    it('getAllSingleStakeOutcomeIds with undefined', () => {
      component.getAllSingleStakeOutcomeIds();
    })
  });
  describe('toteBetCanBePlaced', () => {
    it('isToteBetWithProperStake false and toteFreeBetSelected false', () => {
      component.toteFreeBetSelected = false;
      toteBetslipService.isToteBetWithProperStake = jasmine.createSpy('isToteBetWithProperStake').and.returnValue(false);
      expect(component['toteBetCanBePlaced']()).toBeFalse();
    });
    it('isToteBetWithProperStake false and toteFreeBetSelected true', () => {
      component.toteFreeBetSelected = true;
      toteBetslipService.isToteBetWithProperStake = jasmine.createSpy('isToteBetWithProperStake').and.returnValue(false);
      expect(component['toteBetCanBePlaced']()).toBeTrue();

    });
  });

  it('should call deleteFromToteBetStorage', ()=> {
    storageService.get.and.returnValue({poolBet: {freebetTokenId: 12, freebetTokenValue: 12}});
    spyOn(component, 'deleteFromToteBetStorage');
    component.deleteFromToteBetStorage();
    expect(component.deleteFromToteBetStorage).toHaveBeenCalled();
  })

  it('should call showLuckySignPostBanner return false', ()=> {
    betReceiptService.isBonusApplicable.and.returnValue(false);
    const outcomeDetail = {
      outcomeDetails: [{
        categoryId : '21',
        marketId: 12345,
        name : 'ieuehokeo',
        eventDesc : 'wertyuio',
        accMax : 1,
        accMin: 1
      }],
      bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]
    }
    component.showLuckySignPostBanner(outcomeDetail);
    expect(component.isLuckyAvailable).toEqual(false);
  })

  it('should call showLuckySignPostBanner return true', ()=> {
    betReceiptService.isBonusApplicable.and.returnValue(true);
    const outcomeDetail = {
      outcomeDetails: [{
        categoryId : '21',
        marketId: 12345,
        name : 'ieuehokeo',
        eventDesc : 'wertyuio',
        accMax : 1,
        accMin: 1
      },
      {
        categoryId : '21',
        marketId: 34567,
        name : 'ieuehokeo',
        eventDesc : 'wertyuio',
        accMax : 1,
        accMin: 1
      },
      {
        categoryId : '21',
        marketId: 67584,
        name : 'ieuehokeo',
        eventDesc : 'wertyuio',
        accMax : 1,
        accMin: 1
      },
      {
        categoryId : '21',
        marketId: 98574,
        name : 'ieuehokeo',
        eventDesc : 'wertyuio',
        accMax : 1,
        accMin: 1
      }],
      bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]
    }
    component.showLuckySignPostBanner(outcomeDetail);
    expect(component.isLuckyAvailable).toEqual(true);
  })
  
  describe('#GA tracking on click', () => {
    it('sendGTMData', () => {
      component['sendGtmDataoninfoicon']('lucky15');
      expect(gtmService.push).toHaveBeenCalled();
    }); 
  });

  describe('#showLuckySignPostInfoLable', () => {
    it('should return true for info label', () => {
      expect(component['showLuckySignPostInfoLable']('L15')).toBeTruthy();
    });
    it('should return true for info label', () => {
      expect(component['showLuckySignPostInfoLable']('L31')).toBeTruthy();
    });
    it('should return true for info label', () => {
      expect(component['showLuckySignPostInfoLable']('L63')).toBeTruthy();
    });
  });

  describe('calculateAllWinnerBonus()', () => {
    it('should call calculateAllWinnerBonus()', () => {
      component.betResponseData = {bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]}
      component.showLuckySignPost = true;
      const response = component['calculateAllWinnerBonus']();
      expect(response).toEqual('£0.00');
    }); 
  });

  describe('isShownAllWinner()', () => {
    it('should call isShownAllWinner()', () => {
      component.betResponseData = {bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]}
      expect(component.isShownAllWinner()).toBeFalsy();
    });

    it('should call isShownAllWinner()', () => {
      component.betResponseData = {bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betType: 'L15',
        availableBonuses :{
          availableBonus:[{
            multiplier:'2'
          }]
        }
      }]}
      expect(component.isShownAllWinner()).toBeFalsy();
    });

    it('should call isShownAllWinner()', () => {
      component.estReturn = 0;
      component.betResponseData = {bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]}
      betReceiptService.isAllWinnerOnlyApplicable = jasmine.createSpy('isAllWinnerOnlyApplicable').and.returnValue(true);
      const response = component.isShownAllWinner();
      expect(response).toEqual(1);
    });

    it('should call isShownAllWinner()', () => {
      betReceiptService.returnAllWinner.and.returnValue('£23.5');
      component.estReturn = 2;
      component.betResponseData = {bets: [{
        leg: [{'part':[{eventId: "11"}]}],
        betTypeRef: {id: 'L15'},
        availableBonuses :{
          availableBonus:{
            multiplier:'2'
          }
        }
      }]}
      betReceiptService.isAllWinnerOnlyApplicable = jasmine.createSpy('isAllWinnerOnlyApplicable').and.returnValue(true);
      spyOn(component, 'calculateAllWinnerBonus').and.returnValue('£23.5');
      const response = component.isShownAllWinner();
      expect(response).toEqual('£23.5');
    });
  });

  describe('checkSP()', () => {
    it('should call checkSP()', () => {
      const betData = {outcomes: [{
          price:{priceType: 'SP'}
        }],
        type: 'L15'
      }
      const response = component.checkSP(betData);
      expect(response).toBeTruthy();
    });

    it('should call checkSP()', () => {
      const betData = {outcomes: [{
          price:{priceType: 'LP'}
        }],
        type: 'L31'
      }
      const response = component.checkSP(betData);
      expect(response).toBeFalsy();
    });
  });  
});
