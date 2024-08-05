
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BppService } from '../../../bpp/services/bpp/bpp.service';
import { CurrencyCalculator } from './currency-calculator.class';
import { Observable } from 'rxjs';
import { IRate } from './rate.model';

@Injectable()
export class CurrencyCalculatorService {
  constructor(
    private bppService: BppService) {}

  /**
   * @ngdoc factory
   * @name toteCurrencyFactory
   * @description
   * # toteCurrencyFactory
   * Factory in the tote module.
   */
  getCurrencyCalculator(): Observable<CurrencyCalculator> {
    return (this.bppService.send('getCurrencyRates') as Observable<any>).pipe(
      map((allRates) => {
        const rates: IRate[] = allRates.response.respGetCurrencies.currencyDetail;
        return new CurrencyCalculator(rates);
      }));
  }
}
