import { Injectable } from '@angular/core';
import { FRACTIONAL_TO_DECIMAL_MAP } from '@app/shared/services/fracToDec/frac-to-dec.constant';

@Injectable()
export class FracToDecService {
  constructor() {
  }

  /**
   * Convert odds format
   * @param priceNum {number}
   * @param priceDen {number}
   * @returns {string}
   */
  fracToDec(priceNum: number, priceDen: number): string | number {
    return this.getDecimal(priceNum, priceDen);
  }

  getDecimal(priceNum: number, priceDen: number, fixed: number = 2): string | number {
    const predefinedDecimalValue = FRACTIONAL_TO_DECIMAL_MAP[`${priceNum}/${priceDen}`];

    if (predefinedDecimalValue) {
      return predefinedDecimalValue;
    }

    const result = (1 + (priceNum / priceDen));
    if (isFinite(result)) {
      return result.toFixed(fixed);
    }

    return null;
  }
}
