import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { multiplesOrderRules } from '@betslip/constants/multiples-order-rules.constant';
import { ISingleBet } from '@core/models/single-bet.model';
import { TimeService } from '@core/services/time/time.service';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipFiltersService {
  constructor(private timeService: TimeService) {}

  filterStakeValue(val: number): number {
    return Number(val.toString().replace(/[^0-9.]/g, '')) || 0;
  }

  handicapValueFilter(handicapValue: string): string {
    return handicapValue.indexOf('-') === -1
      ? `+${handicapValue}`
      : `${handicapValue}`;
  }

  multiplesSort(multiples: ISingleBet[], allSinglesLen: number): ISingleBet[] {
    _.map(multiples, betObj => _.extend(betObj, {
      weight: this.getWeight(betObj, allSinglesLen)
    }));

    return _.sortBy(multiples, 'weight');
  }

  todayTomorrowDate(value: Date, isShort: boolean, ukTimeZone?: boolean): string {
    let formattedDate: string;
    let isTomorrow: boolean;

    const now = new Date();
    const isToday: boolean = this.timeService.isEqualDatesByPattern(now, value, 'dd/MM/yyyy', ukTimeZone);

    if (!isToday) {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);

      isTomorrow = this.timeService.isEqualDatesByPattern(now, value, 'MM/yyyy', ukTimeZone)
        && this.timeService.isEqualDatesByPattern(tomorrow, value, 'dd', ukTimeZone);
    }

    if (isToday) {
      formattedDate = isShort
        ? 'Today'
        : `${this.timeService.formatByPattern(value, 'hh:mm a', null, ukTimeZone)}, Today`;
    } else if (isTomorrow) {
      formattedDate = isShort
        ? 'Tomorrow'
        : `${this.timeService.formatByPattern(value, 'hh:mm a', null, ukTimeZone)}, Tomorrow`;
    } else {
      formattedDate = isShort
        ? this.timeService.formatByPattern(value, 'd MMM, yyyy', null, ukTimeZone)
        : this.timeService.formatByPattern(value, 'hh:mm a, d MMM, yyyy', null, ukTimeZone);
    }

    return formattedDate;
  }

  /**
   *  This Method used for decorates bsMultiples with .weight method
   * @param bsElement:<Array> - concrete multiplier
   * @param allBetsCount:<Number> - count items in BetSlip
   * @returns {number}
   */
  private getWeight(bsElement: ISingleBet, allBetsCount: number): number | string {
    let rule: { [key: string]: any } = multiplesOrderRules.more,
      result: number | string = rule.other;
    const bsType: string = bsElement.type;

    if (_.has(multiplesOrderRules, allBetsCount.toString())) {
      rule = multiplesOrderRules[allBetsCount];
    }

    rule.patterns.forEach(item => {
      switch (item[1]) {
        case 'strict':
          result = (item[0] === bsType ? item[2] : result);
          break;
        case 'r_exp':
          result = (new RegExp(item[0].toString(), 'ig').test(bsType) ? item[2] : result);
          break;
        default:
      }
    });

    return result;
  }
}
