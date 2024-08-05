import { Base } from './base.model';

/**
 * @enum switch values for Coupon Segment being active time ( dayOfWeek != null || from/to != null),
 */
export enum ScheduleType { DaysOfWeek, DatesPeriod }

/**
 * @class creates pair of weekday and true/false value
 * for e.g. { dayName: 'Monday', checked: true }
 */
export class DayOfWeek {
  dayName: string;
  checked: boolean;

  constructor(day: string, chosen: boolean) {
    this.dayName = day;
    this.checked = chosen;
  }

  /**
   * @function used in cms-data-table
   */
  public toString(): string {
    return this.checked ? this.dayName.slice(0, 3) : '';
  }
}

/**
 * Backend model of Coupon Segment
 * @property couponKeys - IDs of coupons for current segment
 * @property dayOfWeek - array, for e.g. ['Tuesday', 'Thursday']
 * @property from, to - dates for segment active period
 */
export interface CouponSegment extends Base {
  id: string;
  title: string;
  couponKeys: string;
  dayOfWeek: string[];
  to: string;
  from: string;
}

/**
 * UI model differs from backend model
 * @property scheduleType - switcher for Coupon Segment ( dayOfWeek != null || from/to != null),
 * @property dayOfWeekArr - array of 7 DayOfWeek objects with true values if checked
 */
export interface CouponSegmentExt extends CouponSegment {
  scheduleType: ScheduleType;
  dayOfWeekArr: DayOfWeek[];
}

