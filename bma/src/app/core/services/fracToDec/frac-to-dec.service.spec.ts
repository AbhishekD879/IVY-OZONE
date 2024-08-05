import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

describe('FracToDecService', () => {
  let service: FracToDecService;

  let userService;

  beforeEach(() => {
    userService = {
      oddsFormat: 'frac'
    };

    service = new FracToDecService(userService);
  });

  describe('getFormattedValue', () => {
    it('frac', () => {
      expect(service.getFormattedValue(1, 5)).toEqual('1/5');
    });
    it('decimal', () => {
      userService.oddsFormat = 'decimal';
      expect(service.getFormattedValue(1, 5)).toEqual('1.20');
    });
  });

  describe('fracToDec', () => {
    it('decimal', () => {
      userService.oddsFormat = 'decimal';
      expect(service.fracToDec(1, 5)).toEqual('1.20');
    });
  });

  it('getFracTional', () => {
    expect(service.getFracTional(1, 4)).toEqual('1/4');
  });

  it('getDecimal', () => {
    expect(service.getDecimal(13, 8)).toEqual(2.62);
  });

  describe('decToFrac', () => {
    it('decToFrac', () => {
      expect(service.decToFrac(21.5)).toEqual('21/1');
    });

    it('decToFrac for acca', () => {
      expect(service.decToFrac(21.5, true)).toEqual('20.5/1');
    });

    it('decToFrac for acca 1/1000', () => {
      expect(service.decToFrac(1.001, true)).toEqual('1/1000');
    });

    it('decToFrac for acca 1/100', () => {
      expect(service.decToFrac(1.01, true)).toEqual('0.01/1');
    });
  });

  describe('getAccumulatorPrice', () => {
    it('should return acca price for oddsFormat frac', () => {
      expect(service.getAccumulatorPrice('1/2')).toEqual('0.5/1');
      expect(service.getAccumulatorPrice('5/2')).toEqual('2.5/1');
      expect(service.getAccumulatorPrice('13/7')).toEqual('1.85/1');
    });

    it('should return acca price for oddsFormat frac when priceNum < 100', () => {
      expect(service.getAccumulatorPrice('100/2')).toEqual('50/1');
    });

    it('should return acca price for oddsFormat decimal when priceNum = 100', () => {
      expect(service.getAccumulatorPrice('1/100')).toEqual('0.01/1');
    });

    it('should return acca price for oddsFormat decimal', () => {
      userService.oddsFormat = 'decimal';
      expect(service.getAccumulatorPrice('100')).toEqual('100.00');
    });

    it('should return acca price for oddsFormat decimal when priceNum > 100', () => {
      userService.oddsFormat = 'frac';
      expect(service.getAccumulatorPrice('1/1000')).toEqual('1/1000');
    });
  });

  describe('roundTwoFraction', () => {

    it('should round string', () => {
      expect(service.roundTwoFraction('123.12345')).toBe('123.12');
    });

    it('should round number', () => {
      expect(service.roundTwoFraction(123.12345)).toBe('123.12');
    });

    it('should round with one fraction', () => {
      expect(service.roundTwoFraction(123.1)).toBe('123.1');
    });

    it('should round with no fraction', () => {
      expect(service.roundTwoFraction(123)).toBe('123');
    });
  });

  describe('#findNearest', () => {
    it('should return 1/100', () => {
      const result = service['findNearest'](1.01);

      expect(result).toEqual('1/100');
    });

    it('should return null', () => {
      const result = service['findNearest'](11);

      expect(result).toEqual(null);
    });

    it('should return 1/100', () => {
      const result = service['findNearest'](0.1);

      expect(result).toEqual(null);
    });
  });

  describe('getNumberWith2Decimals', () => {
    it('convert number to trimmed representation', () => {
      expect(service.getNumberWith2Decimals(2.4378)).toEqual('2.43');
    });
    it('convert string to trimmed string representation', () => {
      expect(service.getNumberWith2Decimals('2.4378')).toEqual('2.43');
    });
    it('convert NaN to empty string representation', () => {
      expect(service.getNumberWith2Decimals(NaN)).toEqual('');
    });
  });
});
