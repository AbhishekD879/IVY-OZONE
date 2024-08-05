import { BetslipMultipleBetPartsComponent } from '@betslip/components/betslipMultipleBetPart/betslip-multiple-bet-parts.component';

describe('BetslipMultipleBetPartsComponent', () => {
  let component;
  let userService;
  let fracToDecService;

  beforeEach(() => {
    userService = {
      oddsFormat: 'frac'
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy('getDecimal').and.returnValue(10.550)
    };

    component = new BetslipMultipleBetPartsComponent(userService, fracToDecService);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('trackByIndex should trek index', () => {
    expect(component.trackByIndex(1)).toBe(1);
  });

  describe('formatOdds', () => {
    it('should return empty string if no price', () => {
      expect(component.formatOdds(null)).toBe('');
      expect(fracToDecService.getDecimal).not.toHaveBeenCalled();
    });

    it('should not format SP type', () => {
      const price = {
        priceType: 'SP'
      };

      expect(component.formatOdds(price as any)).toBe('SP');
      expect(fracToDecService.getDecimal).not.toHaveBeenCalled();
    });

    it('should not format SP type', () => {
      const price = {
        priceNum: '10',
        priceDen: '1'
      };

      expect(component.formatOdds(price as any)).toBe('10/1');
      expect(fracToDecService.getDecimal).not.toHaveBeenCalled();
    });

    it('should not format SP type', () => {
      const price = {
        priceNum: '10',
        priceDen: '1'
      };
      userService.oddsFormat = 'decimal';

      expect(component.formatOdds(price as any)).toBe('10.55');
      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(price.priceNum, price.priceDen);
    });
  });
});
