import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ICashoutMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';

@Injectable()
export class CashOutLabelService {

  constructor() {
    this.checkCondition = this.checkCondition.bind(this);
  }

  /**
   * Check condition for cashout
   *
   * @param eventObj {object}
   * @param configArr {Array}
   *
   * @returns {boolean}
   */
  checkCondition(eventObj: ISportEvent, configArr: ICashoutMarket[]): boolean {
    if (!_.has(eventObj, 'cashoutAvail')) {
      return false;
    }

    return this.checkForValid(eventObj, configArr, 'cashoutAvail');
  }

  /**
   * Checks all wether valid property is present
   *
   * @param eventObj {object}
   * @param configArr {arr}
   * @param field {string}
   *
   * @returns {boolean}
   */
  private checkForValid(eventObj: ISportEvent, configArr: ICashoutMarket[], field: string): boolean {
    const validValues: string[] = _.pluck(configArr, field),
    property: string[] = eventObj[field].split(',');

    return property.some(element => {
      return validValues.indexOf(element) !== -1;
    });
  }

}
