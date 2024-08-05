import { BetslipTotalWrapperComponent } from '@app/betslip/components/betslipTotalWrapper/betslip-total-wrapper.component';

describe('BetslipTotalWrapperComponent', () => {
  let component: BetslipTotalWrapperComponent;
  let gtmService, toteBetslipService, betReceiptService,maxPayOutErrorService,filterService,userService;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy()
    };
    betReceiptService = {
      maxPayOutFlag: true,
      betReceipt: true,
      luckyAllWinnersBonus: () => {return 1;},
      returnAllWinner: () => {return 1;},
    }
    toteBetslipService = {
      getToteFreeBetText: () => { return 'getToteFreeBetText'}
    }
    userService = {
      currencySymbol : 'USD'
    }
    component = new BetslipTotalWrapperComponent(gtmService, toteBetslipService, betReceiptService,maxPayOutErrorService,filterService,userService);
  });

  it('on destroy component', () => {
    betReceiptService.maxPayOutFlag = false;
    betReceiptService.betReceipt = false;
    component.ngOnDestroy();
    expect(betReceiptService.maxPayOutFlag).toBe(false);
  });

  describe('isTotalStakeShown', () => {
    it('should be true if there is both free bet and stake', () => {
      component.totalFreeBetsStake = '$1';
      component.totalStake = '$1';
      expect(component.isTotalStakeShown).toBeTruthy();
    });

    it('should be true if there is no free bet', () => {
      component.totalFreeBetsStake = null;
      component.totalStake = '$1';
      expect(component.isTotalStakeShown).toBeTruthy();
    });

    it('should be false when there are no neither free bet nor stake', () => {
      component.totalFreeBetsStake = null;
      component.totalStake = null;
      expect(component.isTotalStakeShown).toBeFalsy();
    });

    it('should be false if there is no stake', () => {
      component.totalFreeBetsStake = '$1';
      component.totalStake = null;
      expect(component.isTotalStakeShown).toBeFalsy();
    });
    it('should be true if it is bet receipt with 0 stake', () => {
      component.totalFreeBetsStake = '$1';
      component.totalStake = '$0';
      component.isBetReceipt = false;
      expect(component.isTotalStakeShown).toBeTruthy();
    });
    it('should be false if it is not bet receipt with 0 stake', () => {
      component.totalFreeBetsStake = '$1';
      component.totalStake = '$0';
      component.isBetReceipt = true;
      expect(component.isTotalStakeShown).toBeFalsy();
    });
  });

  describe('ngOnInit', () => {
    it('calculateAllWinnerBonus', () => {
      expect(component.calculateAllWinnerBonus()).toEqual(1);
    });
    it('isShownAllWinner', () => {
      expect(component.isShownAllWinner()).toEqual(1);
    });
    it('send GTM Data on render', () => {
      spyOn<any>(component,'sendGTMData');
      component.ngOnInit();
      expect(component.sendGTMData).toHaveBeenCalled();
    });
    it('send GTM Data on render', () => {
      spyOn<any>(component,'sendGTMData');
      betReceiptService.maxPayOutFlag = false;
      betReceiptService.betReceipt = false;
      component.ngOnInit();
      expect(component.sendGTMData).not.toHaveBeenCalled();
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
  it('getFreeBetText', () => {
    expect(component.getFreeBetText()).toEqual('getToteFreeBetText');
  });
});
