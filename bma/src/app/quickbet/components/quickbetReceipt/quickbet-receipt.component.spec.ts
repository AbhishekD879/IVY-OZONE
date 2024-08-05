import { QuickbetReceiptComponent } from './quickbet-receipt.component';
import { IQuickbetReceiptDetailsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { BYBBet } from '@yourcall/models/bet/byb-bet';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { mostRacingTipDataComp } from '@app/lazy-modules/racingPostTip/mock/racing-pot-tip-mock';
/* eslint-disable */
import { of, throwError as observableThrowError } from 'rxjs';
import { of as observableOf } from 'rxjs';
/* eslint-enable */
import { FIVESELECTIONSWITHE, THREESELECTIONSWITHF, FIVESELECTIONSWITHF
} from '@app/quickbet/components/quickbetReceipt/quickbet-receipt.mock';
import { FirstBetGAService } from '@app/lazy-modules/onBoardingTutorial/firstBetPlacement/services/first-bet-ga.service';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';

describe('QuickBetReceiptComponent', () => {
  let component: QuickbetReceiptComponent;
  let userService;
  let filtersService;
  let quickbetService;
  let nativeBridge;
  let cmsService;
  let window;
  let storageService;
  let gtmService,maxPayOutErrorService;
  let pubSubService;
  let http, racingPostTipService;
  let fiveASideEntryConfirmationService;
  let fiveASideContestSelectionService;
  let freeBetsService;
  let locale, firstBetGAService, betReuseService, sessionStorage;
  let bonusSuppressionService;

  beforeEach(() => {
    racingPostTipService = {
      updateRaceData: jasmine.createSpy('updateRaceData')
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };
    userService = {
      currencySymbol: '$',
      receiptViewsCounter: 0,
      winAlertsToggled: false,
      set: jasmine.createSpy(),
      username: 'test',
      post: jasmine.createSpy().and.returnValue(observableOf({ body: {} })),
      getLoggedInUser: jasmine.createSpy('getLoggedInUser').and.returnValue('user'),
      bppToken: 'kjkjhkjahsldjads'
    };

    filtersService = {
      setCurrency: jasmine.createSpy(),
      filterPlayerName: jasmine.createSpy('filterPlayerName').and.returnValue(''),
      filterAddScore: jasmine.createSpy('filterAddScore').and.returnValue('')
    };

    quickbetService = {
      getOdds: jasmine.createSpy('getOdds'),
      getLinesPerStake: jasmine.createSpy('getLinesPerStake').and.returnValue('2 Lines at £1 per line'),
      getEWTerms: jasmine.createSpy('getEWTerms').and.returnValue('Each Way Odds 1/5 Places 1-2-3'),
      isVirtualSport: jasmine.createSpy('isVirtualSport').and.returnValue(true),
      getBybSelectionType: jasmine.createSpy('getBybSelectionType'),
      readUpCellBets: jasmine.createSpy('readUpCellBets').and.returnValue( 
        observableOf( { 'races': mostRacingTipDataComp, nextRace: true } as any))
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({ body: 'data' })),
      post: jasmine.createSpy().and.returnValue(observableOf({ body: {} }))
    };

    fiveASideEntryConfirmationService = {
      getShowdownConfirmationDisplay: jasmine.createSpy('getShowdownConfirmationDisplay'),
      isTestOrRealUser: jasmine.createSpy('isTestOrRealUser')
    };

    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
      } as any)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
		FiveASideGameLauncher: { entryTermsAndConditionsTag : "Conditions Apply."},
        CelebratingSuccess: {
          displaySportIcon: ['quickbet']
        }
      })),
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(of({
        svg: 'svg',
        svgId: 'svgId'
      }))
    };

    nativeBridge = {
      onActivateWinAlerts: jasmine.createSpy(),
      onEventAlertsClick: jasmine.createSpy(),
      showFootballAlerts: jasmine.createSpy()
    };

    window = {
      nativeWindow: {
        NativeBridge: { pushNotificationsEnabled: true }
      }
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue(undefined)
    };
    gtmService = {
      push: jasmine.createSpy()
    };

    fiveASideContestSelectionService = {
      defaultSelectedContest: jasmine.createSpy('defaultSelectedContest')
    };
    freeBetsService = {
      store: jasmine.createSpy('store'),
      getFreeBetsState: jasmine.createSpy('getFreeBetsState').and.returnValue({
        availble: true, 
        data: [{ freebetTokenId: 123 }, { freebetTokenId: 143 }],
        betTokens: [{ freebetTokenId: 56 }, { freebetTokenId: 78 }],
        fanZone:[{ freebetTokenId: 34 }, { freebetTokenId: 92 }],
      })
    };
    locale = {
      getString: jasmine.createSpy().and.callFake(() => 'HL')
    } as any;
    firstBetGAService = new FirstBetGAService(gtmService);
    firstBetGAService = {
      setGtmData: jasmine.createSpy('setGtmData'),
    };
    sessionStorage = {
      get: jasmine.createSpy('get').and.callFake(() => true)
    }

    betReuseService = {
      reuseQuickBet: jasmine.createSpy('reuseQuickBet')
    }

    component = new QuickbetReceiptComponent(
      userService,
      filtersService,
      quickbetService,
      nativeBridge,
      window,
      pubSubService,
      http,
      storageService,
      racingPostTipService,
      cmsService,
      fiveASideEntryConfirmationService,
      fiveASideContestSelectionService,
      freeBetsService,
      gtmService,
      maxPayOutErrorService,
      locale,
      firstBetGAService,
      betReuseService,
      sessionStorage,
      bonusSuppressionService
    );

    component.selection = {
      stake: '1.22',
      eventId: '1',
      categoryName: 'football',
      categoryId: '16',
      drilldownTagNames: 'abc_fb'
    } as IQuickbetSelectionModel;

    component.betReceipt = {
      bet: { id: 1 },
      receipt: {
        id: 'test'
      },
      betId: '2345',
      stake: {
        amount: '100',
        freebet: '10',
        stakePerLine: '111',
      },
      legParts: [{
        eventDesc: '',
        marketDesc: '',
        handicap: '',
        outcomeDesc: ''
      }],
      price: {
        priceType: 'test_price',
        priceTypeRef: {
          id: 'GUARANTEED'
        }
      },
      payout: { potential: '99' },
      oddsValue: '1/2'
    } as IQuickbetReceiptDetailsModel;
    component['filtersService']['isGreyhoundsEvent'] = jasmine.createSpy().and.returnValue(false);
  });
  describe('ngOnInit', () => {
  it('ngOnInit', () => {
    spyOn(component, 'filterOutcomeName');
    spyOn(component, 'filterMarketName');
    spyOn(component, 'filterEventName');
    spyOn(component, 'subscribeToFeatured');
    spyOn<any>(component, 'checkMaxPayOut');

    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    jasmine.createSpy('freeBetsStoreUpdate');
    component.ngOnInit();

    expect(component.hasFreebet).toBe(true);
    expect(quickbetService.getOdds).toHaveBeenCalled();
    expect(component.isEachWay).toBe(true);
    expect(filtersService.setCurrency).toHaveBeenCalledTimes(5);
    expect(component.filterOutcomeName).toHaveBeenCalled();
    expect(component.filterMarketName).toHaveBeenCalled();
    expect(component.filterEventName).toHaveBeenCalled();
    expect(component.eachEayTerms).toEqual('Each Way Odds 1/5 Places 1-2-3');
    expect(component.linesPerStake).toEqual('2 Lines at £1 per line');
    expect(component.subscribeToFeatured).toHaveBeenCalled();
  });
});

  it('#getSystemConfiguration should assign the terms and conditions value as null', () =>{
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue({ FiveASideGameLauncher : {}});
    expect(component.termsConditionTag).toBeFalsy();
  });

  it('#getSystemConfiguration should assign the terms and conditions value as null when fiveaside config is not done', () =>{
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue({});
    expect(component.termsConditionTag).toBeFalsy();
  });

  it('#checkEntryConfirmationLegs should check bet has 5 legs', () => {
    spyOn(component as any, 'getEntryConfirmationDetails');
    component.selection = new BYBBet({
      dashboardData: {
        selections: [1,2,3,4,5],
        game: { title: '|A| |vs| |B|' }
      }
    }) as any;
    component['checkEntryConfirmationLegs']();
    expect(component['getEntryConfirmationDetails']).toHaveBeenCalled();

  });

  it('#checkEntryConfirmationLegs should check bet has 5 legs and do not call', () => {
    spyOn(component as any, 'getEntryConfirmationDetails');
    component['checkEntryConfirmationLegs']();
    expect(component['getEntryConfirmationDetails']).not.toHaveBeenCalled();
  });

  it('#checkEntryConfirmationLegs should check bet has 5 legs and do not call', () => {
    spyOn(component as any, 'getEntryConfirmationDetails');
    component.selection = undefined;
    component['checkEntryConfirmationLegs']();
    expect(component['getEntryConfirmationDetails']).not.toHaveBeenCalled();
  });

  it('should init eachWayTerms only if selection is each Way', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    component.betReceipt.stake.stakePerLine = component.betReceipt.stake.amount = '100';
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();

    expect(component.isEachWay).toBe(false);
    expect(filtersService.setCurrency).toHaveBeenCalledTimes(5);
    expect(component.eachEayTerms).toBeUndefined();
  });

  it('should toggleWinAlerts onInit if enabled', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    storageService.get.and.returnValue(true);
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    expect(storageService.set).toHaveBeenCalledWith('winAlertsEnabled', true);
  });

  it('ngOnDestroy should call native bridge', () => {
    component.winAlertsBet = '111';
    component.ngOnDestroy();

    expect(nativeBridge.onActivateWinAlerts).toHaveBeenCalled();
  });
  it('ngOnDestroy should call native bridge', () => {
    component.ngOnDestroy();

    expect(nativeBridge.onActivateWinAlerts).not.toHaveBeenCalled();
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

  describe('#setSportIcon', () => {
    it('cmsConfig and betReceipt as null', () => {
      cmsService.getSystemConfig.and.returnValue(of(null));
      component.selection = null;
      component.setSportIcon();
      expect(component.isSportIconEnabled).toBeFalse;
    });
    it('CelebratingSuccess as null', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: null}));
      component.selection = {categoryId: '21'} as any;
      component.setSportIcon();
      expect(component.isSportIconEnabled).toBeFalse;
    });
    it('displaySportIcon as null', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: null}}));
      component.selection = {categoryId: '21'} as any;
      component.setSportIcon();
      expect(component.isSportIconEnabled).toBeFalse;
    });
    it('generic icon', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: ['quickbet']}}));
      component.selection = {categoryId: '21'} as any;
      cmsService.getItemSvg.and.returnValue(of({}));
      component.setSportIcon();
      expect(component.sportIconSvgId).toBe('icon-generic');
    });
    it('5-a-side icon', () => {
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: ['quickbet']}}));
      component.selection = {categoryId: '21'} as any;
      component.bybSelectionType = "5-A-Side";
      cmsService.getItemSvg.and.returnValue(of({}));
      component.setSportIcon();
      expect(component.sportIconSvgId).toBe('5-a-side');
    });
  });
  describe('getStake', () => {
    it('should return stake with currency', () => {
      filtersService.setCurrency = jasmine.createSpy().and.returnValue('5$');
      const result = component.getStake('5');

      expect(filtersService.setCurrency).toHaveBeenCalled();
      expect(result).toBe('5$');
    });

    it('should not return stake with currency', () => {
      filtersService.setCurrency = jasmine.createSpy().and.returnValue('5$');
      const result = component.getStake(null);

      expect(filtersService.setCurrency).not.toHaveBeenCalled();
      expect(result).toBe('');
    });
  });

  it('toggleWinAlerts should set win alert bet id', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id: '111' }
    } as IQuickbetReceiptDetailsModel;
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    expect(!component.winAlertsReceiptId).toBeTruthy();
    component.toggleWinAlerts(receipt, true);
    expect(component.winAlertsReceiptId).toBe('111');
    expect(component.winAlertsBet).toBe('111');
    expect(userService.set).toHaveBeenCalledWith({ winAlertsToggled: true });
  });

  it('toggleWinAlerts should remove win alert bet id', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id: '111' }
    } as IQuickbetReceiptDetailsModel;
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    component.toggleWinAlerts(receipt, false);

    expect(component.winAlertsBet).toBeNull();
    expect(storageService.set).toHaveBeenCalledWith('winAlertsEnabled', false);
  });

  it('toggleWinAlerts should not call user set and set win alerts receipt id', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id: '111' }
    } as IQuickbetReceiptDetailsModel;
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    component['user'] = {
      winAlertsToggled: true,
    } as any;
    component.toggleWinAlerts(receipt, true);

    expect(component.winAlertsReceiptId).toBe('111');
    expect(component.winAlertsBet).toBe('111');
    expect(userService.set).not.toHaveBeenCalled();
    expect(storageService.set).toHaveBeenCalledWith('winAlertsEnabled', true);
  });

  it('toggleWinAlerts with winAlertsReceiptId', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id: '111' }
    } as IQuickbetReceiptDetailsModel;
    component.winAlertsReceiptId = '111';
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    component['user'] = {
      winAlertsToggled: true,
    } as any;
    component.toggleWinAlerts(receipt, true);
    expect(component.winAlertsBet).toBe('111');
    expect(userService.set).not.toHaveBeenCalled();
  });

  it('toggleWinAlerts should not call any action', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id: '111' }
    } as IQuickbetReceiptDetailsModel;
    window.nativeWindow.NativeBridge.pushNotificationsEnabled = false;
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    component.toggleWinAlerts(receipt, true);

    expect(component.winAlertsBet).toBeUndefined();
  });

  it('toggleWinAlerts should set winAlertsBet value as receiptId', () => {
    jasmine.createSpy('freeBetsStoreUpdate');
    const receipt = {
      receipt: { id : '111'}
    } as IQuickbetReceiptDetailsModel ;
    spyOn(component, 'sendRacingPostByUpcell');
    component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
    component.ngOnInit();
    component['user'] = {
      winAlertsToggled: true
    } as any;
    component['winAlertsReceiptId'] = '345';
    component.toggleWinAlerts(receipt, true);

    expect(component.winAlertsBet).toBe('111');
    expect(userService.set).not.toHaveBeenCalled();
  });

  describe('#showWinAlertsTooltip', () => {
    it('showWinAlertsTooltip should be true', () => {
      const result = component.showWinAlertsTooltip();
      expect(result).toBeTruthy();
    });
    it('showWinAlertsTooltip should be false', () => {
      storageService.get = jasmine.createSpy('').and.returnValue({ 'receiptViewsCounter-test': 2 });
      const result = component.showWinAlertsTooltip();
      expect(result).toBeFalsy();
    });
  });

  describe('getPotentialPayoutValue', () => {
    it('payout: "200$" returns "200$" ', () => {
      expect(component.getPotentialPayoutValue('200$')).toEqual('200$');
    });

    it('payout: "" returns "N/A" ', () => {
      expect(component.getPotentialPayoutValue('')).toEqual('N/A');
    });

    it('payout: undefined returns "N/A"', () => {
      expect(component.getPotentialPayoutValue(undefined)).toEqual('N/A');
    });
  });

  describe('filterEventName', () => {
    it('empty string case" ', () => {
      component.betReceipt = {};
      component.selection = undefined;
      component.clearName = jasmine.createSpy();
      component.filterEventName();
      expect(component.clearName).toHaveBeenCalledWith('');
    });

    it('non-empty string', () => {
      component.selection = undefined;
      component.betReceipt = {
        legParts: [{
          eventDesc: 'one'
        }, {}]
      } as any;
      component.clearName = jasmine.createSpy();
      component.filterEventName();
      expect(component.clearName).toHaveBeenCalledWith('one');
    });

    it('filterEventName (virtual)', () => {
      component.selection = <any>{
        categoryName: 'Virtual Sports',
        eventName: 'test event'
      };
      component.betReceipt = <any>{
        legParts: [{
          eventDesc: 'one'
        }, {}]
      };
      expect(component.filterEventName()).toEqual('test event');
    });

    it('exclude extra place icon rom unnamed favourites', () => {
      component.selection = <any>{
        isUnnamedFavourite: true,
        categoryName: 'Virtual Sports',
        eventName: 'test event'
      };

      expect(component.getExcludedDrillDownTagNames()).toEqual('MKTFLAG_EPR,EVFLAG_EPR');

      component.selection = <any>{
        isUnnamedFavourite: false,
        categoryName: 'Virtual Sports',
        eventName: 'test event'
      };

      expect(component.getExcludedDrillDownTagNames()).toEqual('');
    });

  });

  describe('filterMarketName', () => {
    it('betReceipt.legParts.length = 2 ', () => {
      component.betReceipt = {
        legParts: [{
          eventDesc: 'one',
          marketDesc: 'one1',
          outcomeDesc: 'one2',
        }, {
          eventDesc: 'two',
          marketDesc: 'two1',
          outcomeDesc: 'two2',
        }]
      } as any;
      component.clearName = jasmine.createSpy();
      component.filterMarketName();
      expect(filtersService.filterAddScore).toHaveBeenCalledTimes(2);
      expect(component.clearName).toHaveBeenCalledTimes(2);
    });
  });

  describe('filterOutcomeName', () => {
    it('betReceipt.legParts.length = 2 + handicap', () => {
      component.betReceipt = {
        legParts: [{
          eventDesc: 'one',
          outcomeDesc: 'outcomeDesc',
          handicap: 'handicap'
        }, {
          eventDesc: 'two',
          outcomeDesc: 'outcomeDesc'
        }]
      } as any;
      component.clearName = jasmine.createSpy();
      component.filterOutcomeName();
      expect(component.betReceipt.legParts[0].handicap).toBeTruthy();
      expect(component.betReceipt.legParts[1].handicap).toBeFalsy();
      expect(filtersService.filterPlayerName).toHaveBeenCalledTimes(2);
      expect(component.clearName).toHaveBeenCalledTimes(2);
    });
  });

  it('clearName(name string) with symbols to be replaced', () => {
    expect(component.clearName('|,string,|')).toEqual('string');
  });

  describe('isEachWayBet', () => {
    it('stake.stakePerLine !== stake.amount', () => {
      const stake = {
        amount: '200',
        stakePerLine: '10'
      };
      expect(component.isEachWayBet(stake)).toEqual(true);
    });
    it('stake.stakePerLine === stake.amount', () => {
      const stake = {
        amount: '10',
        stakePerLine: '10'
      };
      expect(component.isEachWayBet(stake)).toEqual(false);
    });
  });

  it('getOdds, price: {priceDec: 200}', () => {
    component.getOdds({ priceDec: 200 });
    expect(quickbetService.getOdds).toHaveBeenCalledWith({ priceDec: 200 });
  });

  it('setCurrency, val: "val"', () => {
    component.setCurrency('val');
    expect(filtersService.setCurrency).toHaveBeenCalledWith('val', '$');
  });

  describe('oddsValue', () => {
    it('oddsValue returns bet receipt odds value', () => {
      expect(component.oddsValue).toBe('1/2');
    });

    it('oddsValue returns yc odds value', () => {
      component.ycOddsValue = () => '1.2';
      expect(component.oddsValue).toBe('1.2');
    });
  });


  it('should filter outcome name with handicap value', () => {
    filtersService.filterPlayerName.and.returnValue('tie');
    component.betReceipt.legParts = [{
      eventDesc: 'Man City v Watford"',
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'tie',
      outcomeId: '955100247',
      handicap: '+2.0'
    }];
    component.selection = {markets:[{outcomes:[{outcomeMeaningMajorCode: 'AH'}]}]} as any;
    const actualResult = component.filterOutcomeName();

    expect(filtersService.filterPlayerName).toHaveBeenCalledWith('tie');
    expect(actualResult).toEqual('tie (+2.0)');
  });

  it('should filter outcome name with handicap value no outcomes', () => {
    filtersService.filterPlayerName.and.returnValue('tie');
    component.betReceipt.legParts = [{
      eventDesc: 'Man City v Watford"',
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'tie',
      outcomeId: '955100247',
      handicap: '+2.0'
    }];
    component.selection = {} as any;
    const actualResult = component.filterOutcomeName();

    expect(filtersService.filterPlayerName).toHaveBeenCalledWith('tie');
    expect(actualResult).toEqual('tie (+2.0)');
  });
  
  it('should filter outcome name without handicap value', () => {
    filtersService.filterPlayerName.and.returnValue('Man City');
    component.betReceipt['legParts'] = [{
      eventDesc: 'Man City v Watford"',
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'Man City',
      outcomeId: '955100247',
      handicap: '+2.0'
    }] as any;

    component.selection = { markets: [{ outcomes: [{ outcomeMeaningMajorCode: 'HL' }] }] } as any;
    const actualResult = component.filterOutcomeName();

    expect(filtersService.filterPlayerName).toHaveBeenCalledWith('Man City');
    expect(actualResult).toEqual('Man City (2.0)');
  });

  it('should filter market name', () => {
    filtersService.filterAddScore.and.returnValue('Handicap Match Result - Man City');
    component.betReceipt.legParts = [{
      eventDesc: 'Man City v Watford"',
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'Man City',
      outcomeId: '955100247',
    }];

    const actualResult = component.filterMarketName();

    expect(filtersService.filterAddScore).toHaveBeenCalledWith('Handicap Match Result - Man City +2.0 goals', 'Man City');
    expect(actualResult).toEqual('Handicap Match Result - Man City');
  });

  it('should filter event name', () => {
    component.selection = undefined;
    component.betReceipt.legParts = [{
      eventDesc: 'Man City v Watford"',
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'Man City',
      outcomeId: '955100247',
    }];

    const actualResult = component.filterEventName();

    expect(actualResult).toEqual('Man City v Watford"');
  });

  it('should filter event name with default eventDesc', () => {
    component.selection = undefined;
    component.betReceipt.legParts = [{
      marketDesc: 'Handicap Match Result - Man City +2.0 goals',
      outcomeDesc: 'Man City',
      outcomeId: '955100247',
    }] as any;

    const actualResult = component.filterEventName();

    expect(actualResult).toEqual('');
  });

  it('should return potential payout value', () => {
    const actualResult = component.getPotentialPayoutValue('1.0');

    expect(actualResult).toEqual('1.0');
  });

  it('should return N/A when no potential payout value were found', () => {
    const actualResult = component.getPotentialPayoutValue(null);

    expect(actualResult).toEqual('N/A');
  });

  describe('#getEWTerms', () => {
    it('should call getEWTerms method', () => {
      component.getEWTerms({} as any);

      expect(quickbetService.getEWTerms).toHaveBeenCalledWith({});
    });
  });

  describe('#getLinesPerStake', () => {
    it('should call getLinesPerStake method', () => {
      component.getLinesPerStake({} as any);

      expect(quickbetService.getLinesPerStake).toHaveBeenCalledWith({});
    });
  });

  describe('Should check isBogEnabled', () => {
    it('should call isBogFromPriceType()', () => {
      expect(component.isBogFromPriceType()).toBe(true);
    });

    it('should call isBogFromPriceType() with facke value of priceTypeRef id and should check isBogEnabled', () => {
      jasmine.createSpy('freeBetsStoreUpdate');
      component.betReceipt = {
        ...component.betReceipt,
        price: {
          priceType: 'test_price',
          priceTypeRef: {
            id: 'SP'
          }
        },
      } as any;
      spyOn(component, 'sendRacingPostByUpcell');
      component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
      component.ngOnInit();

      expect(component.isBogFromPriceType()).toBe(false);
      expect(component.isBogEnabled).toBe(false);
    });

    it('should check isBogEnabled when isBogFromPriceType() = false', () => {
      jasmine.createSpy('freeBetsStoreUpdate');
      component.isBogFromPriceType = jasmine.createSpy('isBogFromPriceType').and.returnValue(false);
      spyOn(component, 'sendRacingPostByUpcell');
      component['initRacingPostTip'] = jasmine.createSpy('initRacingPostTip');
      component.ngOnInit();

      expect(component.isBogEnabled).toBe(false);
    });
  });

  describe('setBybData', () => {
    it('should set byb data', () => {
      component.selection = new BYBBet({
        dashboardData: {
          game: { title: '|A| |vs| |B|' }
        }
      }) as any;
      component['setBybData']();
      expect(component.bybEventName).toBe('A vs B');
      expect(quickbetService.getBybSelectionType).toHaveBeenCalled();
    });

    it('should set byb data', () => {
      component.selection = {} as any;
      component['setBybData']();
      expect(component.bybEventName).toBeUndefined();
      expect(quickbetService.getBybSelectionType).not.toHaveBeenCalled();
    });
  });

  describe('Close quickbet mode;', () => {
    it('should emit closeQuickbetPanel', () => {
      spyOn(component.closeQuickbetPanel, 'emit');
      component.onQuickbetEvent();
      expect(component.closeQuickbetPanel.emit).toHaveBeenCalled();
    });
  });

  describe('sendRacingPostByUpcell', () => {
    it('should make unsuccessful request with params', () => {
      component['_racingPostTip'] = {
        'startTime': '2020-12-28T09:13:09Z',
        'eventId': '12345',
        'categoryId': '18'
      } as any;
      component.sendRacingPostByUpcell(true);
      expect(quickbetService.readUpCellBets).not.toHaveBeenCalled();
    });
    it('should make a successful request with params', () => {
      component['_racingPostTip'] = {
        'startTime': '2020-12-28T09:13:09Z',
        'eventId': '12345',
        'categoryId': '21'
      } as any;
      component.sendRacingPostByUpcell(true);
      expect(quickbetService.readUpCellBets).toHaveBeenCalled();
    });
  });

  describe('initRacingPostTip', () => {
    it('#initRacingPostTip should not subscribe for racingpost data', () => {
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: false
      };
      component.selection.categoryId = '16';
      component['sendRacingPostByUpcell'] = jasmine.createSpy('sendRacingPostByUpcell');
      component['initRacingPostTip']();
      expect(component.sendRacingPostByUpcell).not.toHaveBeenCalled();
    });
    it('#initRacingPostTip should subscribe for racingpost data', () => {
      component.selection.categoryId = '21';
      component.racingPostToggle = {
        enabled: false,
        mainBetReceipt: true,
        quickBetReceipt: true
      };
      component['sendRacingPostByUpcell'] = jasmine.createSpy('sendRacingPostByUpcell');
      component['initRacingPostTip']();
      expect(component.sendRacingPostByUpcell).toHaveBeenCalledWith(false);
    });
    it('#initRacingPostTip should subscribe for racingpost data', () => {
      component.selection.categoryId = '21';
      component.racingPostToggle = {
        enabled: true,
        mainBetReceipt: true,
        quickBetReceipt: true
      };
      component['sendRacingPostByUpcell'] = jasmine.createSpy('sendRacingPostByUpcell');
      component['initRacingPostTip']();
      expect(component.sendRacingPostByUpcell).toHaveBeenCalledWith(true);
    });
  });
  it('onRacingPostGTMEvent', () => {
    racingPostTipService = {
      racingPostGTM: jasmine.createSpy('racingPostGTM')
    };
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
  describe('#getEntryConfirmationDetails', () => {
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and
        .returnValue(of({ 'showdown': false, 'ecText': '', 'contestId': '' }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = {};
      fiveASideContestSelectionService.defaultSelectedContest = 'contestpresent';
      component['getEntryConfirmationDetails'](selection);
      expect(component.showEntryConfirmation.showdown).toBe(false);
    });
    it('should not set Five A Side ShowDown details, if selections length is less than 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and
        .returnValue(of({ 'showdown': false, 'ecText': '', 'contestId': '' }));
      const selection = new BYBBet(THREESELECTIONSWITHF) as any;
      selection.freebet = { id: '123345' };
      component['getEntryConfirmationDetails'](selection);
      expect(fiveASideEntryConfirmationService.getShowdownConfirmationDisplay).not.toHaveBeenCalled();
    });
    it('should not set Five A Side ShowDown, if default contest not selected', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and
        .returnValue(of({ 'showdown': false, 'ecText': '', 'contestId': '' }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = {};
      fiveASideContestSelectionService.defaultSelectedContest = null;
      component['getEntryConfirmationDetails'](selection);
      expect(fiveASideEntryConfirmationService.getShowdownConfirmationDisplay).not.toHaveBeenCalled();
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = {};
      fiveASideContestSelectionService.defaultSelectedContest = 'contestpresent';
      component['getEntryConfirmationDetails'](selection);
      expect(component.showEntryConfirmation.showdown).toBe(true);
      expect(fiveASideContestSelectionService.defaultSelectedContest).toEqual(null);
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHE) as any;
      selection.freebet = {};
      component['getEntryConfirmationDetails'](selection);
      expect(fiveASideEntryConfirmationService.getShowdownConfirmationDisplay).not.toHaveBeenCalled();
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHE) as any;
      selection.freebet = false;
      component['getEntryConfirmationDetails'](selection);
      expect(fiveASideEntryConfirmationService.getShowdownConfirmationDisplay).not.toHaveBeenCalled();
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHE) as any;
      selection.freebet = { id: '123345' };
      component['getEntryConfirmationDetails'](selection);
      expect(fiveASideEntryConfirmationService.getShowdownConfirmationDisplay).not.toHaveBeenCalled();
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = { id: '' };
      fiveASideContestSelectionService.defaultSelectedContest = 'contestpresent';
      component['getEntryConfirmationDetails'](selection);
      expect(component.showEntryConfirmation.showdown).toBe(true);
      expect(fiveASideContestSelectionService.defaultSelectedContest).toEqual(null);
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = { id: '123345' };
      fiveASideContestSelectionService.defaultSelectedContest = 'contestpresent';
      component['getEntryConfirmationDetails'](selection);
      expect(component.showEntryConfirmation.showdown).toBe(true);
    });
    it('should not set Five A Side ShowDown, if both conditions does not satisfy when selections length is 5', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(of({ 'showdown': true }));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = { id: '' };
      fiveASideContestSelectionService.defaultSelectedContest = 'contestpresent';
      component['getEntryConfirmationDetails'](selection);
      expect(component.showEntryConfirmation.showdown).toBe(true);
    });
    it('should throw error for invalid response in getentry confirmation details', () => {
      fiveASideEntryConfirmationService.getShowdownConfirmationDisplay.and.returnValue(observableThrowError('no data'));
      const selection = new BYBBet(FIVESELECTIONSWITHF) as any;
      selection.freebet = { id: '' };
      component['getEntryConfirmationDetails'](selection);
    });
  });
  describe('checkMaxPayOut', () => {
    it('if max payout true', () => {
      spyOn(component, 'sendGTMData');
      component.betReceipt = { betTags: { betTag: [{ tagName: 'CAPPED', tagValue: "" }] } };
      component['checkMaxPayOut']();
      expect(component.maxPayOutFlag).toBe(true);
    });
    it('if max payout false when no bet tags', () => {
      spyOn(component, 'sendGTMData');
      component.betReceipt = {};
      component['checkMaxPayOut']();
      expect(component.maxPayOutFlag).toBe(false);
    });
    it('if max payout false when no tag name', () => {
      spyOn(component, 'sendGTMData');
      component.betReceipt = { betTags: { betTag: [{ tagName: '', tagValue: "" }] } };
      component['checkMaxPayOut']();
      expect(component.maxPayOutFlag).toBe(false);
    });
  });
  describe('togglemaxPayedOut', () => {
    it('togglemaxPayedOut - false', () => {
      component.isMaxPayedOut = false;
      spyOn<any>(component,'sendGTMData');
      component['togglemaxPayedOut']();
      expect(component.sendGTMData).toHaveBeenCalled();
    });

    it('togglemaxPayedOut - true', () => {
      component.isMaxPayedOut = true;
      spyOn<any>(component,'sendGTMData');
      component['togglemaxPayedOut']();
      expect(component.sendGTMData).not.toHaveBeenCalled();
    });
  });
  it('sendGTMData', () => {
    component['sendGTMData']('click');
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('#enableRacingPostTip', () => {
    it('should return value as true', () => {
      component['racingPostToggle'] = {enabled: true, quickBetReceipt:true, mainBetReceipt: true};
      component['isNextRacesData'] = false;
      const flag = component.enableRacingPostTip();
      expect(flag).toEqual(true);
    });
    it('should return value as false', () => {
      component['racingPostToggle'] = {enabled: false, quickBetReceipt:true, mainBetReceipt: true};
      component['isNextRacesData'] = false;
      const flag = component.enableRacingPostTip();
      expect(flag).toEqual(false);
    });
  });

  describe('#freeBetsStoreUpdate', () => {
    it('should call freeBetsStoreUpdate method with freebet ID', () => {
      component['freeBetsStoreUpdate']({freebetId: 123} as any);
      expect(freeBetsService.store).toHaveBeenCalledWith('test', 
      {data: [{ freebetTokenId: 143 },
        { freebetTokenId: 56 },
        { freebetTokenId: 78 }, { freebetTokenId: 34 },
        { freebetTokenId: 92 }]});
    });
    it('should call freeBetsStoreUpdate method without freebet', () => {
      component['freeBetsStoreUpdate']({freebetId: null} as any);
      expect(freeBetsService.store).not.toHaveBeenCalled();
    });
  });

  describe('#appendDrillDownTagNames', () => {
    it('should return true for appendDrillDownTagName', () => {
      locale.getString.and.returnValue('Match Result');
      const returnValue = component.appendDrillDownTagNames({marketName: 'Match Result'});
      expect(returnValue).toEqual('Match Result,');
    });

    it('should return empty string  for appendDrillDownTagName', () => {
      locale.getString.and.returnValue(undefined);
      const returnValue = component.appendDrillDownTagNames({marketName: ''});
      expect(returnValue).toEqual('');
    });
  });

  describe('#reuseBets;', () => {
    it('should call reuse and emit closeQuickbetPanel', () => {
      spyOn(component.closeQuickbetPanel, 'emit');
      component.reuseBets();
      expect(betReuseService.reuseQuickBet).toHaveBeenCalled();
      expect(component.closeQuickbetPanel.emit).toHaveBeenCalled();
    });
  });

  describe('subscribeToFeatured', () => {
    beforeEach(() => {
      component.selection = {
        stake: '1.22',
        eventId: '1',
        categoryName: 'football',
        markets: [{outcomes: [{id: 1}]}],
        categoryId: '16',
        drilldownTagNames: 'abc_fb'
      } as IQuickbetSelectionModel;
    });
    it('should detect changes (OUTCOME_UPDATED)', () => {
      component.showReuse = true;
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb());
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(true);
    });

    it('should check resue if no update from selcn or event', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb({ update: {type: 'PRICE', event: {eventId: 1, market: {outcome: {displayed: 'Y', status: 'A'}}}} }));
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(true);
    });

    it('should check resue if selection is active', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb({ update: {type: 'SELCN', event: {eventId: 1, market: {outcome: {outcomeId: 1, displayed: 'Y', status: 'A'}}}} }));
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(true);
    });

    it('should check resue if event is active', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb({ update: {type: 'EVENT', event: {eventId: 1, displayed: 'Y', status: 'A'}} }));
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(true);
    });

    it('should check resue if selection is in-active', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb({ update: {type: 'SELCN', event: {eventId: 1, market: {outcome: {outcomeId: 1, displayed: 'Y', status: 'S'}}}} }));
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(false);
    });

    it('should check resue if market is in-active', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'WS_EVENT_UPDATE' && cb({ update: {type: 'EVENT', event: {eventId: 1, displayed: 'Y', status: 'S'}}}));
      component['subscribeToFeatured']();
      expect(component.showReuse).toBe(false);
    });
  });
  describe('GTM', () => {
    it('onFootballBellClick', () => {
      const selection = component.selection;
      spyOn<any>(component, 'sendGTMMatchAlertClick').and.callThrough();
      component['onFootballBellClick']();
      expect(nativeBridge['onEventAlertsClick']).toHaveBeenCalledWith(selection.eventId,
        selection.categoryName.toLocaleLowerCase(),
        selection.categoryId,
        selection.drilldownTagNames,
        ALERTS_GTM.QUICK_BET);
      expect(component['sendGTMMatchAlertClick']).toHaveBeenCalledWith();
    });
    it('handleAlertInfoClick', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': ALERTS_GTM.NA,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
      };
      component['handleAlertInfoClick']();
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData);
    });
    it('sendGTMWinAlertToggle - enabled - false', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.TOGGLE_OFF,
        'component.PositionEvent': ALERTS_GTM.QUICK_BET,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT
      };
      component['sendGTMWinAlertToggle'](false);
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData);
    });
    it('sendGTMMatchAlertClick - enabled - false', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': ALERTS_GTM.QUICK_BET,
        'component.EventDetails': ALERTS_GTM.MATCH_ALERT_ICON
      };
      component['sendGTMMatchAlertClick']();
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData);
    });
  });
});
