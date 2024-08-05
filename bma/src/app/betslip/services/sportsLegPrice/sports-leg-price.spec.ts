import { SportsLegPriceModel } from '@betslip/services/sportsLegPrice/sports-leg-price';

describe('#SportsLegPriceModel', () => {
  let sportsLegPriceModel;

  beforeEach(() => {
    const price = {
      priceDen: 2,
      priceNum: 3,
      priceType: '1'
    };

    sportsLegPriceModel = new SportsLegPriceModel(price);
  });

  it('should set data prop to sportsLegPriceModel after init', () => {
    expect(sportsLegPriceModel.data).toBeDefined();
  });

  it('should call toNum twice', () => {
    spyOn(sportsLegPriceModel, 'toNum');

    const den = sportsLegPriceModel.den, num = sportsLegPriceModel.num;

    expect(sportsLegPriceModel.toNum).toHaveBeenCalledTimes(2);
  });

  it('should set props to sportsLegPriceModel.data', () => {
    sportsLegPriceModel.props = { smth: 'smth' };

    expect(sportsLegPriceModel.props.smth).toBe('smth');
    expect(sportsLegPriceModel.props.priceNum).toBe(3);
  });

  it('toNum() should return value as number', () => {
    expect(sportsLegPriceModel.toNum('2')).toBe(2);
  });

  it('toNum() should return value as number', () => {
    expect(sportsLegPriceModel.toNum(null)).toBe(null);
  });

  it('doc() should set id property to current sportsLegPriceModel.type', () => {
    const result = sportsLegPriceModel.doc(true, true);

    expect(result.price.priceTypeRef.id).toBe('1');
  });

  it('doc() should set id property to "GUARANTEED"', () => {
    sportsLegPriceModel.data.priceType = 'LP';

    const result = sportsLegPriceModel.doc(true, true);

    expect(result.price.priceTypeRef.id).toBe('GUARANTEED');
  });

  it('doc() shouldn"t set num & den props', () => {
    sportsLegPriceModel.data.priceType = 'SP';

    const result = sportsLegPriceModel.doc(true, true);

    expect(result.price.num).toBeUndefined();
    expect(result.price.den).toBeUndefined();
  });
});
