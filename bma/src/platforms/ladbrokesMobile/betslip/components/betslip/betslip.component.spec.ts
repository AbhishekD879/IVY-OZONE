import {of as observableOf, Subject, Subscription } from 'rxjs';
import { discardPeriodicTasks, fakeAsync, flush, tick } from '@angular/core/testing';
import { LadbrokesBetslipComponent } from '@ladbrokesMobile/betslip/components/betslip/betslip.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BetslipComponent } from '@betslip/components/betslip/betslip.component';
import { IBetslipDepositData } from '@betslip/models/betslip-deposit.models';

describe('LadbrokesBetslipComponent', () => {

  let component: LadbrokesBetslipComponent,
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
    componentFactoryResolver,
    accountUpgradeLinkService,
    germanSupportService,
    quickDepositIframeService,
    changeDetectorRef,
    serviceClosureService,
    siteServerRequestHelperService,
    sessionStorageService,
    coreToolsService,
    signpostingCmsService,
    getSelectionDataService

  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: false
  }
  beforeEach(fakeAsync(() => {
    userService = {
      currencySymbol: '£',
      status: true,
      sportBalance: null,
      getRetailCard: jasmine.createSpy('getRetailCard'),
      username: 'test',
      oddsFormat: 'frac',
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
      getUserDepositMessage: jasmine.createSpy('getUserDepositMessage').and.returnValue('foo'),
      getUserDepositNeededAmount: jasmine.createSpy('getUserDepositNeededAmount').and.returnValue('10.00')
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
      rejectOffer: jasmine.createSpy('rejectOffer').and.returnValue(observableOf({}))
    };
    cmsService = {
      getQuickStakes : jasmine.createSpy('getQuickStakes').and.returnValue({subscribe: () => true}),
      getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(observableOf({})),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        Overask: {
          title: 'title',
          topMessage: 'top message',
          bottomMessage: 'bottom message',
        },
        maxPayOut: {
          maxPayoutFlag: true,
          maxPayoutMsg: 'your return is one million'
        }
      })),
    };
    windowRefService = {
      nativeWindow: {
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
          style: {}
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
      getPriceUpdate: jasmine.createSpy('getPriceUpdate').and.returnValue(observableOf({}))
    };
    betslipService = {
      getMultiplePotentialPayout: jasmine.createSpy(),
      isSuspended: jasmine.createSpy().and.returnValue(false),
      removeByOutcomeId: jasmine.createSpy(),
      isSinglesHasOldPrice: jasmine.createSpy().and.returnValue(true),
      buildPotentialPayoutObj: jasmine.createSpy(),
      setPriceType: jasmine.createSpy(),
      removeFzSelectionsOnLogout: jasmine.createSpy(),
      getOverlayLiveUpdateMessage: jasmine.createSpy('getOverlayLiveUpdateMessage').and.returnValue('message'),
      parsePlaceBetsResponse: jasmine.createSpy('parsePlaceBetsResponse').and.returnValue({
        bets: [{
          freeBet: {}
        }]
      }),
      winOrEachWay: jasmine.createSpy('winOrEachWay'),
      fetch: jasmine.createSpy('fetch').and.returnValue(observableOf([])),
      showSuspendedOutcomeErr: jasmine.createSpy('showSuspendedOutcomeErr').and.returnValue({
        multipleWithDisableSingle: false,
        disableBet: false,
        msg: 'Please beware that %1 of your selections has been suspended'
      }),
      placeBets: jasmine.createSpy('placeBets').and.returnValue(observableOf({})),
      findSuspendedBetsId: jasmine.createSpy('findSuspendedBetsId'),
      getPlaceBetPending: jasmine.createSpy('getPlaceBetPending').and.returnValue(true),
      getConfig: jasmine.createSpy('getConfig').and.returnValue(observableOf({})),
      setConfig: jasmine.createSpy(),
      isMultipleFreeBetSelected: jasmine.createSpy('isMultipleFreeBetSelected'),
      setAmount: jasmine.createSpy('setAmount'),
      countSuspendedOutcomes: jasmine.createSpy('countSuspendedOutcomes').and.returnValue(0),
      setPlaceBetPending: jasmine.createSpy('setPlaceBetPending').and.callFake(value => value),
      areBetsWithStakes: jasmine.createSpy(),
      betSlipReady: new Subject(),
      count: jasmine.createSpy('count'),
      updateLegsWithPriceChange: jasmine.createSpy('updateLegsWithPriceChange'),
      exucuteOverask: jasmine.createSpy('exucuteOverask').and.returnValue(observableOf({})),
      getBetslipBetByResponseBet: jasmine.createSpy('getBetslipBetByResponseBet'),
      getSuspendedMessage: jasmine.createSpy('getSuspendedMessage'),
      updateAvailableFreeBets: jasmine.createSpy('updateAvailableFreeBets'),
      findBetForFreeBetTooltip: jasmine.createSpy('findBetForFreeBetTooltip')
    };
    toteBetReceiptService = {};
    quickDepositIframeService = {};
    resolveService = {
      reset: jasmine.createSpy('reset')
    };

    betReceiptService = {
      message: {
        type: undefined,
        msg: undefined
      }
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
      get: jasmine.createSpy('get'),
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
      getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(observableOf(null)),
      getFreeBetsState: jasmine.createSpy('getFreeBetsState').and.returnValue({})
    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve()),
      whenSession: jasmine.createSpy('whenSession').and.returnValue(Promise.resolve())
    };
    fracToDecService = {
      decToFrac: jasmine.createSpy(),
      getDecimal: jasmine.createSpy().and.returnValue(5)
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, cb) => {
        if (p2 === 'BS_SELECTION_LIVE_UPDATE') {
          cb({
            info: () => ({}),
            history: {
              isPriceChanged: () => false,
              isPriceChangedAndMarketUnsuspended: () => false
            }
          });
        } else {
          cb(true);
        }
      }),
      publishSync: jasmine.createSpy('publishSync'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
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
        ODDS_BOOST_MAX_STAKE_EXCEEDED: 'ODDS_BOOST_MAX_STAKE_EXCEEDED'
      },
      execute: jasmine.createSpy('execute').and.returnValue({}),
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      register: jasmine.createSpy('register')
    };
    toteBetslipService = {
      reload: jasmine.createSpy('reload'),
      clear: jasmine.createSpy('clear'),
      removeToteBet: jasmine.createSpy('removeToteBet'),
      placeBet: jasmine.createSpy('placeBet').and.returnValue(Promise.resolve({})),
      getTotalStake: jasmine.createSpy('getTotalStake'),
      isToteBetPresent: jasmine.createSpy('isToteBetPresent').and.returnValue(true),
      isToteBetWithProperStake: jasmine.createSpy('isToteBetWithProperStake').and.returnValue(true),
      setFreeBetsConfig: (config) => { return config;}
    };
    bsFiltersService = {
      todayTomorrowDate: jasmine.createSpy('todayTomorrowDate'),
      multiplesSort: jasmine.createSpy('multiplesSort').and.returnValue([])
    };
    betslipStorageService = {
      restoreUserStakeData: jasmine.createSpy('restoreUserStakeData'),
      setFreeBet: jasmine.createSpy('setFreeBet'),
      clean: jasmine.createSpy('clean'),
      restore: jasmine.createSpy('restore').and.returnValue([])
    };
    betslipDataService = {
      containsRegularBets: jasmine.createSpy('containsRegularBets').and.returnValue(false)
    };
    betslipStakeService = {
      getStake: jasmine.createSpy('getStake'),
      getFreeBetStake: jasmine.createSpy('getFreeBetStake'),
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
      getEventTime: jasmine.createSpy()
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
      inShopToMultiChannelLink: jasmine.createSpy('inShopToMultiChannelLink'),
      onlineToMultiChannelLink: jasmine.createSpy('onlineToMultiChannelLink')
    };
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser').and.returnValue(true)
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };

    signpostingCmsService = {
      getFreebetSignposting : jasmine.createSpy('getFreebetSignposting').and.returnValue(observableOf({}))
    };

    getSelectionDataService = {
      getOutcomeData: jasmine.createSpy().and.returnValue(observableOf(null)),
    };

    createComponent();
    component.isGermanUser = false;
    component.overlayMsgConfig = {};
    component.quickDeposit = {} as IBetslipDepositData;
    tick();
  }));

  function createComponent() {
    component = new LadbrokesBetslipComponent(
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
      germanSupportService,
      changeDetectorRef,
      serviceClosureService,
      siteServerRequestHelperService,
      sessionStorageService,
      coreToolsService,
      signpostingCmsService,
      getSelectionDataService
    );
  }


  describe('#ngOnInit', () => {
    beforeEach(() => {
      component['core'] = jasmine.createSpy('core');
    });

    it('should set quickDepositService.config.userHasCreditCard as false', () => {
      spyOn(component as any, 'formatBetslipStakes');
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe');
      germanSupportService.isGermanUser.and.returnValue(true);

      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BetSlip', [pubSubService.API.SESSION_LOGIN, pubSubService.API.SESSION_LOGOUT],
        jasmine.any(Function));
      expect(component.isGermanUser).toBeTruthy();
    });

    it('removeFzSelectionsOnLogout on session login', () => {
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe');
      betslipService.removeFzSelectionsOnLogout = jasmine.createSpy('removeFzSelectionsOnLogout');

      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('BetSlip', [pubSubService.API.SESSION_LOGIN, pubSubService.API.SUCCESSFUL_LOGIN],
        jasmine.any(Function));
      expect(betslipService.removeFzSelectionsOnLogout).toHaveBeenCalled();
    });

    it('should subscribe to BetSlip BS_SHOW_OVERLAY channel', () => {
      component['pubSubService'].subscribe = jasmine.createSpy('subscribe');

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith('BetSlip', pubSubService.API.BS_SHOW_OVERLAY, jasmine.any(Function));
    });

    
  });

  it('#ngOnDestroy', () => {
    component['sub'] = new Subscription();
    component['sub'].unsubscribe = jasmine.createSpy();
    component['resetForecastReoderState'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('BetSlip');
  });

  it('@showOverlayMessage', () => {
    const messageConfig = { message: 'message', type: '' };
    component['showOverlayMessage'](messageConfig);

    expect(component.overlayMsgConfig).toEqual(messageConfig);
  });

  describe('selectionLiveUpdate', () => {
    let bet;

    beforeEach(() => {
      bet = {
        info: () => ({}),
        history: {
          isPriceChanged: () => false,
          isPriceChangedAndMarketUnsuspended: () => false
        }
      };
    });

    it('should show overlay message', () => {
      betslipService.getOverlayLiveUpdateMessage.and.returnValue('msg');
      component['selectionLiveUpdate'](bet);
      expect(component.overlayMsgConfig).toEqual({ message: 'msg', type: '' });
    });

    it('should not show overlay message', () => {
      betslipService.getOverlayLiveUpdateMessage.and.returnValue('');
      component['selectionLiveUpdate'](bet);
      expect(component.overlayMsgConfig).toEqual({});
    });

    it('should not show overlay if overask is in Process', () => {
      component['overAskService'].isInProcess = true;
      component['selectionLiveUpdate'](bet);
      expect(component.overlayMsgConfig).toEqual({});
    });
  });

  it('@handleDefaultError', () => {
    const messageConfig = { message: 'message', type: '' };
    component.placeStakeErr = 'message';

    // @ts-ignore
    spyOn(BetslipComponent.prototype, 'handleDefaultError');

    component['handleDefaultError']({} as any);

    expect(component.overlayMsgConfig).toEqual(messageConfig);
  });

  describe('clearOverlayMessage', () => {
    it('should clear message if no type', () => {
      component['clearOverlayMessage']();
      expect(component.overlayMsgConfig).toEqual({ message: '', type: '' });
    });

    it('should clear message if type match', () => {
      component.overlayMsgConfig = { message: 'acca', type: 'ACCA' };
      component['clearOverlayMessage']('ACCA');
      expect(component.overlayMsgConfig).toEqual({ message: '', type: '' });
    });

    it('should not clear message if type mismatch', () => {
      component.overlayMsgConfig = { message: 'price update', type: '' };
      component['clearOverlayMessage']('ACCA');
      expect(component.overlayMsgConfig).toEqual({ message: 'price update', type: '' });
    });
  });

  describe('ngOnDestroy', () => {
    it('should set quick deposit', () => {
      component['sub'] = new Subscription();
      component['sub'].unsubscribe = jasmine.createSpy();
      component.quickDeposit = {
        quickDepositPending: true,
      } as any;

      component.ngOnDestroy();

      expect(component['quickDepositService'].quickDepositCache.quickDepositPending).toBeTruthy();
    });
  });

  afterEach(() => {
    component = null;
  });

  describe('formatBetslipStakes',() => {
    it('formatBetslipStakes',fakeAsync(() => {
      spyOn(component as any, 'formatBetslipStakes')
      cmsService['getQuickStakes'] = jasmine.createSpy('getQuickStakes').and.returnValue(observableOf(['1.0','2','3'])),
      createComponent();
      tick()
      flush();
      discardPeriodicTasks();
    }))
  })
});
