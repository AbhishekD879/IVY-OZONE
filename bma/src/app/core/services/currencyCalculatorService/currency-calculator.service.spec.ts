
import { of as observableOf,  Observable } from 'rxjs';

import { CurrencyCalculatorService } from './currency-calculator.service';

describe('CurrencyCalculatorService', () => {
  let service: CurrencyCalculatorService;

  let bppService;

  beforeEach(() => {
    bppService = {
      send: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    service = new CurrencyCalculatorService(bppService);
  });

  it('getCurrencyCalculator', () => {
    expect(service.getCurrencyCalculator()).toEqual(jasmine.any(Observable));
    expect(bppService.send).toHaveBeenCalledWith('getCurrencyRates');
  });
});
