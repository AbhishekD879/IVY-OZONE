import { Injectable } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';

@Injectable()
export class PriceOddsButtonService {
  constructor() {}

  /**
   * Display outcomes for racing spots.
   * @private
   * @return {Boolean}
   */
  isRacingOutcome(outcome: IOutcome, marketPriceTypeCodes: string): boolean {
    const prices = outcome.prices && outcome.prices[0];
    const priceType = outcome.correctPriceType || prices && prices.priceType;
    const priceTypeCodes = marketPriceTypeCodes && marketPriceTypeCodes.replace(/,/g, '')
      .replace(/\s+/g, '');
    const isSP = priceTypeCodes === 'SP' || priceType === 'SP';
    const isLPSP = !isSP && priceTypeCodes === 'LPSP';

    return isSP || this.isFavourite(outcome) || (isLPSP && !prices);
  }

  private isFavourite(outcome: IOutcome): boolean {
    return outcome.name.toLowerCase() === 'unnamed favourite' ||
      outcome.name.toLowerCase() === 'unnamed 2nd favourite' ||
      outcome.isFavourite;
  }
}
