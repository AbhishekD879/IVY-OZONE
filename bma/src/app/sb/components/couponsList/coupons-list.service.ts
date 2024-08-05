
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import * as _ from 'underscore';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { ICoupon } from '@sb/components/couponsListSportTab/coupons.model';
import { ICouponSegment } from '@sb/components/couponsList/coupons-list.model';
import { DAYS, POPULAR } from '@sb/components/couponsList/coupons-list.constant';

@Injectable({
  providedIn: 'root'
})
export class CouponsListService {
  private daysOfWeek: string[] = DAYS;
  private popularSegment: ICouponSegment = POPULAR;

  constructor(
    private cmsService: CmsService
  ) {}

  /**
   * Get Coupon Segment from CMS
   * @returns {Observable<ICouponSegment[]>}
   */
  getCouponSegment(): Observable<ICouponSegment[]> {
    return this.cmsService.getCouponSegment().pipe(
      map((data: ICouponSegment[]) => {
        return data;
      }));
  }

  /**
   * Group Coupon By Segment
   * @param {ICoupon[]} coupons
   * @param {ICouponSegment[]} couponSegments
   * @returns {ICouponSegment[]}
   */
  groupCouponBySegment(coupons: ICoupon[], couponSegments: ICouponSegment[]): ICouponSegment[] {
    if (couponSegments && couponSegments.length) {
      const couponSegment = this.getCouponByDate(couponSegments);
      if (!_.isEmpty(couponSegment)) {
        couponSegment.couponKeys = _.uniq((couponSegment.couponKeys as string).split(','));
        couponSegment.coupons = [];
        this.popularSegment.coupons = [];
        _.each(couponSegment.couponKeys, (id: string) => {
          const coupon = _.findWhere(coupons, { id });
          if (_.isObject(coupon)) {
            couponSegment.coupons.push(coupon);
          }
        });
        _.each(coupons, (coupon: ICoupon) => {
          if (!_.contains(couponSegment.couponKeys, coupon.id)) {
            (this.popularSegment.couponKeys as string[]).push(coupon.id);
            this.popularSegment.coupons.push(coupon);
          }
        });
        this.popularSegment.coupons = this.sortCoupons(this.popularSegment.coupons);
        return couponSegment.coupons.length > 0 ? [couponSegment, this.popularSegment] : [this.popularSegment];
      }
    }
    this.popularSegment.couponKeys = _.pluck(coupons, 'id');
    this.popularSegment.coupons = this.sortCoupons(coupons);
    return [this.popularSegment];
  }

  /**
   * Sort coupons data
   * @param {ICoupon[]} coupons
   * @returns {ICoupon[]}
   */
  private sortCoupons(coupons: ICoupon[]): ICoupon[] {
    return coupons.length ? _.chain(coupons)
      .sortBy(data => data.name.toLowerCase())
      .sortBy('displayOrder')
      .value() : [];
  }

  /**
   * Get Coupon By Date
   * @param {ICouponSegment[]} couponSegment
   * @returns {ICouponSegment}
   */
  private getCouponByDate(couponSegment: ICouponSegment[]): ICouponSegment {
    const couponByDateRange = this.getCouponByDateRange(couponSegment);
    const getCouponByDay = this.getCouponByDay(couponSegment);
    return !_.isEmpty(couponByDateRange) && couponByDateRange ||
      !_.isEmpty(getCouponByDay) && getCouponByDay ||
      {} as ICouponSegment;
  }

  /**
   * Get Coupon By Date Range (from,to)
   * @param {ICouponSegment[]} couponSegment
   * @returns {ICouponSegment}
   */
  private getCouponByDateRange(couponSegment: ICouponSegment[]): ICouponSegment {
    const couponsByRange = _.filter(couponSegment, (segment: ICouponSegment) => {
      if (segment.from && segment.to) {
        const nowDate = new Date(new Date()).getTime();
        const fromDate = this.getCorrectTime(segment.from);
        const toDate = this.getCorrectTime(segment.to);
        return fromDate <= nowDate && nowDate <= toDate;
      }
    });
    return couponsByRange && couponsByRange.length ? couponsByRange[0] : {} as ICouponSegment;
  }

  /**
   * Get Correct time
   * @param {string} date
   * @returns {number}
   */
  private getCorrectTime(date: string): number {
    const a = date.split(/[^0-9]/).map(Number);
    return new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]).getTime();
  }

  /**
   * Get Coupon By Day ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
   * @param {ICouponSegment[]} couponSegment
   * @returns {ICouponSegment}
   */
  private getCouponByDay(couponSegment: ICouponSegment[]): ICouponSegment {
    const dayIndex = new Date().getDay();
    const dayName = this.daysOfWeek[dayIndex];
    const couponsByDay = _.filter(couponSegment, (segment: ICouponSegment) => {
      if (segment.dayOfWeek) {
        return segment.dayOfWeek.indexOf(dayName) >= 0;
      }
    });
    return couponsByDay && couponsByDay.length ? couponsByDay[0] : {} as ICouponSegment;
  }
}

