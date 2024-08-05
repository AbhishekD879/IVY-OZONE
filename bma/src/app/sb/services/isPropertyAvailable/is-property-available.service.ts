import { Injectable } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';

@Injectable()
export class IsPropertyAvailableService {
  constructor() {}

  /**
   * Checks: have any of array events specific property possibility
   * @param checkCondition {function}
   *
   * @returns {Function}
   */
  isPropertyAvailable(checkCondition: Function): Function {
    return (eventsArr: ISportEvent[], configArr: { cashoutAvail: string }[]) => {
      return eventsArr.some(this.isGroupPropertyAvailable(configArr, checkCondition));
    };
  }

  /**
   * Disabled/enabled property for group of events
   * @param configArr {array}
   * @param checkCondition {function}
   *
   * @returns {Function}
   */
  private isGroupPropertyAvailable(configArr: { cashoutAvail: string }[], checkCondition: Function): (value: ISportEvent ) => boolean {
    return (eventObj: ISportEvent) => {
      return checkCondition(eventObj, configArr);
    };
  }
}


