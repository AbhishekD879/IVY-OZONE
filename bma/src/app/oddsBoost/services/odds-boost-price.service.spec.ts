import { OddsBoostPriceService } from './odds-boost-price.service';

describe('OddsBoostPriceService', () => {
  let service: OddsBoostPriceService;

  beforeEach(() => {
    service = new OddsBoostPriceService();
  });

  it('getFractionalPriceRange', () => {
    const oldPrice = { num: 1, den: 3 };
    const newPrice = { num: 3, den: 1 };

    expect(service.getFractionalPriceRange(oldPrice, newPrice)).toEqual([
      { range: [3, 2, 1], scrollUp: true },
      { divider: '/' },
      { range: [3, 2, 1], scrollUp: false }
    ]);
  });

  describe('getDecimalPriceRange', () => {
    it('should return range (oldPrice: 1.2, newPrice: 10.5)', () => {
      expect(
        service.getDecimalPriceRange({ decimal: 1.2 }, { decimal: 10.5 })
      ).toEqual([
        { range: ['x', '1'], scrollUp: false },
        { range: [1, 0], scrollUp: false },
        { divider: '.' },
        { range: [5, 4, 3, 2], scrollUp: true },
        { range: [0], scrollUp: false }
      ]);
    });

    it('should return range (oldPrice: 10.5, newPrice: 1.2 )', () => {
      expect(
        service.getDecimalPriceRange({ decimal: 10.5 }, { decimal: 1.2 })
      ).toEqual([
        { range: ['1', 'x'], scrollUp: true },
        { range: [1, 0], scrollUp: true },
        { divider: '.' },
        { range: [5, 4, 3, 2], scrollUp: false },
        { range: [0], scrollUp: false }
      ]);
    });

    it('should return range (oldPrice: 1/2, newPrice: 7/10 )', () => {
      expect(
        service.getDecimalPriceRange({ num: 1, den: 2 }, { num: 7, den: 10 })
      ).toEqual([
        { range: [0], scrollUp: false },
        { divider: '.' },
        { range: [5], scrollUp: false },
        { range: [0], scrollUp: false }
      ]);
    });
  });

  it('getRange', () => {
    expect(service['getRange'](3, 1)).toEqual([3, 2, 1]);
    expect(service['getRange'](1, 3)).toEqual([3, 2, 1]);
  });

  it('getNumberRange', () => {
    expect(service['getNumberRange'](1, 5)).toEqual([1, 2, 3, 4, 5]);
    expect(service['getNumberRange'](1, 5, 3)).toEqual([1, 3, 5]);
    expect(service['getNumberRange'](10, 5)).toEqual([10, 9, 8, 7, 6, 5]);
    expect(service['getNumberRange'](10, 5, 3)).toEqual([10, 8, 5]);
  });
});
