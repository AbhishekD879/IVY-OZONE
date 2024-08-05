import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf, throwError as observableThrowError, throwError } from 'rxjs';

import { BetslipReceiptComponent } from '@betslip/components/betslipReceipt/betslip-receipt.component';
import { IBetReceiptEntity } from '@betslip/services/betReceipt/bet-receipt.model';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';
import {
  mainBetSingleMock, mostRacingTipsWithOutHorsesMock
} from '@app/lazy-modules/racingPostTip/mock/racing-pot-tip-mock';
import { DecimalPipe } from '@angular/common';
import { betslipReceiptBannerData } from '@app/betslip/components/betslipContainer/mockData/betslip-receipt-banner-data.mock';

describe('BetslipReceiptComponent', () => {
  let component: BetslipReceiptComponent;
  let user,
    betReceiptService,
    sessionService,
    storageService,
    betSlipBannerService,
    betInfoDialogService,
    locationStub,
    gtmService,
    router,
    commandService,
    device,
    gtmTrackingService,
    bodyScrollLockService,
    nativeBridgeService,
    bannersService,
    windowRefService,
    overAskService,
    localeService,
    pubSubService,
    racingPostTipService,
    bppErrorService,
    sessionStorageService,
    fbService,
    firstBetGAService,
    changeDetection,
    scorecastDataService;

  const betslipMock: IBetDetail = {
    betId: '574707',
    betType: 'SGL',
    betTypeName: 'Single',
    betTermsChange: [],
    bonus: '',
    callId: '',
    cashoutStatus: '',
    cashoutValue: '0.90',
    currency: 'GBP',
    date: '2018-12-27 07:24:19',
    eventMarket: 'Win or Each Way',
    eventName: '08:10 Steepledowns',
    ipaddr: '10.80.62.7',
    leg: [],
    legType: 'W',
    name: 'EMILY MOLLIE',
    numLegs: '1',
    numLines: '1',
    numLinesLose: '0',
    numLinesVoid: '0',
    numLinesWin: '0',
    numSelns: '1',
    odds: {
      frac: '5/2',
      dec: '3.50',
    },
    oddsBoosted: false,
    paid: 'Y',
    placedBy: '',
    potentialPayout: '3.50',
    receipt: 'O/0208872/0000115',
    refund: '0.00',
    settleInfo: '',
    settled: 'N',
    settledAt: '',
    source: 'M',
    stake: '1.00',
    stakePerLine: '1.00',
    startTime: '2018-12-27 08:10:00',
    asyncAcceptStatus: 'A',
    status: 'A',
    tax: '0.00',
    taxRate: '0.00',
    taxType: 'S',
    stakeValue: 1.00,
    tokenValue: '0.00',
    uniqueId: '625520283007346341076352773621',
    userId: '',
    winnings: '0.00',
    availableBonuses:undefined
  };
  let sportEvents = [
    {
      id: '123',
    },
    {
      id: '125',
    }
  ];

  const aemMockBanners = [{
    brand: 'coral',
    imgUrl: 'https://banners-cms-assets.coral.co.uk/is/image/1',
    altText: 'Banner 20',
    title: 'Banner 20',
    link: 'https://bet-hl.coral.co.uk/#/betslip/add/665596740',
    target: '_self',
    tcText: '<p><u>HTML T&Cs PLATINUM</u>. 18+. ' +
    'Terms and Conditions Apply. Max bet £10. Please click here to view more. ' +
    '18+. Terms and Conditions Apply. Max bet £10. Please click here to view more. ' +
    '18+. Terms and Conditions Apply. Max bet £10. 18+. 18+.<br>\r\n</p>\r\n',
    tcLink: 'https://bet-hl.coral.co.uk/#/promotions/bet5_get20',
    position: 1,
    lazy: false,
    imgClass: ''
  }];

  const receiptEventsMock = {
    multiples: [
      {
        betTypeName: 'Double',
        betType: 'SGL',
        receipt: 'O/11',
        numLines: '1',
        stake: '5.00',
        numLegs: '1',
        odds: {
          frac: '5/23',
          dec: '3.2',
        },
        potentialPayout: '5.00',
        leg: [
          {
            part: [{ event: { id: 1, }, marketId: '123123' }],
            odds: {
              frac: '5/2',
              dec: '3.50',
            }
          }
        ]
      }
    ],
    singles: [
      {
        betId: '123',
        betType: 'type',
        receipt: 'O/22',
        betTypeName: 'Single',
        stake: '5.00',
        odds: {
          frac: '5/2',
          dec: '3.50',
        },
        eventMarket: 'Match Result',
        numLegs: '1',
        potentialPayout: '5.00',
        leg: [
          {
            part: [{ event: { id: 1, categoryId: '16' }, marketId: '123123' }],
            odds: {
              frac: '5/2',
              dec: '3.50',
            }
          }
        ]
      }
    ]
  } as IBetReceiptEntity;

  const sportEventMock = {
    page: 'betslip',
    categoryId: '6',
    typeId: '5',
    id: '6702260',
    selectionId: '7',
    marketId: '9'
  };


  beforeEach(() => {
    racingPostTipService = {
      racingPostGTM: {},
      updateRaceData: jasmine.createSpy('updateRaceData')
    };
    user = {
      oddsFormat: 'frac',
      receiptViewsCounter: 0,
      winAlertsToggled: false,
      set: jasmine.createSpy(),
      getLoggedInUser: jasmine.createSpy('getLoggedInUser').and.returnValue('user')
    };
    betReceiptService = {
      getActiveSportsEvents: jasmine.createSpy('getActiveSportsEvents').and.returnValue([]),
      getActiveFootballEvents: jasmine.createSpy('getActiveFootballEvents').and.returnValue([]),
      getGtmObject: jasmine.createSpy().and.returnValue({}),
      reuse: jasmine.createSpy('reuse'),
      done: jasmine.createSpy('done'),
      clearMessage: jasmine.createSpy('clearMessage'),
      getBetReceiptSiteCoreBanners: jasmine.createSpy('getBetReceiptSiteCoreBanners').and.returnValue(observableOf(betslipReceiptBannerData)),
      getBetReceipts: jasmine.createSpy('getBetReceipts').and.returnValue(observableOf({})),
      readUpCellBets: jasmine.createSpy('readUpCellBets').and.returnValue(
        observableOf( { 'races': [sportEventMock], nextRace: true })
        ),
        get freeBetStake() {
          return '';
        },
        get totalStake() {
          return '';
        }
    };
  
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve({}))
    };
    storageService = {
      remove: jasmine.createSpy('remove'),
      get: jasmine.createSpy('get')
    };
    betSlipBannerService = {
      setIsBannerAvailable: jasmine.createSpy(),
      setBanner: jasmine.createSpy()
    };
    betInfoDialogService = {
      multiple: jasmine.createSpy()
    };
    locationStub = {
      path: () => ''
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    router = {
      navigate: jasmine.createSpy()
    };
    commandService = {
      executeAsync: () => Promise.resolve({
        streamActive: true,
        streamID: '111'
      }),
      API: {
        GET_LIVE_STREAM_STATUS: ''
      }
    };
    device = {
      isMobileOnly: true
    };
    gtmTrackingService = {};
    bodyScrollLockService = {
      enableBodyScroll: jasmine.createSpy('enableBodyScroll')
    };
    nativeBridgeService = {};

    windowRefService = {
      nativeWindow: {
        NativeBridge : { pushNotificationsEnabled: true },
        location: {
          pathname: 'testPath'
        }
      }
    } as any;

    bannersService = {
      fetchBetslipOffersFromAEM: jasmine.createSpy('fetchBetslipOffersFromAEM').and.returnValue(
        observableOf({offers: aemMockBanners})
      )
    };

    overAskService = {
      setStateAndClearInStorage: jasmine.createSpy('setStateAndClearInStorage'),
      states: {
        off: 'off'
      }
    };

    localeService = {
      getString: jasmine.createSpy('getString')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    bppErrorService = jasmine.createSpyObj('bppErrorService', ['showPopup', 'errorHandler']);

    sessionStorageService = {
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'firstBetTutorial') { return {firstBetAvailable:'true'}} 
          else if(n === 'buttonText') { return false}
          else { return true}
      }), 
      set: jasmine.createSpy('set')
      };
    fbService = {isBetPack: jasmine.createSpy('isBetPack'),
                 isFanzone:jasmine.createSpy('isFanzone')};
    changeDetection = {
      detectChanges: jasmine.createSpy('detectChanges')
    }
    firstBetGAService = {
      setGtmData: jasmine.createSpy('setGtmData'),
    };
    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { 
        return {
          eventLocation: 'scorecast',
          teamname: 'teamname',
          playerName: 'playerName',
          result: '24',
          dimension64: '64'
        }
      },
    }
  });

  function createComponent() {
    component = new BetslipReceiptComponent(user, betReceiptService, sessionService, storageService,
      betInfoDialogService, locationStub, gtmService, router, commandService, device, gtmTrackingService,
      bodyScrollLockService, nativeBridgeService, windowRefService, overAskService, localeService, pubSubService,
      bppErrorService, racingPostTipService,sessionStorageService,fbService, firstBetGAService,changeDetection,scorecastDataService);
    component.racingPostToggle = {enabled:true,quickBetReceipt:true,mainBetReceipt:true};
  }

  afterEach(() => {
    component = null;
  });

  it('should create component instance', () => {
    createComponent();
    expect(component).toBeTruthy();
  });

  it('ngInit', fakeAsync(() => {
    betReceiptService.getActiveFootballEvents.and.returnValue([]);
    betReceiptService.getActiveSportsEvents.and.returnValue(sportEvents);
    createComponent();
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.allReceipts = receiptEventsMock;
    tick();
    expect(component.allReceipts).toEqual(receiptEventsMock);
    tick();
  }));

  it('Should track site core banners', () => {
    createComponent();
    component.trackSiteCoreBanners("p1%20-%201-2-free%20week%2012%20-%20uk%20-%2027th%20march%20-%201st%20april");
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('ngInit no data - Observable error', fakeAsync(() => {
    betReceiptService.getActiveSportsEvents.and.returnValue(sportEvents);
    betReceiptService.getBetReceipts.and.returnValue(throwError('error'));
    createComponent();
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnInit();
    expect(component.loadComplete).toEqual(false);
    tick();
    expect(component.loadComplete).toBeTruthy();
    expect(component.loadFailed).toBeTruthy();
    expect(bppErrorService.showPopup).toHaveBeenCalled();

  }));

  it('reloadComponent no data - Observable error', fakeAsync(() => {
    betReceiptService.getActiveSportsEvents.and.returnValue(sportEvents);
    betReceiptService.getBetReceipts.and.returnValue(throwError('error'));
    createComponent();
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
    component.reloadComponent();
    expect(component.loadComplete).toEqual(false);
    tick();
    expect(component.loadComplete).toBeTruthy();
    expect(component.loadFailed).toBeTruthy();
    expect(bppErrorService.showPopup).toHaveBeenCalled();

  }));

  it('ngInit no data - Observable success', fakeAsync(() => {
    betReceiptService.getBetReceipts.and.returnValue(observableOf(receiptEventsMock));
    createComponent();
    spyOn(component, 'core');
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnInit();
    tick(2000);
    expect(component.loadComplete).toEqual(true);
    expect(bppErrorService.showPopup).not.toHaveBeenCalled();

    expect(component.core).toHaveBeenCalledWith(receiptEventsMock as any);
  }));

  it('reloadComponent no data - Observable success', fakeAsync(() => {
    betReceiptService.getBetReceipts.and.returnValue(observableOf(receiptEventsMock));
    createComponent();
    spyOn(component, 'core');
    component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
    component.reloadComponent();
    tick(2000);
    expect(component.loadComplete).toEqual(true);
    expect(bppErrorService.showPopup).not.toHaveBeenCalled();

    expect(component.core).toHaveBeenCalledWith(receiptEventsMock as any);
  }));


  it('ngInit should start data initialization', fakeAsync(() => {
    betReceiptService.getBetReceipts.and.returnValue(observableOf(receiptEventsMock));
    createComponent();
    spyOn(component, 'core');
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnInit();
    tick();

    expect(component.loadComplete).toEqual(true);
    expect(sessionService.whenProxySession).toHaveBeenCalled();
    expect(betReceiptService.getBetReceipts).toHaveBeenCalled();
  }));

  it('ngInit should start data initialization', fakeAsync(() => {
    betReceiptService.getBetReceipts.and.returnValue(observableOf(receiptEventsMock));
    createComponent();
    spyOn(component, 'core');
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnInit();
    tick();

    expect(component.loadComplete).toEqual(true);
    expect(sessionService.whenProxySession).toHaveBeenCalled();
    expect(betReceiptService.getBetReceipts).toHaveBeenCalled();
  }));

  it('should return true if external URL', () => {
    createComponent();
    expect(component.isExternalUrl('https://example.com')).toBeTruthy();
  });

  it('should redirect to favourites', () => {
    createComponent();
    component.goToFavourites();
    expect(router.navigate).toHaveBeenCalledWith(['/favourites']);
  });

  it('overask, deposit overask declined', fakeAsync(() => {
    betReceiptService.getBetReceipts.and.returnValue(observableOf([receiptEventsMock, receiptEventsMock]));
    overAskService.isAllBetsDeclined = true;
    localeService.getString = jasmine.createSpy('getString').and.returnValue('bs.depositAndPlacebetSuccessMessage');
    createComponent();
    component.message = {
      msg: 'bs.depositAndPlacebetSuccessMessage'
    };
    sessionStorageService.get.and.returnValue( {firstBetAvailable:true});
    storageService.get.and.returnValue( true);
    component.winAlertsEnabled = true;
    component.winAlertsActive = true;
    component.ngOnInit();
    tick();
    expect(component.message.msg).toBeUndefined();
  }));

  describe('ngOnDestroy', () => {

    beforeEach(() => {
      createComponent();
    });
    it('should not finish overask if not in progress', () => {
      overAskService.isInFinal = false;
      component.ngOnDestroy();

      expect(overAskService.setStateAndClearInStorage).not.toHaveBeenCalled();
    });

    it('should set state and clear in storage ', () => {
      overAskService.isInFinal = true;
      component.ngOnDestroy();

      expect(overAskService.setStateAndClearInStorage).toHaveBeenCalledWith(overAskService.states.off);
    });

    it('should call pubSubService.publish with "OVERASK_CLEAN_BETSLIP" and "false" params', () => {
      component['isBettingDone'] = true;

      component.ngOnDestroy();
      expect(pubSubService.publish).toHaveBeenCalledWith('OVERASK_CLEAN_BETSLIP', false);
    });

    it('should not call pubSubService.publish when isBettingDone set to false', () => {
      component.ngOnDestroy();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should clear bet receipt messages after component destroy', () => {
      component.ngOnDestroy();
      expect(betReceiptService.clearMessage).toHaveBeenCalled();
    });

    it('should racingposttip after component destroy', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('racingposttip');
    });
    it('ngOnDestroy: should unsubscribe from upCellSubscription', function () {
      component['upCellSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['upCellSubscription'].unsubscribe).toHaveBeenCalled();
    });
    it('ngOnDestroy: should not unsubscribe from upCellSubscription', function () {
      component['upCellSubscription'] = undefined;
      component.ngOnDestroy();

      expect(component['upCellSubscription']).not.toBeDefined();
    });
  });

  it('done', () => {
    createComponent();
    component.done();
    expect(component['isBettingDone']).toEqual(true);
    expect(betReceiptService.done).toHaveBeenCalled();
    expect(storageService.remove).toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections');
    expect(storageService.remove).toHaveBeenCalledWith('vsbr-selection-map');
    expect(storageService.remove).toHaveBeenCalledWith('lastMadeBetSport');
    expect(storageService.remove).toHaveBeenCalledWith('lastMadeBet');
  });

  it('should reuse', fakeAsync(() => {
    betReceiptService.reuse.and.returnValue(Promise.resolve());
    createComponent();
    component.reuse();
    expect(component.reusePending).toBeTruthy();
    tick();
    expect(component.reusePending).toBeFalsy();
  }));

  it('should trigger publish in reuse', () => {
    createComponent();
    component.allReceipts = {singles: [], multiples:[]};
    component.allReceipts.multiples = [{provider: 'betLottery', details:{}}] as any;
    component.reuse();
    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should navigate to home page if there are no data', fakeAsync(() => {
    const decimalPipe = new DecimalPipe('en-US');
    createComponent();
    component.core(false as any);
    tick(2000);
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  }));

  describe('should call for banners with proper parameters', () => {
    it('coral, not desktop - mobile device', fakeAsync(() => {
      betReceiptService.getActiveFootballEvents.and.returnValue([sportEventMock]);
      betReceiptService.getActiveSportsEvents.and.returnValue([sportEventMock]);
      environment.brand = 'bma';
      device = {
        isDesktop: false
      };
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
    }));

    it('coral, default device', fakeAsync(() => {
      betReceiptService.getActiveFootballEvents.and.returnValue([sportEventMock]);
      betReceiptService.getActiveSportsEvents.and.returnValue([sportEventMock]);
      environment.brand = 'bma';
      device = {
        isDesktop: true
      };
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
    }));
  });

  describe('core', () => {

    beforeEach(() => {
      betReceiptService.getActiveSportsEvents.and.returnValue(sportEvents);
      betReceiptService.getActiveFootballEvents.and.returnValue([sportEventMock]);
    });

    describe('isAllBetsDeclined doublecheck', () => {

      it('should not treat all bets as declined - OA accepted, has active multiples', fakeAsync(() => {
        overAskService.isAllBetsDeclined = false;
        const decimalPipe = new DecimalPipe('en-US');
        createComponent();
        component.message = <any>{
          msg: 'test'
        };
        component._racingPostGA = undefined;
        component.core([
          {
            multiples: [{}],
            singles: [{}]
          } as IBetReceiptEntity,
          {
            multiples: [{}],
            singles: []
          } as IBetReceiptEntity
        ]);
        tick(2000);
        expect(component.isAllBetsDeclined).toBe(false);
        expect(pubSubService.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET', 1);
      }));

      it('should not treat all bets as declined - OA accepted, has active singles', fakeAsync(() => {
        overAskService.isAllBetsDeclined = false;
        const decimalPipe = new DecimalPipe('en-US');
        createComponent();
        component.message = <any>{
          msg: 'test'
        };
        component._racingPostGA = undefined;
        component.core([
          {
            multiples: [{}],
            singles: [{}]
          } as IBetReceiptEntity,
          {
            multiples: [],
            singles: [{}]
          } as IBetReceiptEntity
        ]);
        tick(2000);
        expect(component.isAllBetsDeclined).toBe(false);
        expect(pubSubService.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET', 1);
      }));

      it('should treat all bets as declined - OA accepted, but no active bets (topup)', fakeAsync(() => {
        overAskService.isAllBetsDeclined = false;
        createComponent();
        component.message = <any>{
          msg: 'test'
        };
        component._racingPostGA = undefined;
        const decimalPipe = new DecimalPipe('en-US');
        component.core([
          {
            multiples: [{}],
            singles: [{}]
          } as IBetReceiptEntity,
          {
            multiples: [],
            singles: []
          } as IBetReceiptEntity
        ]);
        tick(2000);
        expect(component.totalStake).toBe(undefined);
        expect(component.totalEstimatedReturns).toBe(undefined);
        expect(component.betDate).toBe(undefined);
        expect(localeService.getString).toHaveBeenCalledWith('bs.depositAndPlacebetSuccessMessage');
        expect(component.isAllBetsDeclined).toBe(true);
      }));

      it('should not calculate if all declined', fakeAsync(() => {
        overAskService.isAllBetsDeclined = true;
        const decimalPipe = new DecimalPipe('en-US');
        createComponent();
        component.message = <any>{
          msg: 'test'
        };
        component._racingPostGA = undefined;
        component.core([receiptEventsMock, receiptEventsMock]);
        tick(2000);
        expect(component.totalStake).toBe(undefined);
        expect(component.totalEstimatedReturns).toBe(undefined);
        expect(component.betDate).toBe(undefined);
        expect(localeService.getString).toHaveBeenCalledWith('bs.depositAndPlacebetSuccessMessage');
      }));
    });

    it('should set first banner coming from AEM Target', fakeAsync(() => {
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
    }));

    it('should toggleWinAlerts on init', fakeAsync(() => {
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component.toggleWinAlerts = <any>jasmine.createSpy('toggleWinAlerts');
      component.winAlertsActive = true;
      component.winAlertsEnabled = true;
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(component.toggleWinAlerts).toHaveBeenCalledTimes(2);
    }));

    it('should return true', () => {
      createComponent();
      component.winAlertsEnabled = true;
      component.winAlertsActive = true;
      storageService.get.and.returnValue( true);
      component.ngOnInit();
    })

    it('should test success placebet GTM event not on mobile version', fakeAsync(() => {
      const decimalPipe = new DecimalPipe('en-US');
      const receipts = {
        singles: [{ }],
        multiples: [{ }]
      } as IBetReceiptEntity;
      createComponent();
      component._racingPostGA = {
          location: 'Bet Receipt',
          module: 'RP Tip',
          dimension86: 0,
          dimension87: 0,
          dimension88: null
      } as any;
      spyOn(component, 'getReceiptNumbers').and.returnValue('test numbers' as any);
      component.core([receipts, receipts]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname
      });
    }));

    it ('should test success placebet GTM event on mobile version', fakeAsync(() => {
      const receipts = {
        singles: [{ }],
        multiples: []
      } as IBetReceiptEntity;
      createComponent();
      component._racingPostGA = undefined;
      spyOn(component, 'getReceiptNumbers').and.returnValue('test numbers' as any);
      component.core([receipts, receipts]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname
      });
    }));

    it('should not set banner coming from AEM Target if there is an empty response', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf(null));
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
    }));

    it('should be set freebet & totalstake from freebetsStake$1', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf(null));
      spyOnProperty(betReceiptService, 'freeBetStake').and.returnValue('0.4');
      spyOnProperty(betReceiptService, 'totalStake').and.returnValue('1.4');
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(component.totalStake).toBe(1);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
    }));
    it('should be set freebet=null & totalstake from freebetsStake$2', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf(null));
      spyOnProperty(betReceiptService, 'freeBetStake').and.returnValue(null);
      spyOnProperty(betReceiptService, 'totalStake').and.returnValue('1.4');
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(component.totalStake).toBe(1.4);
    }));
    it('should be set freebet=0 & totalstake from freebetsStake$3', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf(null));
      spyOnProperty(betReceiptService, 'freeBetStake').and.returnValue(0);
      spyOnProperty(betReceiptService, 'totalStake').and.returnValue('1.4');
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
      expect(component.totalStake).toBe(1.4);
    }));
    it('should not set banner coming from AEM Target if there is offers is empty', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf({ offers: null }));
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
    }));

    it('should not set banner coming from AEM Target if there is offers length is 0', fakeAsync(() => {
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableOf({ offers: [] }));

      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
    }));

    it('should add stream dimentions', fakeAsync(() => {
      (betReceiptService.getGtmObject as jasmine.Spy).and.returnValue({
        ecommerce: {
          purchase: {
            products: [
              {}
            ]
          }
        }
      });
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      racingPostTipService.racingPostGTM = {
        location: 'Bet Receipt',
        module: 'RP Tip',
        dimension86: 0,
        dimension87: 0,
        dimension88: null
      };
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname,
        ecommerce: {
          purchase: {
            products: [{
              dimension64: '64', 
              dimension65: 'edp', 
              dimension180: 'scorecast;teamname;playerName;24',
              dimension87: 1,
              dimension88: '111'
            }]
          }
        }
      } as any);

    }));

    it('should add stream dimentions if no stream and no id', fakeAsync(() => {
      commandService.executeAsync = jasmine.createSpy('').and.returnValue(Promise.resolve({}));
      (betReceiptService.getGtmObject as jasmine.Spy).and.returnValue({
        ecommerce: {
          purchase: {
            products: [
              {}
            ]
          }
        }
      });
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname,
        ecommerce: {
          purchase: {
            products: [{
              dimension64: '64', 
              dimension65: 'edp', 
              dimension180: 'scorecast;teamname;playerName;24',
              dimension87: 0,
              dimension88: null
            }]
          }
        }
      } as any);
    }));

    it('should not add stream dimentions when no data', fakeAsync(() => {
      (betReceiptService.getGtmObject as jasmine.Spy).and.returnValue({
        ecommerce: {
          purchase: {
            products: {}
          }
        }
      });
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname,
        ecommerce: {
          purchase: {
            products: {}
          }
        }
      } as any);
    }));

    it('should not add stream dimentions when no purchase', fakeAsync(() => {
      (betReceiptService.getGtmObject as jasmine.Spy).and.returnValue({
        ecommerce: {}
      });
      const decimalPipe = new DecimalPipe('en-US');
      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        location: windowRefService.nativeWindow.location.pathname,
        ecommerce: {}
      } as any);
    }));

    it('should handle error on fetchBetslipOffersFromAEM failure', fakeAsync(() => {
      const decimalPipe = new DecimalPipe('en-US');
      betReceiptService.getActiveFootballEvents.and.returnValue([]);
      betReceiptService.getActiveSportsEvents.and.returnValue([]);
      bannersService.fetchBetslipOffersFromAEM.and.returnValue(observableThrowError('someError'));

      createComponent();
      component._racingPostGA = undefined;
      component.core([receiptEventsMock, receiptEventsMock]);
      tick(2000);
      expect(betSlipBannerService.setBanner).not.toHaveBeenCalled();
    }));

    it ('should call readupcellBets method', fakeAsync(() => {
      const racingPostData = [{
        'date':'2020-11-23T05:13:58.000Z',
        leg: [{
          part: [{
            'startTime': '2020-11-23 11:11:11',
            'username': 'user',
            'eventId': '12345',
            'brand': environment.brand,
            'eventCategoryId': '21'
          }]
        }]
      }] as any;
      createComponent();
      component.allReceipts = {
        singles: [{ }],
        multiples: []
      } as IBetReceiptEntity;
      component._racingPostGA = undefined;
      component.readUpcellBets =  jasmine.createSpy('readUpcellBets');
      component.sendRacingPostByUpcell(racingPostData);
      tick();
      
      expect(component.readUpcellBets).toHaveBeenCalled();
    }));
  });

  it('track by index', () => {
    createComponent();
    expect(component.trackByIndex(1)).toBe(1);
  });

  it('is Single?', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = receiptEventsMock.singles;
    component.allReceipts.multiples = receiptEventsMock.multiples;
    expect(component.isSingles()).toBe(true);
  });

  it('is Multiple?', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = receiptEventsMock.singles;
    component.allReceipts.multiples = receiptEventsMock.multiples;
    expect(component.isMultiples()).toBe(true);
  });

  it('is Multiple? should return false', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = receiptEventsMock.singles;
    component.allReceipts.multiples = [];
    expect(component.isMultiples()).toBeFalsy();
  });

  it('openSelectionMultiplesDialog', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.multiples = receiptEventsMock.multiples;
    spyOn(component, 'getBetReceiptById').and.returnValue(betslipMock);
    component.openSelectionMultiplesDialog(0);
    expect(betInfoDialogService.multiple).toHaveBeenCalledWith(component.allReceipts.multiples[0].betType,
      Number(component.allReceipts.multiples[0].numLines));
  });

  it('getBetReceiptById should return singles', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = receiptEventsMock.singles;
    expect(component.getBetReceiptById(0, false)).toBe(component.allReceipts.singles[0]);
  });

  it('getBetReceiptById should return multiples', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.multiples = receiptEventsMock.multiples;
    expect(component.getBetReceiptById(0, true)).toBe(component.allReceipts.multiples[0]);
  });

  it('isFootballAvailable should return false', () => {
    createComponent();
    sportEvents = [];
    betReceiptService.getActiveFootballEvents.and.returnValue(sportEvents);
    expect(component.isFootballAvailable).toBe(false);
  });

  it('getReceiptNumbers', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = receiptEventsMock.singles;
    component.allReceipts.multiples = receiptEventsMock.multiples;
    expect(component.getReceiptNumbers(receiptEventsMock as IBetReceiptEntity)).toEqual(['O/22', 'O/11']);
  });

  it('getReceiptNumbers should return empty array', () => {
    createComponent();
    component.allReceipts = {} as IBetReceiptEntity;
    component.allReceipts.singles = [];
    component.allReceipts.multiples = [];
    expect(component.getReceiptNumbers(receiptEventsMock as IBetReceiptEntity)).toEqual([]);
  });

  it('should unlock scroll on bet receipt', () => {
    createComponent();
    spyOn<any>(component, 'core');
    component.sendRacingPostByUpcell = jasmine.createSpy('sendRacingPostByUpcell');
    component.ngOnInit();

    expect(bodyScrollLockService.enableBodyScroll).toHaveBeenCalled();
  });

  it('toggleWinAlerts should emit an action', () => {
    const receipt = {
      uniqueId: '123',
      betId: '111'
    } as IBetDetail;

    createComponent();
    spyOn(component.winAlertsToggleChanged, 'emit');

    component.toggleWinAlerts({ receipt, state: true });

    expect(component.winAlertsToggleChanged.emit).toHaveBeenCalled();
    expect(user.set).toHaveBeenCalledWith({winAlertsToggled : true});
  });

  it('toggleWinAlerts should not call user set ', () => {
    const receipt = {
      uniqueId: '123',
      betId: '111'
    } as IBetDetail;

    createComponent();
    component['user'] = {
      winAlertsToggled : true
    } as any;

    spyOn(component.winAlertsToggleChanged, 'emit');
    component.toggleWinAlerts({ receipt, state: true });

    expect(user.set).not.toHaveBeenCalled();
    expect(component.winAlertsToggleChanged.emit).toHaveBeenCalled();
  });

  it('toggleWinAlerts should not emit an action', () => {
    const receipt = {
      uniqueId: '123',
      betId: '111'
    } as IBetDetail;
    windowRefService.nativeWindow.NativeBridge.pushNotificationsEnabled = false;
    createComponent();
    spyOn(component.winAlertsToggleChanged, 'emit');


    component.toggleWinAlerts({ receipt, state: true });

    expect(user.set).not.toHaveBeenCalled();
  });

  describe('receipt list', () => {
    const singleBet = { receipt: '123' };
    const multipleBet = { receipt: '456' };
    const receipts = {
      singles: [singleBet],
      multiples: [multipleBet]
    } as IBetReceiptEntity;

    beforeEach(() => {
      createComponent();
      component.allReceipts = receipts;
    });

    it('should get receipt numbers', () => {
      expect(component.getReceiptNumbers(receipts)).toEqual(['123', '456']);
    });

    it('should get all bets', () => {
      expect(component.getAllBets(receipts)).toEqual([singleBet, multipleBet] as IBetDetail[]);
    });

    it('should ckeck for boosted bets (has not boosted bets)', () => {
      expect(component.hasBoostedBets(receipts)).toEqual(false);
    });

    it('should ckeck for boosted bets (has boosted bets)', () => {
      receipts.singles[0].oddsBoosted = true;
      expect(component.hasBoostedBets(receipts)).toEqual(true);
    });
  });

  describe('#getReceiptCounter', () => {
    it('should count receipts', () => {
      createComponent();
      const singleBet = { receipt: '123' };
      const multipleBet = { receipt: '456' };
      const receipts = {
        singles: [singleBet],
        multiples: [multipleBet]
      } as IBetReceiptEntity;
      component.allReceipts = receipts;
      expect(component['getReceiptCounter']()).toEqual(2);
    });
  });

  it('should return overask service', () => {
    createComponent();
    expect(component.overask).toEqual(overAskService);
  });

  
  describe('sendRacingPostByUpcell', () => {
    it('should make successful request with params', () => {
      const betSlipData = [{
        'date':'2020-11-23T05:13:58.000Z',
        leg: [{
          part: [{
            'startTime': '2020-11-23 11:11:11',
            'username': 'user',
            'eventId': '12345',
            'brand': environment.brand,
            'eventCategoryId': '21'
          }]
        }]
      }] as any;
      createComponent();
      component.allReceipts = {
        singles: [{ }],
        multiples: []
      } as IBetReceiptEntity;
      component.readUpcellBets =  jasmine.createSpy('readUpcellBets');
      component.sendRacingPostByUpcell(betSlipData);
      expect(component.racingPostData).not.toEqual(null);
      expect(component.readUpcellBets).toHaveBeenCalled();
    });
  });

  describe('sendRacingPostByUpcell', () => {
    it('should make unsuccessful request with params', () => {
      const betSlipData =  [{
        'date':'2020-11-23T05:13:58.000Z',
        leg: [{
          part: [{
            'startTime': '11/11/11 11:11:11',
            'username': 'user',
            'eventId': '12345',
            'brand': environment.brand,
            'eventCategoryId': '18'
          }]
        }]
      }] as any;
      createComponent();
      component.allReceipts = {
        singles: [{ }],
        multiples: []
      } as IBetReceiptEntity;
      component.readUpcellBets =  jasmine.createSpy('readUpcellBets');
      component.sendRacingPostByUpcell(betSlipData);
      expect(component.readUpcellBets).not.toHaveBeenCalled();
    });
    it('singles Token & Free Bet @getFreebetLabelText', () => {
      createComponent();
      fbService.isBetPack.and.returnValues(true, false);
      component.allReceipts.singles = [
        {
          tokenValue: '7.00',
          freebetOfferCategory: 'Bet Pack'
        },{
          tokenValue: '7.00',
        }
        ] as any;
      expect(component.getFreebetLabelText()).toEqual('TOKEN & FREE BET');
    });
    it('singles fanzone & Free Bet @getFreebetLabelText', () => {
      createComponent();
      fbService.isBetPack.and.returnValues(false, false);
      fbService.isFanzone.and.returnValues(true, false);

      component.allReceipts.singles = [
        {
          tokenValue: '7.00',
          freebetOfferCategory: 'Fanzone'
        },{
          tokenValue: '7.00',
        }
        ] as any;
      expect(component.getFreebetLabelText()).toEqual('FREE BET');
    });
    it('@multiples freebet getFreebetLabelText', () => {
      createComponent();
      fbService.isBetPack.and.returnValue(false);
      component.allReceipts.multiples = [
        {
          
        },
        {
          tokenValue: '3.00',
        }
        ] as any;
      expect(component.getFreebetLabelText()).toEqual('FREE BET');
  });

  it('@multiples Bet Token getFreebetLabelText', () => {
    createComponent();
    fbService.isBetPack.and.returnValue(true);
    component.allReceipts.multiples =  [
      {
        tokenValue: '7.00',
        freebetOfferCategory: 'Bet Pack'
      }
    ] as any;
    expect(component.getFreebetLabelText()).toEqual('BET TOKEN');
});
it('@multiples Fanzone getFreebetLabelText', () => {
  createComponent();
  fbService.isBetPack.and.returnValue(false);
  fbService.isFanzone.and.returnValue(true);

  component.allReceipts.multiples =  [
    {
      tokenValue: '7.00',
      freebetOfferCategory: 'Fanzone'
    }
  ] as any;
  expect(component.getFreebetLabelText()).toEqual('Fanzone');
});

it('@multiples empty getFreebetLabelText', () => {
  createComponent();
  component.allReceipts = receiptEventsMock;
  fbService.isBetPack.and.returnValue(false);
  expect(component.getFreebetLabelText()).toEqual('');
});

it('@multiples empty getFreebetLabelText', () => {
  createComponent();
  fbService.isBetPack.and.returnValue(false);
  component.allReceipts.singles =  [] as any;
  expect(component.getFreebetLabelText()).toEqual('');
});
  });

  it('onRacingPostGTMEvent', () => {
    racingPostTipService = {
      racingPostGTM: jasmine.createSpy('racingPostGTM')
    };
    createComponent();
    const mock = {
      output: 'racingPostGTM',
      value: {
        location: 'Bet Receipt',
        module: 'RP Tip',
        dimension86: 0,
        dimension87: 0,
        dimension88: null
      }
    } as any;
    component.onRacingPostGTMEvent(mock);
  });


  describe('#enableRacingPostTip', () => {
    it('should return value as true', () => {
      createComponent();
      component.allReceipts.multiples = [];
      component.allReceipts.singles = mainBetSingleMock as any;
      const flag = component.enableRacingPostTip();
      expect(flag).toEqual(true);
    });
    it('should return value as false', () => {
      createComponent();
      component.allReceipts.multiples = mostRacingTipsWithOutHorsesMock as any;
      component.allReceipts.singles = []
      const flag = component.enableRacingPostTip();
      expect(flag).toEqual(false);
    });
    it('should return value as true', () => {
      createComponent();
      component.isNextRacesData = false;
      component.allReceipts.multiples = [];
      component.allReceipts.singles = mainBetSingleMock as any;
      const flag = component.enableRacingPostTip();
      expect(flag).toEqual(true);
    });
  });

  describe('#readUpCellBets', () => {

    it('should not call publish', () => {
      createComponent();
      component.readUpcellBets('/bets', [{}]);
      expect(pubSubService.publish).toHaveBeenCalled();
    });

    it('should not call publish', () => {
      betReceiptService['readUpCellBets'] = jasmine.createSpy('readUpCellBets').and.returnValue(
        observableOf( { 'races': [sportEventMock], nextRace: false }))
      createComponent();
      component.readUpcellBets('/bets', [{}]);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  describe('betpack Onboarding', () => {
    it('Should call loadOnBoardingInfo on load when local storage has onBoardtutorial', () => {
        user = { username: 'testUser' } as any;
        device = { isMobile : true, isMobileOnly: true }   as any;
        storageService = {
            get: jasmine.createSpy('get').and.returnValue({onBoardingTutorial: { 'betPack-testUser': true }})
        };
        component = new BetslipReceiptComponent(user, betReceiptService, sessionService, storageService,
          betInfoDialogService, locationStub, gtmService, router, commandService, device, gtmTrackingService,
          bodyScrollLockService, nativeBridgeService, windowRefService, overAskService, localeService, pubSubService,bppErrorService, racingPostTipService, sessionStorageService, fbService, firstBetGAService,changeDetection,scorecastDataService);
        component.ngOnInit();

        expect(component.isUserLoggedIn).toEqual(true);
        expect(component.isMobile).toEqual(true);
    });

    it('Should call loadOnBoardingInfo on load when local storage doesnt have onBoardtutorial', () => {
        user = { username: 'testUser' } as any;
        device = { isMobile : true }   as any;
        storageService = {
            get: jasmine.createSpy('get').and.returnValue(false)
        };
        component = new BetslipReceiptComponent(user, betReceiptService, sessionService, storageService,
          betInfoDialogService, locationStub, gtmService, router, commandService, device, gtmTrackingService,
          bodyScrollLockService, nativeBridgeService, windowRefService, overAskService, localeService, pubSubService,bppErrorService, racingPostTipService, sessionStorageService, fbService, firstBetGAService,changeDetection, scorecastDataService);        
          
        component.ngOnInit();

        expect(component.isUserLoggedIn).toEqual(true);
        expect(component.isMobile).toEqual(true);
    });


    it('should close the onboarding screen on close emitter', () => {
      component = new BetslipReceiptComponent(user, betReceiptService, sessionService, storageService,
        betInfoDialogService, locationStub, gtmService, router, commandService, device, gtmTrackingService,
        bodyScrollLockService, nativeBridgeService, windowRefService, overAskService, localeService, pubSubService,bppErrorService, racingPostTipService, sessionStorageService, fbService, firstBetGAService,changeDetection, scorecastDataService);  
        const event: any = { output: 'closeOnboardingEmitter',value: ''}
        component.handleOnBoardingEvents(event);
        expect(component.onBetReceiptOverlaySeen).toEqual(true);
    });
});
  
});