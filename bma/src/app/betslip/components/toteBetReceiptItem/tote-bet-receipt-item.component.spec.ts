import { ToteBetReceiptItemComponent } from './tote-bet-receipt-item.component';

describe('ToteBetReceiptItemComponent', () => {
  let component: ToteBetReceiptItemComponent;
  let coreToolsService;
  let userService;
  let toteBetslipService;
  let localeService;
  let receipt;

  const toteBet = {
    orderedLegs: [],
    betName: 'Placepot',
    numberOfLines: 5,
    poolName: 'test',
    stakeRestrictions: {
      maxStakePerLine: '1',
      maxTotalStake: '1',
      minStakePerLine: '1',
      minTotalStake: '1',
      stakeIncrementFactor: '1'
    }
  };

  beforeEach(() => {
    coreToolsService = {
      getCurrencySymbolFromISO: jasmine.createSpy()
    };
    userService = {
      currencySymbol: '$'
    };
    toteBetslipService = {
      getTokenValue: jasmine.createSpy('getTokenValue'),
      getRoundedValue: jasmine.createSpy('getRoundedValue'),
      getToteFreeBetText: jasmine.createSpy('getToteFreeBetText')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };

    component = new ToteBetReceiptItemComponent(toteBetslipService, localeService, coreToolsService, userService);
    component.poolCurrencyCode = 'GBP';
    component.toteBet = toteBet;

    component['localeService'].getString = jasmine.createSpy();
    receipt = {
      isFCTC: true,
      numLines: '5',
      stakePerLine: 2,  
      stake: 2,  
    } as any;
  });

  it('should create and init component', () => {
    expect(component).toBeTruthy();
    expect(component.userCurrencySymbol).toEqual('$');
    toteBetslipService.getTokenValue.and.returnValue();
  });

  describe('ngOnInit', () => {
    it('should init non pot bet', () => {
      component.receipts = [receipt];
      component.toteBet.orderedLegs = undefined;
      toteBetslipService.getRoundedValue = (val: string) => {
        return val;
      };
      component.ngOnInit();
      expect(coreToolsService.getCurrencySymbolFromISO).toHaveBeenCalledWith('GBP');
      expect(component.toteBet.isPotBet).toBeFalsy();
    });
    it('should init pot bet', () => {
      component.receipts = [receipt];
      component.toteBet.orderedLegs = [];
      toteBetslipService.getRoundedValue = (val: string) => {
        return val;
      };
      component.ngOnInit();
      expect(coreToolsService.getCurrencySymbolFromISO).toHaveBeenCalledWith('GBP');
      expect(component.toteBet.isPotBet).toBeTruthy();
    });
  });

  describe('#buildLinesTitle', () => {
    it('forcast receipt case for 5 lines', () => {
      component.receipts = [receipt];
      toteBetslipService.getRoundedValue = (val: string) => {
        return val;
      };
      component['buildLinesTitle']();
      expect(component['localeService'].getString).toHaveBeenCalledWith('bs.linesPerStake', {
        lines: '5', stake: '0.40', currency: undefined 
      });
    });
    it('forcast receipt case for 1 line', () => {
      receipt.numLines = '1';
      component.receipts = [receipt];
      toteBetslipService.getRoundedValue = (val: string) => {
        return val;
      };
      component['buildLinesTitle']();
      expect(component['localeService'].getString).toHaveBeenCalledWith('bs.linePerStake', {
         lines: '1', stake: '2.00', currency: undefined 
      });
    });
  });

  it('should call getFreeBetText()', () => {
    expect(component['getFreeBetText']()).toBeUndefined();
  });
});
