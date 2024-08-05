import { LadbrokesHistoricPricesComponent } from '@ladbrokesMobile/shared/components/historicPrices/historic-prices.component';


describe('LadbrokesHistoricPricesComponent', () => {
  let component;

  let
    user,
    localeService;

  beforeEach(() => {
    user = {
      oddsFormat: 'frac'
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Was')
    };

    component = new LadbrokesHistoricPricesComponent(
      user,
      localeService
    );

    component.outcome = {
    } as any;
  });

  it('outputRacingHistoricPrice should get historic prices', () => {
    expect(component.outputRacingHistoricPrice()).toBe('');

    component.outcome.prices = [] as any;
    expect(component.outputRacingHistoricPrice()).toBe('');

    component.outcome.prices = [{
      priceNum: 1,
      priceDen: 5
    }, {
      priceNum: 2,
      priceDen: 6
    }] as any;
    expect(component.outputRacingHistoricPrice()).toBe('2/6');

    component.outcome.prices = [{
      priceNum: 1,
      priceDen: 5
    }, {
      priceNum: 2,
      priceDen: 6
    }, {
      priceNum: 3,
      priceDen: 11
    }] as any;
    expect(component.outputRacingHistoricPrice()).toBe('2/6 > 3/11');
  });
});

