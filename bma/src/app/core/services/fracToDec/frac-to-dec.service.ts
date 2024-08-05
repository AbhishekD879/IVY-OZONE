import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { DECIMAL_LOW_MAP, DECIMAL_TO_FRACTIONAL_MAP, FRACTIONAL_TO_DECIMAL_MAP } from '../constants/frac-to-dec.constant';
import { IConstant } from '../models/constant.model';
import { UserService } from '@core/services/user/user.service';

@Injectable()
export class FracToDecService {
  private decFracMap: Array<IConstant> = DECIMAL_TO_FRACTIONAL_MAP;
  private decLowMap: Array<IConstant> = DECIMAL_LOW_MAP;
  private maxDecInMap: number = this.decFracMap[this.decFracMap.length - 1].dec;
  private maxDecLowMap: number = this.decLowMap[this.decLowMap.length - 1].dec;

  constructor(private userService: UserService) {

  }

  getFormattedValue(priceNum: number, priceDen: number): string|number {
    if (this.userService.oddsFormat === 'frac') {
      return this.getFracTional(priceNum, priceDen);
    }

    return this.fracToDec(priceNum, priceDen);
  }

  /**
   * Convert odds format
   * @param priceNum {number}
   * @param priceDen {number}
   * @returns {string}
   */
  fracToDec(priceNum: number, priceDen: number): string|number {
    return this.getDecimal(priceNum, priceDen);
  }


  getFracTional(priceNum: number, priceDen: number): string {
    return `${priceNum}/${priceDen}`;
  }

  getDecimal(priceNum: number, priceDen: number, fixed: number = 2): string|number {
    const predefinedDecimalValue = FRACTIONAL_TO_DECIMAL_MAP[`${priceNum}/${priceDen}`];

    if (predefinedDecimalValue) {
      return predefinedDecimalValue;
    }

    return (1 + (priceNum / priceDen)).toFixed(fixed);
  }

  /**
   * Convert dec price to fraction
   * @param {Number} priceDec
   * @return {string}
   */
  decToFrac(priceDec: string | number, isACCAPrice: boolean = false): string {
    let price = Number(priceDec);
    if (isACCAPrice) {
      if (this.roundTwoFraction(price) === '1.00') {
        price = 1.001;
      }
      return this.findNearest(price.toFixed(3), this.decLowMap, this.maxDecLowMap)
        || `${this.roundTwoFraction(price - 1)}/1`;
    } else {
      return this.findNearest(price.toFixed(3)) || `${Math.round((price - 1))}/1`;
    }
  }

  /**
   * Convert price from 1/2 to 0.5/1, 13/7 to 1.85/1
   * @param {string} price
   * @return {string}
   */
  getAccumulatorPrice(price: string): string {
    const [priceNum, priceDen] = price.split('/');
    if (Number(priceDen) > 100) {
      return price;
    }
    if (this.userService.oddsFormat !== 'frac') {
      return Number(price).toFixed(2);
    }
    const newPrice = Number(priceNum) / Number(priceDen);

    return `${this.roundTwoFraction(newPrice)}/1`;
  }

  /**
   * Get number with two fraction digits without rounding off
   *  doesnt adds zeros if no digits after dot
   */
  roundTwoFraction(value: string | number): string {
    if (typeof value !== 'string') {
      value = value.toString();
    }

    return value.match(/^-?\d+(?:\.\d{0,2})?/)[0];
  }

  /**
   * Returns number with 2 decimals and no rounding
   * @param value {number | string}
   * @returns {string}
   */
  getNumberWith2Decimals(value: number | string): string {
    const matchedValueArr = value.toString().match(/^-?\d+(?:\.\d{0,2})?/);
    return matchedValueArr && matchedValueArr[0] ? matchedValueArr[0] : '';
  }

  /**
   * Convert odds format
   * @param decimal {number}
   * @returns {number || boolean}
   */
  private findNearest(decimal, map = this.decFracMap, max = this.maxDecInMap) {
    let prevIndex = 0;
    let frac = null;

    if (decimal >= 1 && decimal <= max && decimal % 1 !== 0) {
      _.each(map, (val, index) => {
        if (decimal >= map[prevIndex].dec && decimal <= val.dec) {
          frac = (val.dec - decimal) > (decimal - map[prevIndex].dec) ? map[prevIndex].frac
            : map[index].frac;
        }
        prevIndex = index;
      });
    }
    return frac;
  }
}
