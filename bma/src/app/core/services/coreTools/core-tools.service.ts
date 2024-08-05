import { Injectable } from '@angular/core';
import * as _ from 'underscore';

@Injectable()
export class CoreToolsService {
  constructor() {
    this.merge = this.merge.bind(this);
  }

  isJSON(json: string): boolean {
    return (/^[\],:{}\s]*$/.test(json.replace(/\\["\\\/bfnrtu]/g, '@')
    .replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']')
    .replace(/(?:^|:|,)(?:\s*\[)+/g, '')));
  }

  /*
   * Get currency symbol from ISO
   *
   * @param {string} currency
   *
   * @return {string}
   */
  getCurrencySymbolFromISO(currency) {
    return {
      USD: '$',
      GBP: '£',
      EUR: '€',
      SEK: 'Kr',
      HKD: 'HK$',
      SGD: 'SGD$'
    }[currency] || currency;
  }

  camelize(value: string): string {
    return value.replace(/(_[a-z])/g, $1 => {
      return $1.toUpperCase().replace('_', '');
    });
  }

  /**
   * Deep merge of two objects
   * @param source
   * @param target
   * @return {any}
   */
  merge(source: any, target: any): any {
    Object.keys(target).forEach(k => {
      if (_.isObject(target[k]) && _.isObject(source[k])) {
        source[k] = source[k] || {};
        this.merge(source[k], target[k]);
      } else {
        source[k] = target[k];
      }
    });

    return source;
  }

  /**
   * Deep merge if source is empty/undefined
   * @param {any} source
   * @param {any} target
   */
  deepMerge(source: any, target: any): any {
    Object.keys(target).forEach(k => {
      if ((target && _.isObject(target[k])) && (source && _.isObject(source[k]))) {
        this.deepMerge(source[k], target[k]);
      } else if (source && target) {
        source[k] = target[k];
      } else {
        source = {};
        source[k] = target[k];
      }
    });

    return source;
  }

  /**
   * Generate UUID - Universally Unique Identifier
   *
   * @returns {string} unique str
   *          e.g."550e8400-e29b-41d4-a716-446655440000"
   */
  uuid() {
    const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split(''),
      uuidArray = new Array(36);
    let rnd = 0,
      r,
      i;

    for (i = 0; i < 36; i++) {
      if (i === 8 || i === 13 || i === 18 || i === 23) {
        uuidArray[i] = '-';
      } else if (i === 14) {
        uuidArray[i] = '4';
      } else {
        if (rnd <= 0x02) {
          // eslint-disable-next-line no-bitwise
          rnd = 0x2000000 + (Math.random() * 0x1000000) | 0;
        }

        // eslint-disable-next-line no-bitwise
        r = rnd & 0xf;
        // eslint-disable-next-line no-bitwise
        rnd = rnd >> 4;
        // eslint-disable-next-line no-bitwise
        uuidArray[i] = chars[(i === 19) ? (r & 0x3) | 0x8 : r];
      }
    }
    return uuidArray.join('');
  }

  /*
   * Check if object has nested property
   * @param obj {object} - The object to query
   * @param path {Array|string} - The path to check
   * @returns {boolean}
   */
  hasOwnDeepProperty(obj: Object, path: string): boolean {
    const args: string[] | string = _.isString(path) ? path.split('.') : path as string;

    for (let i = 0; i < args.length; i++) {
      // eslint-disable-next-line no-prototype-builtins
      if (!obj || !obj.hasOwnProperty(args[i])) {
        return false;
      }
      // eslint-disable-next-line no-param-reassign
      obj = obj[args[i]];
    }
    return true;
  }

  /**
   * Return object nested property with square braces for example myObject[1][0][4]
   * @param obj {object} - The object to query
   * @param deepSegment {string} - The path to check
   * @param defaultValue {string?} - The default fallback value to be returned
   * @returns {*}
   */
  getDeepSegment(obj: object, deepSegment: string, defaultValue: string) {
    return deepSegment.split('[').reduce((value: object[], segment: any) => {
      segment = segment.split(']')[0];
      if (_.isNumber(segment)) {
        return value && value.length && value.length > segment ? value[segment] : defaultValue;
      } else {
        return value && value.hasOwnProperty(segment) ? value[segment] : defaultValue;
      }
    }, obj);
  }

  /**
   * Return object nested property, or default value provided if property doesn't exist
   * (but when it exists even if undefined - its value will still be returned)
   * @param obj {object} - The object to query
   * @param path {string} - The path to check
   * @param def {string?} - The default fallback value to be returned
   * @returns {*}
   */
  getOwnDeepProperty(obj: any, path: string = '', def?) {
    return path.split('.').reduce((value, segment, index, segments) => {
      let valueToReturn;
      if (!_.has(value, segment.split('[')[0])) {
        segments.length = 0;
        valueToReturn = def;
      } else {
        valueToReturn = this.getDeepSegment(value, segment, def);
      }
      return valueToReturn;
    }, obj);
  }

  getDaySuffix(day) {
    if (day > 3 && day < 21) {
      return 'th';
    }
    switch (day % 10) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  }

  /**
   * Deep clone of object with out any referance
   * @param obj any object clone
   */
  deepClone(obj: any): any {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * Round down 0.056 => 0.05
   * @param number
   * @param decimals - characters after dot
   * @returns {number}
   */
  roundDown(value: number, decimals: number = 0): number {
    return Number( `${Math.floor(+`${value}e${decimals}`)}e-${decimals}`);
  }

  /**
   * Round 0.055 => 0.06
   * @param number
   * @param digits - characters after dot
   * @returns {number}
   */
  roundTo(value: number, digits: number = 0): number {
    const multiplicator = Math.pow(10, digits);
    value = parseFloat((value * multiplicator).toFixed(11));
    return Math.round(value) / multiplicator;
  }

}
