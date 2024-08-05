import { Component, Input } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { PRIZEPOOL } from '@app/fiveASideShowDown/constants/constants';
import {
  IPrize,
  IPrizeTypeDesc,
} from '@app/fiveASideShowDown/models/IPrize';

@Component({
  selector: 'fiveaside-prize-pool',
  template: ``
})

/**
 * Prize Pool Component used to populate the prize header
 * and show the prize pool grid
 */
export class FiveASidePrizePoolComponent {
  @Input() prizePoolData: IPrize | any;

  readonly prizeTypeDesc: IPrizeTypeDesc = PRIZEPOOL.prizeTypeDesc;
  readonly FREEBET: string = PRIZEPOOL.freebet;
  readonly TICKET: string = PRIZEPOOL.ticket;
  readonly VOUCHER: string = PRIZEPOOL.voucher;
  readonly CASH: string = PRIZEPOOL.cash;
  readonly signPostingLogoUrl: string =
    environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;

  currencySymbol: string = PRIZEPOOL.userCurrency;

  constructor() {}

  /**
   * Return one for the natural ordering of key value angular pipe
   * @returns { number }
   */
  public returnOne(): number {
    return 1;
  }

  /**
   * Add ordinal suffix to prizes
   */
  // eslint-disable-next-line
  public addOrdinalSuffix(number: string): string {
    let suffixNumber =  number;
    if (number.includes('-')) {
      const REPLACE_ALL_SPACES = / /g;
      number = number.replace(REPLACE_ALL_SPACES,'');
      suffixNumber =  number;
      [ number ] = number.split('-').slice(-1);
    }
    const numberVal: number = Number(number);
    const tenModule: number = numberVal % 10;
    const hundredModule: number = numberVal % 100;

    if (tenModule === 1 && hundredModule !== 11) {
      return `${suffixNumber}st`;
    }
    if (tenModule === 2 && hundredModule !== 12) {
      return `${suffixNumber}nd`;
    }
    if (tenModule === 3 && hundredModule !== 13) {
      return `${suffixNumber}rd`;
    }
    return `${suffixNumber}th`;
  }

  /**
   * To Get signposting url
   * @param {string} fileName
   * @returns {string}
   */
  public getSignpostingUrl(fileName: string): string {
    return `${this.signPostingLogoUrl}${fileName}`;
  }

  /**
   * To limit the decimal length
   * @param {string} value
   * @returns {string}
   */
   public fixedDecimals(value: string): string {
    const decimalValues = value.toString().split('.')[1];

    if(Number(decimalValues) > 0) {
      return Number(value).toFixed(2).toString();
    } else {
      return Math.round(Number(value)).toString();
    }
  }
}


