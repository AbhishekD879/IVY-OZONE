import { RacingPostTipComponent } from './racing-post-tip.component';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { of as observableOf } from 'rxjs';
import {
  mostRacingTipDataComp,
  mostTippedHorsesEventsMock,
  mainBetSingleMock,
  betPlacedOnHR,
  receiptEventsMock,
  UnsuspendedRacesMock,
  outcomeUnsuspendedRacesMock,
  priceUpdate
} from '@lazy-modules/racingPostTip/mock/racing-pot-tip-mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('#RacingPostTipComponent', () => {
  let component: RacingPostTipComponent;
  let timeService;
  let commandService;
  let deviceService;
  let raceOutcomeDetails;
  let gtm;
  let locale;
  let pubSubService;
  let routingHelperService;
  let addToBetslipByOutcomeIdService;
  let racingPostTipService;
  let changeDetectorRef;
  let router;
  let windowRef, betSlipService, userService, fracToDecService, gtmService;
  let liveServeHandleUpdatesService;

  const racingGaService = new RacingGaService(gtm, locale, pubSubService);
  racingGaService.sendGTM = jasmine.createSpy('sendGTM');

  const betSlipData = {
    response: {
      respTransGetBetDetail: {
        bet: [{
          'date': '2020-11-23T06:41:44.000Z',
          'username': 'user',
          'eventId': '12345',
        }]
      }
    }
  };
  const RPTip = {
    isTipPresent: true
  };
  const format = 'dec';

  beforeEach(() => {

    liveServeHandleUpdatesService = {
      subscribe: jasmine.createSpy().and.callFake((a, cb: Function) => cb && cb()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    }

    deviceService = {
      isMobile: true
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy(),
      detach: jasmine.createSpy(),
      markForCheck: jasmine.createSpy('markForCheck')
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern'),
      getLocalDateFromString: jasmine.createSpy('getLocalDateFromString')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    raceOutcomeDetails = {
      isGenericSilk: jasmine.createSpy('isGenericSilk'),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
      getSilkStyle: jasmine.createSpy('getSilkStyle')
    };
    gtm = {
      push: jasmine.createSpy()
    };
    locale = {
      getString: jasmine.createSpy('racingposttip.startingPrice').and.returnValue('SP')
    };
    pubSubService = {
      push: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
        if (b === 'RACING_POST_TIP') {
          cb(betSlipData);
        } else if (b === 'QUICKBET_PANEL_CLOSE') {
          cb(true);
        } else if (b === 'IS_TIP_PRESENT') {
          cb(RPTip);
        } else if (b === 'OUTCOME_UPDATED') {
          cb(priceUpdate);
        } else if (b === 'SET_ODDS_FORMAT') {
          cb(format);
        } else {
          cb && cb(betSlipData);
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    userService = {
      oddsFormat: jasmine.createSpy('oddsFormat')
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(racingGaService)),
      API: {
        RACING_GA_SERVICE: 'test',
        BETSLIP_READY: '@betslipModule/betslip.module#BetslipModule:init'
      }
    };
    racingPostTipService = {
      getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
        observableOf( { 'races': mostRacingTipDataComp } as any)
      ),
      getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue(mostTippedHorsesEventsMock[0] as any ),
      getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue(mostTippedHorsesEventsMock[0] as any),
      sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents').and.returnValue(UnsuspendedRacesMock as any)
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy('getDecimal').and.returnValue('1.20'),
      getFracTional: jasmine.createSpy('getFracTional').and.returnValue('1/5')
    };
    addToBetslipByOutcomeIdService = {
      addToBetSlip: jasmine.createSpy('addToBetSlip').and.returnValue(observableOf(true))
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    betSlipService = jasmine.createSpy('betslipService');

    component = new RacingPostTipComponent(timeService, routingHelperService,commandService,
      deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService, racingPostTipService, changeDetectorRef, locale, router,
      windowRef, betSlipService, pubSubService, userService, fracToDecService,
      gtmService,liveServeHandleUpdatesService);
    component.priceOutCome = {
      displayOrder: 1,
      icon: false,
      id: '125825053',
      marketId:'125825053',
      name: 'Sancta Sedes',
      correctPriceType: 'SP',
      racingFormOutcome: { silkName: '123.ong', isBeatenFavourite: false },
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngonInit should start data initialization ', () => {
    beforeEach(() => {
      component.priceOddsBtn = {
        nativeElement: {
          setAttribute: jasmine.createSpy('setAttribute')
        }
      } as any;
    });
    it('#getRacingPostData it should get racing post data & race info', () => {
      component.racingPostData = mostRacingTipDataComp as any;
      component.mainBetReceipts = mainBetSingleMock as any;
      component.multiReceipts = [];
      const RPTipPresent = {
        isTipPresent: false
      };
      pubSubService.subscribe.and.callFake((a, b, cb: Function) => {
        if (b === 'IS_TIP_PRESENT') {
          cb(RPTipPresent);
        } else if (b === 'OUTCOME_UPDATED') {
          cb(priceUpdate);
        } else if (b === 'SET_ODDS_FORMAT') {
          cb(format);
        }
      });
      (commandService.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      component['dimensionData'] = {
        dimension86: 0,
        dimension87: 1,
        dimension88: 12,
        quantity: 1
      } as any;
      component['isBetPlacedOnHR'] = true;
      component.priceOutCome.id = '125825053';
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component['getPrice'] = jasmine.createSpy('getPrice');
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component['checkForSuspendedRaces'] = jasmine.createSpy('checkForSuspendedRaces');
      component['showMainbet'] = jasmine.createSpy('showMainbet');
      component['showQuickbet'] = jasmine.createSpy('showQuickbet');
      component.ngOnInit();
      expect(component['mostRecentTipsData']).not.toBeNull();
      expect(component.cssClass).toEqual('');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('#getRacingPostData it should get racing post data & from main', () => {
      component.mainBetReceipts = [];
      component.priceOutCome.id = '125825053';
      component.priceOutCome.marketId = '125825054';
      pubSubService.subscribe.and.callFake((a, b, cb: Function) => {
        if (b === 'OUTCOME_UPDATED') {
          cb(priceUpdate);
        }
      });
      (commandService.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamActive: false
      }));
      component['dimensionData'] = {
        dimension86: 0,
        dimension87: 0,
        dimension88: null,
        quantity: 1
      } as any;
      component.multiReceipts = [];
      component['isBetPlacedOnHR'] = true;
      component.racingPostData = [];
      component.quickBetReceipt = { categoryId: '16', eventId: 1 } as any;
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component['getPrice'] = jasmine.createSpy('getPrice');
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component['showMainbet'] = jasmine.createSpy('showMainbet');
      component['showQuickbet'] = jasmine.createSpy('showQuickbet');
      component.ngOnInit();
      expect(component.mostTippedHorseEvents.length).toBe(0);
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
    it('#getRacingPostData should not fetch data', () => {
      racingPostTipService = {
        getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
          observableOf({'races': mostRacingTipDataComp} as any)
        ),
        getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue([] as any ),
        getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue([] as any),
        sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents').and
          .returnValue(UnsuspendedRacesMock as any)
      };
      component = new RacingPostTipComponent(timeService, routingHelperService,commandService,
        deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService, racingPostTipService, changeDetectorRef, locale, router,
        windowRef, betSlipService, pubSubService, userService, fracToDecService,
        gtmService,liveServeHandleUpdatesService);
        (commandService.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {}));
        component['dimensionData'] = {
          dimension86: 0,
          dimension87: 0,
          dimension88: null,
          quantity: 1
        } as any;
      component.mainBetReceipts = [];
      component.multiReceipts = receiptEventsMock.multiples;
      component['isBetPlacedOnHR'] = false;
      component.racingPostData = [];
      pubSubService.subscribe = jasmine.createSpy();
      component['showMainbet'] = jasmine.createSpy('showMainbet');
      component['showQuickbet'] = jasmine.createSpy('showQuickbet');
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component.quickBetReceipt = { categoryId: '16', eventId: 1 } as any;
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component.ngOnInit();
      expect(component.mostTippedHorseEvents.length).toBe(0);
    });
    it('#getRacingPostData should not fetch data', () => {
      racingPostTipService = {
        getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
          observableOf({'races': mostRacingTipDataComp} as any)
        ),
        sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents')
          .and.returnValue(UnsuspendedRacesMock as any),
        getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue([] as any ),
        getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue([] as any)
      };
      component = new RacingPostTipComponent(timeService, routingHelperService,commandService,
        deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService, racingPostTipService, changeDetectorRef, locale, router,
        windowRef, betSlipService, pubSubService, userService, fracToDecService,
        gtmService,liveServeHandleUpdatesService);
      component.mainBetReceipts = [];
      component.multiReceipts = receiptEventsMock.multiples;
      component['isBetPlacedOnHR'] = false;
      component.racingPostData = mostRacingTipDataComp as any;
      pubSubService.subscribe = jasmine.createSpy();
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component.quickBetReceipt = { categoryId: '16', eventId: 1 } as any;
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component.ngOnInit();
      expect(component.mostTippedHorseEvents.length).toBe(0);
    });
    it('#getRacingPostData should fetch data', () => {
      racingPostTipService = {
        getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
          observableOf({'races': mostRacingTipDataComp} as any)
        ),
        sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents'),
        getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue(mostTippedHorsesEventsMock),
        getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue(mostTippedHorsesEventsMock)
      };
      component = new RacingPostTipComponent(timeService, routingHelperService,commandService,
        deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService, racingPostTipService, changeDetectorRef, locale, router,
        windowRef, betSlipService, pubSubService, userService, fracToDecService,
        gtmService,liveServeHandleUpdatesService);
      component.mainBetReceipts = mainBetSingleMock as any;
      component.isSuspended = UnsuspendedRacesMock as any;
      component.multiReceipts = [];
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: false
      } as any;
      component['isBetPlacedOnHR'] = true;
      component.racingPostData = mainBetSingleMock as any;
      component.quickBetReceipt = {categoryId: '16', eventId:1} as any;
      component['getTopTipFromTips'] = jasmine.createSpy('getTopTipFromTips');
      component['getSilkAndEdpUrl'] = jasmine.createSpy('getSilkAndEdpUrl');
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component['tipShownGaTrack'] = jasmine.createSpy('tipShownGaTrack');
      component['checkForTipExpired'] = jasmine.createSpy('checkForTipExpired');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      pubSubService.subscribe = jasmine.createSpy();
      component['checkForSuspendedRaces'] = jasmine.createSpy('checkForSuspendedRaces');
      component.ngOnInit();
      expect(component.mostTippedHorseEvents.length).toBe(2);
      expect(component.mostTippedRace).toBeDefined();
      expect(component['getTopTipFromTips']).toHaveBeenCalled();
      expect(component['getSilkAndEdpUrl']).toHaveBeenCalled();
      expect(component['tipShownGaTrack']).toHaveBeenCalled();
      expect(component['checkForTipExpired']).toHaveBeenCalled();
      expect(component['checkForBetsData']).toHaveBeenCalled();
      expect(component['checkForSuspendedRaces']).toHaveBeenCalled();
    });
    it('#getRacingPostData should fetch data after', () => {
      component = new RacingPostTipComponent(timeService, routingHelperService,commandService,
        deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService, racingPostTipService, changeDetectorRef, locale, router,
        windowRef, betSlipService, pubSubService, userService, fracToDecService,
        gtmService,liveServeHandleUpdatesService);
      component.mainBetReceipts = [];
      component.isSuspended = [];
      component.multiReceipts = [];
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: false
      } as any;
      component['isBetPlacedOnHR'] = true;
      component.racingPostData = mainBetSingleMock as any;
      component.quickBetReceipt = {categoryId: '16', eventId:1} as any;
      component['getTopTipFromTips'] = jasmine.createSpy('getTopTipFromTips');
      component['getSilkAndEdpUrl'] = jasmine.createSpy('getSilkAndEdpUrl');
      component['isHorseExists'] = jasmine.createSpy('isHorseExists');
      component['tipShownGaTrack'] = jasmine.createSpy('tipShownGaTrack');
      component['checkForTipExpired'] = jasmine.createSpy('checkForTipExpired');
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      pubSubService.subscribe = jasmine.createSpy();
      component['showMainbet'] = jasmine.createSpy('showMainbet');
      component['showQuickbet'] = jasmine.createSpy('showQuickbet');
      component['checkForPriceUpdate'] = jasmine.createSpy('checkForPriceUpdate');
      component['checkForSuspendedRaces'] = jasmine.createSpy('checkForSuspendedRaces');
      component.ngOnInit();
      expect(component['getTopTipFromTips']).not.toHaveBeenCalled();
      expect(component['getSilkAndEdpUrl']).not.toHaveBeenCalled();
      expect(component['tipShownGaTrack']).not.toHaveBeenCalled();
      expect(component['checkForTipExpired']).not.toHaveBeenCalled();
      expect(component['checkForBetsData']).toHaveBeenCalled();
      expect(component['checkForSuspendedRaces']).toHaveBeenCalled();
      expect(component['showQuickbet']).toHaveBeenCalled();
    });
  });

  describe('checkForSilkLoaded', () => {
    it('when silk loaded', () => {
      component['checkForSilkLoaded']();
      expect(component.isSilkLoaded).toBe(true);
    });
    it('when silk not loaded', () => {
      component.priceOutCome = {
        racingFormOutcome: { isBeatenFavourite: false },
      } as any;
      component['checkForSilkLoaded']();
      expect(component.isSilkLoaded).toBe(false);
    });
    it('when silk not loaded', () => {
      component.priceOutCome = {} as any;
      component['checkForSilkLoaded']();
      expect(component.isSilkLoaded).toBe(false);
    });
    it('when silk not loaded', () => {
      component.priceOutCome = {
        displayOrder: 1,
        icon: false,
        id: '125825053',
        marketId:'125825053',
        name: 'Sancta Sedes',
        correctPriceType: 'SP'
      } as any;
      component['checkForSilkLoaded']();
      expect(component.isSilkLoaded).toBe(false);
    });
  });

  describe('showReceipt', () => {
    it('showTipBetReciept is true when enabled and main bet receipt toggle in on', () => {
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: false
      } as any;
      component['showReceipt']();
      expect(component.showTipBetReciept).toBe(true);
    });
    it('showTipBetReciept is true when enabled and quick bet receipt toggle in on', () => {
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: false,
        quickBetReceipt: true
      } as any;
      component['showReceipt']();
      expect(component.showTipBetReciept).toBe(true);
    });
    it('showTipBetReciept is false when enabled and main bet receipt toggle in off', () => {
      component.racingPostToggle = {
        enabled: false,
        mainBetReceipt: false,
        quickBetReceipt: true
      } as any;
      component['showReceipt']();
      expect(component.showTipBetReciept).toBe(false);
    });
    it('showTipBetReciept is false when enabled and quick bet receipt toggle in off', () => {
      component.racingPostToggle = {
        enabled: false,
        mainBetReceipt: true,
        quickBetReceipt: false
      } as any;
      component['showReceipt']();
      expect(component.showTipBetReciept).toBe(false);
    });

  });
  describe('showMainbet', () => {
    it('should call main bet', () => {
      component['showReceipt'] = jasmine.createSpy('showReceipt');
      racingPostTipService = {
        getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
          observableOf({ 'races': mostRacingTipDataComp } as any)
        ),
      sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents'),
      getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue(mostTippedHorsesEventsMock),
      getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue(mostTippedHorsesEventsMock)
      };
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: false
      } as any;
      component['showMainbet']();
      expect(component.mostTippedHorseEvents.length).toBe(0);
    });
  });
  describe('showQuickbet', () => {
    it('should call main bet', () => {
      component['showReceipt'] = jasmine.createSpy('showReceipt');
      racingPostTipService = {
        getRacingPostByUpcell: jasmine.createSpy('getRacingPostByUpcell').and.returnValue(
          observableOf({ 'races': mostRacingTipDataComp } as any)
        ),
        sendRacingPostSuspendedEvents: jasmine.createSpy('sendRacingPostSuspendedEvents'),
        getMostTipThroughMainBet: jasmine.createSpy('getMostTipThroughMainBet').and.returnValue(mostTippedHorsesEventsMock),
        getMostTipThroughQuickBet: jasmine.createSpy('getMostTipThroughQuickBet').and.returnValue(mostTippedHorsesEventsMock)
      };
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: false,
        quickBetReceipt: true
      } as any;
      component['showQuickbet']();
      expect(component.mostTippedHorseEvents.length).toBe(0);
    });
  });

  describe('#getTopTipFromTips  ', () => {

    it('ngInit should if condion of path', () => {
      deviceService = {
        isMobile: true
      };
      component.liveServeChannels=[ 'sSELCN1256080108', 'sSELCN1256080108', 'sSELCN1256080108'];
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['checkForSilkLoaded'] = jasmine.createSpy('checkForSilkLoaded');
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sSELCN',payload:{'lp_den':'2','lp_num':'3'}});
      });
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sSELCN1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(component['eventCategory']).toEqual('Mobile');
      expect(component['checkForSilkLoaded']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should check for desktop condion for path', () => {
      component.liveServeChannels=[ 'sSELCN1256080108', 'sSELCN1256080108', 'sSELCN1256080108'];
      component = new RacingPostTipComponent(timeService, routingHelperService,
        commandService, deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService,
        racingPostTipService, changeDetectorRef, locale, router, windowRef,
        betSlipService, pubSubService, userService, fracToDecService, gtmService,liveServeHandleUpdatesService);
      deviceService = {
        isMobile: false
      };
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sSELCN',payload:{'lp_den':'2','lp_num':'3'}});
      });
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should check for payload else condion for path', () => {
      component.liveServeChannels=[ 'sSELCN1256080108', 'sSELCN1256080108', 'sSELCN1256080108'];
      component = new RacingPostTipComponent(timeService, routingHelperService,
        commandService, deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService,
        racingPostTipService, changeDetectorRef, locale, router, windowRef,
        betSlipService, pubSubService, userService, fracToDecService, gtmService,liveServeHandleUpdatesService);
      deviceService = {
        isMobile: false
      };
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sSELCN',payload:{'lp_d':'2','lp_n':'3'}});
      });
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should check for empty liveserve data else condion for path', () => {
      component.liveServeChannels=[ 'sSELCN1256080108', 'sSELCN1256080108', 'sSELCN1256080108'];
      component = new RacingPostTipComponent(timeService, routingHelperService,
        commandService, deviceService, raceOutcomeDetails, addToBetslipByOutcomeIdService,
        racingPostTipService, changeDetectorRef, locale, router, windowRef,
        betSlipService, pubSubService, userService, fracToDecService, gtmService,liveServeHandleUpdatesService);
      deviceService = {
        isMobile: false
      };
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb(null)
      });
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#getTopTipFromTipsForWidget ', () => {
    it('should check for else condion for path', () => {
      deviceService = {
        isMobile: true
      };
      component.liveServeChannels=[ 'sEVENT1256080108', 'sEVENT1256080108', 'sEVENT1256080108'];
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};      
      component.filteredHorses = {
        outcomeStatusCode: 'S',
        isResulted: true
      };
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sEVENT',payload:{'lp_den':'2','lp_num':'3',  started: 'Y',  'eventStatusCode': 'A',markets:[{  'marketStatusCode': 'A'}]}});
      });
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(component['eventCategory']).toEqual('Mobile');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should check for else condion without sEVENT for path', () => {
      deviceService = {
        isMobile: true
      };
      component.liveServeChannels=[ 'sEVENT1256080108', 'sEVENT1256080108', 'sEVENT1256080108'];
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};      
      component.filteredHorses = {
        outcomeStatusCode: 'S',
        isResulted: true
      };
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sEMKT',payload:{'lp_den':'2','lp_num':'3',    'eventStatusCode': 'A',markets:[{  'marketStatusCode': 'A'}]}});
      });
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(component['eventCategory']).toEqual('Mobile');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should check for else condion with suspend outcomestatuscode as "A" for path', () => {
      deviceService = {
        isMobile: true
      };
      component.liveServeChannels=[ 'sEVENT1256080108', 'sEVENT1256080108', 'sEVENT1256080108'];
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};      
      component.filteredHorses = null;
      component['liveServeHandleUpdatesService'].subscribe = jasmine.createSpy().and.callFake((a,cb) => {
        cb({type:'sEVENT',payload:{'lp_den':'2','lp_num':'3', started: 'Y', 'eventStatusCode': 'A',markets:[{  'marketStatusCode': 'A'}]}});
      });
      component['mostTippedRace'] = mostTippedHorsesEventsMock[0] as any;
      component['rPhorseName'] = 'Sancta Sedes';
      component['mostTippedRace'].markets[0].outcomes[2].liveServChannels='sEVENT1256080108';
      component['getTopTipFromTips']();
      expect(component['eventCategory']).not.toBeNull();
      expect(component['eventCategory']).toEqual('Mobile');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });


  it('#getPrice should else of get price ', () => {
    component['prices'] = [];
    locale.getString.and.returnValue('SP');
    const result = component['getPrice'](component['prices']);
    expect(result).toEqual('SP');
    expect(locale.getString).toHaveBeenCalledWith('racingposttip.startingPrice');
  });

  it('#getPrice should get decimal price ', () => {
    userService.oddsFormat = 'dec';
    component['prices'] = [{
      'priceNum': '1',
      'priceDen': '5',
      'priceDec': '1.20'
    }] as any;
    component['getPrice'](component['prices']);
    expect(fracToDecService.getDecimal).toHaveBeenCalled();
  });
  it('#getPrice should get fractional price ', () => {
    userService.oddsFormat = 'frac';
    component['prices'] = [{
      'priceNum': '1',
      'priceDen': '5',
      'priceDec': '1/5'
    }] as any;
    component['getPrice'](component['prices']);
    expect(fracToDecService.getFracTional).toHaveBeenCalled();
  });

  it('#goToEvent if could not get sportType', () => {
    const eventEntity = mostTippedHorsesEventsMock[0];
    expect(component['genEventDetailsUrl'](eventEntity as any)).toEqual('url');
  });

  it('#isGenericSilk', () => {
    component['isGenericSilk'](({ name: 'event' } as any), ({ name: 'outcome' } as any));
    expect(raceOutcomeDetails.isGenericSilk).toHaveBeenCalledWith({ name: 'event' }, { name: 'outcome' });
  });

  it('#getSilkStyle', () => {
    component['getSilkStyle'](([{ name: 'event' }] as any), ({ name: 'outcome' } as any));
    expect(raceOutcomeDetails.getSilkStyle).toHaveBeenCalledWith([{ name: 'event' }], { name: 'outcome' });
  });

  it('should add to betslip', () => {
    component['add'] = jasmine.createSpy('add');
    component.addToBetSlip();
    expect(commandService.executeAsync).toHaveBeenCalled();
  });

  it('#add method', () => {
    component.priceOutCome = {
      id:'1'
    } as any;
    const racingpostGA = {
      location: 'Bet Receipt',
      module: 'RP Tip',
      dimension86: 0,
      dimension87: 0,
      dimension88: null
    } as any;
    addToBetslipByOutcomeIdService = {
      addToBetSlip: jasmine.createSpy('addToBetSlip').and.returnValue(
        observableOf(component.priceOutCome, true, true, false, false, false, true, racingpostGA as any)
      )
    };
    spyOn(component.racingPostGTM, 'emit');
    component['add']();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QUICKBET_PANEL_CLOSE);
    expect(component.racingPostGTM.emit).toHaveBeenCalled();
  });
  it('#add method', () => {
    component.priceOutCome = {
      id:'1'
    } as any;
    const racingpostGA = {
      location: 'Bet Receipt',
      module: 'RP Tip',
      dimension86: 0,
      dimension87: 1,
      dimension88: 1234
    } as any;
    addToBetslipByOutcomeIdService = {
      addToBetSlip: jasmine.createSpy('addToBetSlip').and.returnValue(
        observableOf(component.priceOutCome, true, true, false, false, false, true, racingpostGA as any)
      )
    };
    component['add']();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QUICKBET_PANEL_CLOSE);
  });

  describe('#getSilkAndEdpUrl', () => {
    it('should fetch getSilkAndEdpUrl', () => {
      component.priceOutCome =  {
        displayOrder: 1,
        icon: false,
        id: '125825053',
        name: 'Sancta Sedes',
        silkName: '123.png',
        prices: [{
          priceNum: '9',
          priceDen: '2'
        }
      ]
      } as any;
      const event = mostTippedHorsesEventsMock[0];
      component['getSilkAndEdpUrl'](event as any);
      expect(component.edpPageUrl).not.toBeNull();
      expect(component.silkStyle).not.toBeNull();
      expect(component.isGeneralSilk).not.toBeNull();
    });
  });

  describe('#gaTrack', () => {
    it('should track for view race card click', () => {
      component['gaTrack']();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventAction: 'navigation',
        eventCategory: 'bet receipt',
        eventLabel: 'view full racecard'
      }));
    });
  });

  describe('#tipShownGaTrack', () => {
    it('should track tip shown to the user when eventislive and byb false', () => {
      component['isByB'] = jasmine.createSpy('isByB').and.returnValue(true);
      component['tipShownGaTrack'](mostTippedHorsesEventsMock[0] as any);
      expect(gtmService.push).toHaveBeenCalled();
    });
    it('should track tip shown to the user when eventislive and byb true', () => {
      const event = mostTippedHorsesEventsMock[0] as any;
      event.eventIsLive = true;
      component['isByB'] = jasmine.createSpy('isByB').and.returnValue(false);
      component['tipShownGaTrack'](event);
      expect(gtmService.push).toHaveBeenCalled();
    });
  });
  describe('isByB', () => {
    it('check for byb present when data null', () => {
      const data = null;
      expect(component['isByB'](data)).toBe(null);
    });
    it('check for byb present when byb is null', () => {
      component['racingPostEnv'] = {} as any;
      expect(component['isByB'](mostTippedHorsesEventsMock[0])).toBe(undefined);
    });
    it('check for byb present', () => {
      component['racingPostEnv'] = {
        BYB_CONFIG: {
          HR_YC_EVENT_TYPE_ID: 29027
        }
      } as any;
      expect(component['isByB'](mostTippedHorsesEventsMock[0])).toBe(true);
    });
    it('check for byb present when type is not match', () => {
      component['racingPostEnv'] = {
        BYB_CONFIG: {
          HR_YC_EVENT_TYPE_ID: 1234
        }
      } as any;
      expect(component['isByB'](mostTippedHorsesEventsMock[0])).toBe(false);
    });
  });

  describe('ngOnDestroy', () => {
    it('ngOnDestroy: should unsubscribe from addBetSlip', function () {
      component['addBetSlip'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['addBetSlip'].unsubscribe).toHaveBeenCalled();
      expect(liveServeHandleUpdatesService.unsubscribe).toHaveBeenCalledWith(component['liveServeChannels']);
    });

    it('ngOnDestroy: should not unsubscribe from addBetSlip', function () {
      component['addBetSlip'] = undefined;
      component.ngOnDestroy();

      expect(component['addBetSlip']).not.toBeDefined();
    });
    it('ngOnDestroy: should clear timeout', function () {
      component.ngOnDestroy();
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
    });
    it('ngOnDestroy: should be empty ', function () {
      component.ngOnDestroy();
      expect(component.betData.length).toBe(0);
    });
    it('ngOnDestroy: should be empty ', function () {
      component.ngOnDestroy();
      expect(betSlipService.betData.length).toBe(0);
    });
    it('ngOnDestroy: should unsubscribe ', function () {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('priceOddsFormatChange');
    });
    it('ngOnDestroy: should unsubscribe ', function () {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('RPTipPresent');
    });
    it('ngOnDestroy: should unsubscribe ', function () {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('racingpriceOddsUpdate');
    });
  });

  describe('checkForSuspendedRaces', () => {
    it('should check for suspended horses when statuscode is A', () => {
      const suspendedRaces = UnsuspendedRacesMock as any;
      component['checkForSuspendedRaces'](suspendedRaces);
      expect(component.isSuspended.length).not.toBe(0);
    });
    it('should check for suspended horses when suspended races are undefined', () => {
      const suspendedRaces = undefined;
      component['checkForSuspendedRaces'](suspendedRaces);
      expect(component.isSuspended.length).toBe(0);
    });
    it('should check for suspended horses when outcomestatuscode is S', () => {
      const suspendedRaces = outcomeUnsuspendedRacesMock as any;
      component['checkForSuspendedRaces'](suspendedRaces);
      expect(component.isSuspended.length).toBe(0);
    });
  });

  describe('Redirect edp url and close quickbet', () => {
    it('should emit closeFn', () => {
      spyOn(component.closeFn, 'emit');
      component['gaTrack'] = jasmine.createSpy('gaTrack');
      component.redirectEdpUrl();
      expect(component.closeFn.emit).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalled();
      expect(component['gaTrack']).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QUICKBET_PANEL_CLOSE);
    });

  });

  describe('#isHorseExists', () => {
    it('should set false if horses does not exist', () => {
      const request = [{
        horses: null
      }] as any;
      component.showRacePostTip = false;
      component['isHorseExists'](request);
      expect(component.showRacePostTip).toBe(false);
    });
    it('should set false if horses length is 0', () => {
      const request = [{
        horses: []
      }] as any;
      component.showRacePostTip = false;
      component['isHorseExists'](request);
      expect(component.showRacePostTip).toBe(false);
    });
    it('should set true if horse exists', () => {
      const request = [{
        horses: [
          { id: 2}
        ]
      }] as any;
      component.showRacePostTip = false;
      component['isHorseExists'](request);
      expect(component.showRacePostTip).toBe(true);
    });
  });

  describe('#checkForTipExpired', () => {
    it('should set false if horses event started', () => {
      const time = '2020-11-23T06:55:44.000Z';
      component.racingPostTipTime = betSlipData.response.respTransGetBetDetail.bet[0].date;
      component['checkForTipExpired'](time);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should check for racingposttip time', () => {
      const time = '2020-11-23T06:55:44.000Z';
      component.racingPostTipTime = undefined;
      component['checkForTipExpired'](time);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
  
  
  describe('#checkForBetsData called', () => {

    it('should set true if betplaced on horse with if condition', () => {
      const betData = betPlacedOnHR as any;
      component['checkForBetsData'](betData);
      expect(component['BET_PLACED_ON_HR']).toBe('21');
    });

    it('should set true if betplaced on horse with else condition', () => {
      const betData = {};
      component['quickBetReceipt'] = betPlacedOnHR[0] as any;
      component['checkForBetsData'](betData);
      expect(component['isBetPlacedOnHR']).toBe(true);
    });
  });

  describe('#checkForBetsData', () => {
    beforeEach(() => {
      component['checkForBetType'] = jasmine.createSpy('checkForBetType');
    });

    it('should set true if betData exists', () => {
      const betData = betPlacedOnHR as any;
      component['checkForBetsData'](betData);
      expect(component['checkForBetType']).toHaveBeenCalled();
    });

    it('should set true if betData is empty', () => {
      const betData = [] as any;
      component['checkForBetsData'](betData);
      expect(component['isBetPlacedOnHR']).toBe(true);
    });
  });

  describe('checkForPriceUpdate', () => {
    it('when outcome is present', () => {
      component.historicPrices= [{
      priceDec: Number(1),
      priceDen: Number(1),
      priceNum: Number(3),
      isDisplayed: true,
      priceType: 'LP'
      }];

      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['getCssClass'] = jasmine.createSpy('getCssClass');
      component['checkForPriceUpdate'](priceUpdate as any);
      expect(component['getCssClass']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when outcome is not present', () => {
      component.historicPrices= [{
        priceDec: Number(1),
        priceDen: Number(1),
        priceNum: Number(3),
        isDisplayed: true,
        priceType: 'LP'
      }];
      const update = priceUpdate as any;
      component['getCssClass'] = jasmine.createSpy('getCssClass');
      update.outcomes[0].prices[0].priceDec = 2.3;
      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['checkForPriceUpdate'](update);
      expect(component['getCssClass']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('when outcome is present with historic price length 2', () => {
      component.historicPrices= [{
      priceDec: Number(1),
      priceDen: Number(1),
      priceNum: Number(3),
      isDisplayed: true,
      priceType: 'LP'
      },
      {
        priceDec: Number(1),
        priceDen: Number(1),
        priceNum: Number(3),
        isDisplayed: true,
        priceType: 'LP'
        }];

      component.priceOddsBtn = { nativeElement: { setAttribute: jasmine.createSpy('setAttribute'), classList:{remove:jasmine.createSpy('remove') }}};
      component['getCssClass'] = jasmine.createSpy('getCssClass');
      component['checkForPriceUpdate'](priceUpdate as any);
      expect(component['getCssClass']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('getCssClass', () => {
    it('test for no data', () => {
      component['getCssClass'](null, null);
      expect(component.cssClass).toBe('');
    });
    it('test for bet-down', () => {
      const currPrice = priceUpdate as any;
      const updated = priceUpdate as any;
      component['getCssClass'](currPrice.outcomes[0].prices[0],updated.outcomes[1].prices[0]);
      expect(component.cssClass).toEqual('bet-down');
    });
    it('test for bet-up', () => {
      const currPrice = priceUpdate as any;
      const updated = priceUpdate as any;
      component['getCssClass'](currPrice.outcomes[0].prices[0],updated.outcomes[2].prices[0]);
      expect(component.cssClass).toEqual('bet-up');
    });
    it('test for else condition', () => {
      const currPrice = priceUpdate as any;
      const updated = priceUpdate as any;
      component['getCssClass'](currPrice.outcomes[0].prices[0],updated.outcomes[0].prices[3]);
      expect(component.cssClass).toEqual('');
    });
  });

  describe('#checkForBetType', () => {
    it('should check for not tricast and forecast and isbetplaced on hr is true', () => {
      const betData = betPlacedOnHR as any;
      component['checkForBetType'](betData);
      expect(component['isBetPlacedOnHR']).toBe(true);
    });
    it('should check for tricast and isbetplaced on hr is false', () => {
      const betData = betPlacedOnHR as any;
      betData[0].combiType = 'TRICAST';
      component['checkForBetType'](betData[0]);
      expect(component['isBetPlacedOnHR']).toBe(false);
    });
    it('should check for forecast and isbetplaced on hr is false', () => {
      const betData = betPlacedOnHR as any;
      betData[0].combiType = 'FORECAST';
      component['checkForBetType'](betData[0]);
      expect(component['isBetPlacedOnHR']).toBe(false);
    });
  });
  it('get betData', () => {
    expect(component['oddsClasses']).toEqual('btn-bet');
  });
  it('get betData', () => {
    component.cssClass = 'bet-up';
    expect(component['oddsClasses']).toEqual('btn-bet bet-up');
  });
});
