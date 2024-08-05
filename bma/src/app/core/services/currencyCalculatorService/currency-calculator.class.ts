import { IRate } from './rate.model';
import { IReducedRates } from './reduced-rates.model';

export class CurrencyCalculator {
  private rates: Array<IRate>;

  constructor(allRates) {
    this.rates = allRates;
  }

  currencyExchange(from: string, to: string, price: number): string {
    const rates = this.getCurrencyRates(from, to);
    if (from === to) {
      return Number(price).toFixed(2);
    }
    return (price / rates.tote * rates.native).toFixed(2);
  }

  private getCurrencyRates(from: string, to: string): IReducedRates {
    return this.rates.reduce((rates, rate: IRate) => {
      if (rate.currency === to) {
        rates.native = Number(rate.exchangeRate);
      } else if (rate.currency === from) {
        rates.tote = Number(rate.exchangeRate);
      }

      return rates;
    }, { native: 1, tote: 1 });
  }
}

