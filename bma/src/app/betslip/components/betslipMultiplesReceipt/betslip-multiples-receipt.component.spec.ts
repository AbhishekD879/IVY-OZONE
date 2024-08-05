import { BetslipMultiplesReceiptComponent } from './betslip-multiples-receipt.component';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { of } from 'rxjs';

describe('BetslipMultiplesReceiptComponent', () => {
  let component: BetslipMultiplesReceiptComponent;
  let nativeBridge;
  let userService;
  let betReceiptService;
  let storageService;
  let localeService;
  let cmsService;
  let betInfoDialogService;
  let gtmService;
 
  const excludedDrillDownTagNames = 'DrillDownTagNames or Empty string';

  const multiplesReceipts = [{
    leg: [{ part: [{ isFootball: true, description: 'unnamed favourite', event: {categoryId: 1}}] }, { part: [{ isFootball: true }] }]
  }, {
    leg: [{ part: [{ isFootball: false, description: 'Unnamed 2nd Favourite', event: {categoryId: 1} }] }, { part: [{ isFootball: false }] }]
  }, {
    leg: [{ part: [{ isFootball: true }] }, { part: [{ isFootball: false }] }]
  }];

  const receipts = [{
    isFavouriteAvailable: true,
    stakeValue: 5,
    leg: [
      {
        excludedDrillDownTagNames: excludedDrillDownTagNames,
        part: [{ isFootball: true, description: 'unnamed favourite', event: {categoryId: 1}}],
        svgId: 'svgId'
      },
      {
        part: [{ isFootball: true }]
      }
     ]
  }, {
    isFavouriteAvailable: false,
    stakeValue: 5,
    leg: [
      {
        excludedDrillDownTagNames: excludedDrillDownTagNames,
        part: [{ isFootball: false, description: 'Unnamed 2nd Favourite', event: {categoryId: 1} }],
        svgId: 'svgId'
      },
      {
        part: [{ isFootball: false }]
      }
     ]
  }, {
    isFavouriteAvailable: true,
    stakeValue: 5,
    leg: [
      { part: [{ isFootball: true }] },
      { part: [{ isFootball: false }] }
     ]
  }];

  beforeEach(() => {
    nativeBridge = {};
    userService = {
      oddsFormat: 'frac',
      currencySymbol: '$',
      receiptViewsCounter: 5,
      winAlertsToggled: false,
      username: 'test'
    };

    betReceiptService = {
      hasStakeMulti: () => { },
      getStakeMulti: () => { },
      getStakeTotal: () => { },
      setToggleSwitchId: () => { },
      getEWTerms: () => { },
      getLinesPerStake: () => { },
      getReceiptOdds: () => { },
      isBetSlipShown: true,
      returnAllWinner: jasmine.createSpy('returnAllWinner').and.returnValue('1'),
      getFormattedPrice: jasmine.createSpy('getFormattedPrice').and.returnValue('0.5/1'),
      getExcludedDrillDownTagNames: jasmine.createSpy('getExcludedDrillDownTagNames').and.returnValue(excludedDrillDownTagNames),
      luckyAllWinnersBonus:jasmine.createSpy('luckyAllWinnersBonus').and.returnValue('')
    };

    storageService = {
      get: jasmine.createSpy('get').and.returnValue(undefined)
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('Match Result')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };
    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(of({
        svg: 'svg',
        svgId: 'svgId'
      })),
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!",
          displaySportIcon: ["openbets", "settledbets", "cashoutbets", "betreceipt", "edpmybets"]
        }
      }))
    };
    betInfoDialogService={
      multiple:jasmine.createSpy('multiple')
    }

    component = new BetslipMultiplesReceiptComponent(
      nativeBridge,
      userService,
      betReceiptService,
      storageService,
      localeService,
      gtmService,
      cmsService,
      betInfoDialogService   
    );
  });
  
  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.currencySymbol).toEqual('$');
    expect(component.hasStakeMulti).toEqual(jasmine.any(Function));
    expect(component.getStakeMulti).toEqual(jasmine.any(Function));
    expect(component.getStakeTotal).toEqual(jasmine.any(Function));
    expect(component.getEWTerms).toEqual(jasmine.any(Function));
    expect(component.getLinesPerStake).toEqual(jasmine.any(Function));
    expect(component.setToggleSwitchId).toEqual(jasmine.any(Function));
    expect(component.getOdds).toEqual(jasmine.any(Function));
  });

  describe('#trackByIndex', () => {
    it('should call trackByIndex and track by index and leg #', () => {
      expect(component.trackByIndex(2, { legNo: 20 } as any)).toEqual('2_20');
    });
  });

   describe('ngOnInit', () => {
     it('should call ngOnInit and modify multiples receipt with stakeValue', () => {
       component.getStakeMulti = () => 5;
       component.multiReceipts = JSON.parse(JSON.stringify((multiplesReceipts)));
       component.ngOnInit();

       expect(component.multiReceipts).toEqual(receipts as any);
    });
    it('should set generic svg', () => {
      component.getStakeMulti = () => 5;
      component.multiReceipts = [{
        leg: [{ part: [{event: {categoryId: 1}}], svgId: null }],
      }] as any;
      cmsService.getItemSvg = jasmine.createSpy('getItemSvg').and.returnValue(of({svg: 'svg'}));
      component.ngOnInit();
    });
    it('ngOnInit with cms config as null', () => {
      component.multiReceipts = [{
        leg: [{ part: [{event: null}], svgId: null }],
      }] as any;
      cmsService.getSystemConfig.and.returnValue(of(null));
      component.ngOnInit();
    });
    it('ngOnInit with cms config CelebratingSuccess as null', () => {
      component.multiReceipts = [{
        leg: [{ part: [{event: null}], svgId: null }],
      }] as any;
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: null}));
      component.ngOnInit();
    });
    it('ngOnInit with cms config displaySportIcon as undefined', () => {
      component.multiReceipts = [{
        leg: [{ part: [{event: null}], svgId: null }],
      }] as any;
      cmsService.getSystemConfig.and.returnValue(of({CelebratingSuccess: {displaySportIcon: undefined}}));
      component.ngOnInit();
      expect(component.isSportIconEnabled).not.toBeTrue();
    });
  });

  describe('#showWinAlertsTooltip', () => {
    it('should call showWinAlertsTooltip when receiptViewsCounter less or equal MAX_VIEWS_COUNT', () => {
      expect(component.showWinAlertsTooltip()).toEqual(true);
      expect(storageService.get).toHaveBeenCalled();
    });

    it('should call showWinAlertsTooltip when receiptViewsCounter less or equal MAX_VIEWS_COUNT', () => {
      storageService.get = jasmine.createSpy().and.returnValue({'receiptViewsCounter-test': 2});
      expect(component.showWinAlertsTooltip()).toEqual(false);
      expect(storageService.get).toHaveBeenCalled();
    });
  });

  describe('#toggleWinAlerts', () => {
    it('should call toggleWinAlerts method and emit winAlertsToggleChanged', () => {
      const receipt = {
        leg: [{ part: [{ eventCategoryId: '16' }] }]} as any;
      component.winAlertsToggleChanged.emit = jasmine.createSpy('winAlertsToggleChanged.emit');

      component.toggleWinAlerts(receipt, true);

      expect(component.winAlertsToggleChanged.emit).toHaveBeenCalledWith({
        receipt,
        state: true
      });
    });
  });

  it('openSelectionMultiplesDialog', () => {
    component.multiReceipts = [
      {
       availableBonuses: {
         availableBonus: []
       },
       betTypeRef : {
         id : 'L15'
       }
      }
 ] as any;
    component.openSelectionMultiplesDialog('lucky','lucky15' );
    expect(betInfoDialogService.multiple).toHaveBeenCalled();
  });
  it('openSelectionMultiplesDialog without label', () => {
    component.multiReceipts = [
      {
       availableBonuses: {
         availableBonus: []
       },
       betTypeRef : {
         id : 'L63'
       }
      }
 ] as any;
    component.openSelectionMultiplesDialog('lucky');
    expect(betInfoDialogService.multiple).toHaveBeenCalled();
  });

  describe('#oddsACCA', () => {
    it('should call oddsACCA method and retrun frac potentialPayout', () => {
      const result = component.oddsACCA({
        potentialPayout: '1/2'
      } as any);

      expect(betReceiptService.getFormattedPrice).toHaveBeenCalledWith({
        potentialPayout: '1/2'
      });
      expect(result).toEqual('0.5/1');
    });

    it('should call oddsACCA method and retrun dec potentialPayout', () => {
      userService.oddsFormat = 'dec';
      betReceiptService.getFormattedPrice.and.returnValue('1.5');
      const result = component.oddsACCA({
        potentialPayout: '1.5'
      } as any);

      expect(result).toEqual('1.5');
    });

    it('should check show oddsACCA condition', () => {
      const receipt = {
        numLines: '1',
        isFCTC: false,
        potentialPayout: '1.5'
      } as any;
      expect(component.showOddsAcca(receipt)).toBeTruthy();
      receipt.isFCTC = true;
      expect(component.showOddsAcca(receipt)).toBeFalsy();
      receipt.numLines = '3';
      expect(component.showOddsAcca(receipt)).toBeFalsy();
      component.oddsACCA = () => 'test';
      expect(component.showOddsAcca(receipt)).toBeFalsy();
    });

    it('should show SP price if all of legs has SP prices', () => {
      const receipt = {
        numLines: '1',
        isFCTC: false,
        leg: [{ odds: { dec: 'SP', frac: 'SP' } }, { odds: { dec: 'SP', frac: 'SP' }}]} as any;
      expect(component.oddsACCA(receipt)).toEqual('SP');
    });

    it('should call oddsACCA method dec', () => {
      betReceiptService.getFormattedPrice.and.returnValue('0.01');
      userService.oddsFormat = 'dec';
      const result = component.oddsACCA({
        potentialPayout: '0.01'
      } as any);

      expect(result).toEqual('0.01');
    });

    it('should call oddsACCA method frac', () => {
      userService.oddsFormat = 'frac';
      const result = component.oddsACCA({
        potentialPayout: '1.5'
      } as any);

      expect(result).toEqual('0.5/1');
    });

    it('should call oddsACCA method sp price', () => {
      const result = component.oddsACCA({
        potentialPayout: 'NOT_AVAILABLE'
      } as any);

      expect(result).toEqual('N/A');
    });

    it('should call oddsACCA method overask', () => {
      const result = component.oddsACCA({
        potentialPayout: 'N/A'
      } as any);

      expect(result).toEqual('N/A');
    });
  });

  describe('set StakeValue, Favourites availability and excluded promo-icons', () => {
    it('should setReceiptsAdditionalData', () => {
      spyOn(component, 'getStakeMulti').and.returnValue(0);
      cmsService.getItemSvg.and.returnValue(of({}));
      component['setReceiptsAdditionalData'](multiplesReceipts as any);
      
      expect(receipts).toEqual(receipts as any );
    });
    it('should setReceiptsAdditionalData', () => {
      spyOn(component, 'getStakeMulti').and.returnValue(1);
      cmsService.getItemSvg.and.returnValue(of({}));
      component['setReceiptsAdditionalData'](multiplesReceipts as any);

      expect(receipts).toEqual(receipts as any );
    });
  });

  
  describe('#appendDrillDownTagNames', () => {
    it('should return true for appendDrillDownTagName', () => {
      const returnValue = component.appendDrillDownTagNames({event: {categoryId:'16'}, eventMarketDesc: 'Match Result'} as any);
      expect(returnValue).toEqual('Match Result,');
    });

    it('should return empty string  for appendDrillDownTagName', () => {
      const returnValue = component.appendDrillDownTagNames({event: {categoryId:'21'}, eventMarketDesc: 'Match Result'} as any);
      expect(returnValue).toEqual('');
    });

    it('should return empty string  for appendDrillDownTagName', () => {
      const returnValue = component.appendDrillDownTagNames({event: {categoryId:'16'}, eventMarketDesc: 'Both Teams to Score'} as any);
      expect(returnValue).toEqual('');
    });
  });
  describe('GTM', () => {
    it('handleAlertInfoClick', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.CLICK,
        'component.PositionEvent': ALERTS_GTM.NA,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT_ICON
      };
      component['handleAlertInfoClick'](receipts[0]  as any);
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, receipts[0] as any);
    });
    it('sendGTMWinAlertToggle - enabled - false', () => {
      spyOn<any>(component, 'sendGTMAlerts').and.callThrough();
      const gtmData = {
        'component.ActionEvent': ALERTS_GTM.TOGGLE_OFF,
        'component.PositionEvent': ALERTS_GTM.BETSLIP,
        'component.EventDetails': ALERTS_GTM.WIN_ALERT
      };
      component['sendGTMWinAlertToggle'](false, receipts[0] as any);
      expect(component['sendGTMAlerts']).toHaveBeenCalledWith(gtmData, receipts[0] as any);
    });
  });

  describe('@sendGtmDataoninfoicon', () => {
  it('#setGATracking', () => {
    component.sendGtmDataoninfoicon('lucky');
    expect(gtmService.push).toHaveBeenCalled();
  });
  }); 
  describe('showLuckySignPostInfoLable', () => {
    it('should return true for info label', () => {
      // component.value = 'L15';
      expect(component['showLuckySignPostInfoLable']('L15')).toBe(true);
      expect(component['showLuckySignPostInfoLable'](null)).toBe(false);
    });
   
     it('should test isCashoutAvailable', () => {
      const result = component.isCashoutAvailable('Y');
      expect(result).toEqual(true);
    });
     it('should test isCashoutAvailable', () => {
      const result = component.isCashoutAvailable(1);
      expect(result).toEqual(true);
    });
  });

  describe('calculateAllWinnerBonus', () => {
    it('should return luckyAllWinnersBonus', () => {
      
      // expect(component.calculateAllWinnerBonus()).toEqual(true);\
      const result = component.calculateAllWinnerBonus();
    //   component.multiReceipts = [{availableBonuses : {availableBonus:[
    //     {
    //         "type": "LUCKYX_CONSOLATION",
    //         "num_win": "1",
    //         "multiplier": "2"
    //     }
         
    // ] }}]
    expect(result).toEqual('');
    });

    it('isShownAllWinner', () => {
      const result = component.isShownAllWinner();
      expect(result).toEqual('1');

    });
    betReceiptService = {
      maxPayOutFlag: true,
      betReceipt: true,
      luckyAllWinnersBonus: () => {return true;},
      returnAllWinner: () => {return 1;},
    }
  
})
});
