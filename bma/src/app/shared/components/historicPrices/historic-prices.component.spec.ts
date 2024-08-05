import { HistoricPricesComponent } from './historic-prices.component';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IOutcome } from '@core/models/outcome.model';
import Spy = jasmine.Spy;

describe('@HistoricPricesComponent', () => {
  let component: HistoricPricesComponent;

  let
    userService,
    localeService;

  beforeEach(() => {
    userService = {
      odds: 'frac'
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Was')
    };

    component = new HistoricPricesComponent(
      userService,
      localeService
    );

    component.outcome = {
      prices: []
    } as IOutcome;
  });

  it('default hasWasLabel input', () => {
    expect(component.hasWasLabel).toBe(false);
  });

  it('ngOnInit', () => {
    component.outcome.prices = [{} as any, {} as any];
    component.ngOnInit();

    expect(component.hasHistoricPrice).toEqual(true);
  });

  describe('@formatHistoricPrices', () => {
    const prices = [{
      livePriceDec: '11.55'
    }, {
      livePriceDec: '10.25'
    }];
    it('should return prices in decimal format', () => {
      userService.oddsFormat = 'dec';
      expect(component.formatHistoricPrices(prices as IOutcomePrice[])).toEqual('10.25 > 11.55');
    });

    it('should set class if historical prices string is longer then 13 characters', () => {
      const res = component.formatHistoricPrices(prices as IOutcomePrice[]);
      expect(res.length).toBeGreaterThan(12);
      expect(component.setLongPriceStyle).toBe(true);
    });
  });

  describe('@outputRacingHistoricPrice', () => {

    beforeEach(() => {
      component.formatHistoricPrices = jasmine.createSpy('formatHistoricPrices').and.callThrough();
    });

    it('should return []', () => {
      component.outputRacingHistoricPrice();

      expect(component.formatHistoricPrices).not.toHaveBeenCalledWith([]);
    });

    it('should return [{ id: 3 }, { id: 2 }]', () => {
      component.outcome.prices = [{ id: '1' }, { id: '2' }, { id: '3' }] as any;
      component.outputRacingHistoricPrice();

      expect(component.formatHistoricPrices).toHaveBeenCalledWith([{ id: '3' } as any, { id: '2' }]);
    });

    it('should return [{ id: 2 }]', () => {
      component.outcome.prices = [{ id: '1' }, { id: '2' }] as any;
      component.outputRacingHistoricPrice();

      expect(component.formatHistoricPrices).toHaveBeenCalledWith([{ id: '2' }] as any);
    });

    it('should add label if enabled', () => {
      (component.formatHistoricPrices as Spy).and.returnValue('');
      component['checkWasPrice'] = jasmine.createSpy('checkWasPrice').and.returnValue([{ id: '1',priceNum:'5',priceDen:'1', livePriceNum:'6', livePriceDen:'1'}]);
      component.hasWasLabel = true;
      const result = component.outputRacingHistoricPrice();

      expect(result.includes('Was')).toBe(false);
    });

    it('should add label if hasWasLabel false', () => {
      component.outcome.prices = [{ id: '1', priceNum:'5',priceDen:'1', }, { id: '2',livePriceNum:'6', livePriceDen:'1' }] as any;
      component.hasWasLabel = false;
      const result = component.outputRacingHistoricPrice();

      expect(component.formatHistoricPrices).toHaveBeenCalledWith([{ id: '2',livePriceNum:'6', livePriceDen:'1' }] as any);
    });

    it('should add label if hasWasLabel true', () => {
      component.outcome.prices = [{ id: '1', priceNum:'9',priceDen:'1' }, { id: '2',livePriceNum:'6', livePriceDen:'1' }] as any;
      component.hasWasLabel = true;
      const result = component.outputRacingHistoricPrice();

      expect(result.includes('Was')).toBe(true);
    });

    it('should not add label until enabled', () => {
      (component.formatHistoricPrices as Spy).and.returnValue('');
      component['checkWasPrice'] = jasmine.createSpy('checkWasPrice').and.returnValue([{ id: '1',priceNum:'5',priceDen:'1', livePriceNum:'6', livePriceDen:'1'}]);
      const result = component.outputRacingHistoricPrice();

      expect(result.includes('Was')).toBe(false);
    });
  });

  describe('@checkWasPrice', () => {
    it('checkWasPrice was price availble ', () => {
      const currentOdd = {id: '1',priceNum:'9', priceDen:'1' } as any;
      const histaricprices = [{ id: '1',priceNum:'5',priceDen:'1', livePriceNum:'6', livePriceDen:'1'}] as any;
      const result = component['checkWasPrice'](currentOdd, histaricprices);
      expect(result.length).toEqual(1);
    });

    it('checkWasPrice was price grater than current price ', () => {
      const currentOdd = {id: '1',priceNum:'2', priceDen:'1' } as any;
      const histaricprices = [{ id: '1',priceNum:'5',priceDen:'1', livePriceNum:'6', livePriceDen:'1'}] as any;
      const result = component['checkWasPrice'](currentOdd, histaricprices);
      expect(result.length).toEqual(0);
    });
  })

  describe('@fracFn', () => {
    it('should return price fractional format', () => {
      const price = {
        priceNum: 'priceNum',
        priceDen: 'priceDen'
      } as any;
      const result = component.fracFn(price);

      expect(result).toEqual('priceNum/priceDen');
    });

    it('should return price fractional format', () => {
      const price = {
        livePriceNum: 'livePriceNum',
        livePriceDen: 'livePriceDen'
      } as any;
      const result = component.fracFn(price);

      expect(result).toEqual('livePriceNum/livePriceDen');
    });
  });
});
