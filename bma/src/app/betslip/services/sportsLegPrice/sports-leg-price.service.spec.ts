import { SportsLegPriceModel } from '@betslip/services/sportsLegPrice/sports-leg-price';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { IPrice as IBasePrice } from '@core/models/price.model';
import { IPrice } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('#SportsLegPriceService', () => {
  let sportsLegPriceService;

  beforeEach(() => {
    sportsLegPriceService = new SportsLegPriceService();
  });

  it('construct() should return SportsLegPriceModel', () => {
    const result = sportsLegPriceService.construct({ } as IBasePrice);

    expect(result instanceof SportsLegPriceModel).toBeTruthy();
  });

  it('parse() should return SportsLegPriceModel', () => {
    const result = sportsLegPriceService.parse({ priceNum: 2, priceDen: 4, priceTypeRef: { id: 1 }} as IBasePrice);

    expect(result instanceof SportsLegPriceModel).toBeTruthy();
    expect(result.data.priceNum).toBe(2);
    expect(result.data.priceDen).toBe(4);
    expect(result.data.priceType).toBe(1);
  });

  it('convert() should return object', () => {
    const result = sportsLegPriceService.convert({ num: 2, den: 4, type: '1' } as IPrice);

    expect(result.priceNum).toBe(2);
    expect(result.priceDen).toBe(4);
    expect(result.priceType).toBe('1');
  });
});
