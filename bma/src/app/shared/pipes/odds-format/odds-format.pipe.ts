import { Pipe, PipeTransform } from '@angular/core';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Pipe({
  name: 'oddsFormat'
})
export class OddsFormatPipe implements PipeTransform {

  constructor(
    private fracToDecService: FracToDecService
  ) {}

  /**
   * Transform frac /dec format according to PriceOddsValueDirective.oddsPriceValue cases
   *
   * @param {number} priceNum
   * @param {number} priceDen
   * @param {number} priceType
   */
  transform(priceNum: number, priceDen: number, priceType: string, isRacing: boolean): string {
    if (!priceType && !isRacing) {
      return 'SUSP';
    }

    if (!priceType || priceType === 'SP') {
      return 'SP';
    }

    return <string>this.fracToDecService.getFormattedValue(priceNum, priceDen);
  }
}
