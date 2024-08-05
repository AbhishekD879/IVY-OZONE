import { Injectable } from '@angular/core';
import { IPrice, IPriceRangeItem } from '../components/oddsBoostPrice/odds-boost-price.model';

@Injectable()
export class OddsBoostPriceService {
  getFractionalPriceRange(oldPrice: IPrice, newPrice: IPrice): IPriceRangeItem[] {
    const oldNumerator = +oldPrice.num;
    const oldDenominator = +oldPrice.den;

    const newNumerator = +newPrice.num;
    const newDenominator = +newPrice.den;

    return [
      {
        range: this.getRange(oldNumerator, newNumerator),
        scrollUp: oldNumerator < newNumerator
      },
      { divider: '/' },
      {
        range: this.getRange(oldDenominator, newDenominator),
        scrollUp: oldDenominator < newDenominator
      }
    ];
  }

  getDecimalPriceRange(oldPrice: IPrice, newPrice: IPrice): IPriceRangeItem[] {
    let oldDecimal = (+oldPrice.decimal || +oldPrice.num / +oldPrice.den).toFixed(2);
    let newDecimal = (+newPrice.decimal || +oldPrice.num / +oldPrice.den).toFixed(2);

    const oldDecimalDotIndex = oldDecimal.indexOf('.');
    const newDecimalDotIndex = newDecimal.indexOf('.');

    if (oldDecimalDotIndex < newDecimalDotIndex) {
      oldDecimal = 'x'.repeat(newDecimalDotIndex - oldDecimalDotIndex) + oldDecimal;
    } else if (newDecimalDotIndex < oldDecimalDotIndex) {
      newDecimal = 'x'.repeat(oldDecimalDotIndex - newDecimalDotIndex) + newDecimal;
    }

    const oldPriceParts = oldDecimal.split('');
    const newPriceParts = newDecimal.split('');

    return oldPriceParts.map((oldPart, index) => {
      if (oldPart === '.') {
        return { divider: '.' };
      }

      if (oldPart === 'x' || newPriceParts[index] === 'x') {
        return {
          range: [oldPart, newPriceParts[index]],
          scrollUp: oldPart !== 'x'
        };
      }

      const from = +oldPart;
      const to = +newPriceParts[index];
      return {
        range: this.getRange(from, to),
        scrollUp: from < to
      };
    });
  }

  private getRange(from: number, to: number): number[] {
    return from < to ? this.getNumberRange(to, from) : this.getNumberRange(from, to);
  }

  private getNumberRange(min: number, max: number, limit: number = 100): number[] {
    const total = (min < max ? max - min : min - max) + 1;

    let step = total > limit ? Math.round(total / limit) : 1;
    if (min > max) {
      step = -step;
    }

    const range = [];
    for (let i = 0, cur = min; i < total && i < limit; ++i, cur += step) {
      range.push(cur);
    }

    const last = range.length - 1;
    if (range[last] !== max) {
      range[last] = max;
    }

    return range;
  }
}
