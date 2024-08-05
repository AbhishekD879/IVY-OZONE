import { Injectable } from '@angular/core';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';

/**
 * Service used to fetch the Pre event header details
 */
@Injectable({
  providedIn: FiveASideShowDownApiModule,
})
export class FiveASidePreHeaderService {
  constructor() { }

  /**
   * Checking the date to find whether match happening today
   * @param { Date } eventStartTime
   * @returns { boolean }
   */
  checkForMatchDay(eventStartTime: Date): boolean {
    const currentDate: Date = new Date(),
      isSameDate: boolean = eventStartTime.getDate() === currentDate.getDate(),
      isSameMonth: boolean = eventStartTime.getMonth() === currentDate.getMonth(),
      isSameYear: boolean = eventStartTime.getFullYear() === currentDate.getFullYear();
    return isSameDate && isSameMonth && isSameYear;
  }

  /**
   * calculting the time difference from eventStartTime
   * @param { Date } eventStartTime
   * @returns { number }
   */
  getTimeDifference(eventStartTime: Date, currentDate: Date): number {
    return Math.floor(new Date(eventStartTime.getTime().valueOf() - currentDate.getTime().valueOf()).valueOf() / 1000);
  }

  /**
   * formParamArray used to form the repeated array of elements
   * @param {string}
   * @param {number}
   * @returns {string[]}
   */
   formParamArray(value: string, limit: number): string[] {
    const paramArray: string[] = [];
    for (let index = 0; index < limit; index++) {
      paramArray.push(value);
    }
    return paramArray;
  }
}
