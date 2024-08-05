
import { of as observableOf } from 'rxjs';
import { CouponsListService } from '@sb/components/couponsList/coupons-list.service';

import { ICoupon } from '@sb/components/couponsListSportTab/coupons.model';
import { fakeAsync, flush } from '@angular/core/testing';
import { ICouponSegment } from '@sb/components/couponsList/coupons-list.model';

describe('CouponsListService', () => {

  let service: CouponsListService;
  let cmsService;

  const couponSegments = [{
    title: 'Featured Coupons 1',
    couponKeys: '134,543,528',
    dayOfWeek: 'SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY',
    from: null,
    to: null
  }, {
    title: 'Featured Coupons 2',
    couponKeys: '354,856',
    dayOfWeek: 'FRIDAY',
    from: null,
    to: null
  }, {
    title: 'Featured Coupons 3',
    couponKeys: '587,612',
    dayOfWeek: null,
    from: '2128-11-18T23:00:00:00Z',
    to: '3018-11-18T23:00:00:00Z'
  }, {
    title: 'Featured Coupons 4',
    couponKeys: '346,587,612',
    dayOfWeek: null,
    from: '1018-11-18T23:00:00:00Z',
    to: '3018-11-18T23:00:00:00Z'
  }] as any;

  const couponSegmentsByRange = [{
    title: 'Featured Coupons',
    couponKeys: '346,587,612',
    dayOfWeek: null,
    from: '1128-11-18T23:00:00:00Z',
    to: '1018-11-18T23:00:00:00Z'
  }]  as any;

  const couponSegmentsByDay = [{
    title: 'Featured Coupons 1',
    couponKeys: '134,543,528',
    dayOfWeek: 'SUNDAY',
    from: null,
    to: null
  }] as any;

  const coupons = [
    { id: '587', displayOrder: 1, name: 'B Coupon' },
    { id: '243', displayOrder: 1, name: 'A Coupon' },
    { id: '553', displayOrder: 3, name: 'C Coupon' },
    { id: '346', displayOrder: 2, name: 'D Coupon' }] as ICoupon[];

  const sortedCoupons = [
    { id: '243', displayOrder: 1, name: 'A Coupon' },
    { id: '587', displayOrder: 1, name: 'B Coupon' },
    { id: '346', displayOrder: 2, name: 'D Coupon' },
    { id: '553', displayOrder: 3, name: 'C Coupon' }] as ICoupon[];

  const featuredSegment = [{
    title: 'Featured Coupons 4',
    couponKeys: ['346', '587', '612'],
    coupons: [
      { id: '346', displayOrder: 2, name: 'D Coupon' },
      { id: '587', displayOrder: 1, name: 'B Coupon' }],
    dayOfWeek: null,
    from: '1018-11-18T23:00:00:00Z',
    to: '3018-11-18T23:00:00:00Z'
  }, {
    title: 'Popular Coupons',
    couponKeys: ['243', '553'],
    coupons: [
      { id: '243', displayOrder: 1, name: 'A Coupon' },
      { id: '553', displayOrder: 3, name: 'C Coupon' }]
  }] as any;

  const popularSegment = [{
    title: 'Popular Coupons',
    couponKeys: ['587', '243', '553', '346'],
    coupons: [
      { id: '243', displayOrder: 1, name: 'A Coupon' },
      { id: '587', displayOrder: 1, name: 'B Coupon' },
      { id: '346', displayOrder: 2, name: 'D Coupon' },
      { id: '553', displayOrder: 3, name: 'C Coupon' }]
  }] as any;

  describe('CouponsListService', () => {
    beforeEach(() => {
      cmsService = {
        getCouponSegment: jasmine.createSpy().and.returnValue(observableOf(couponSegments))
      };

      service = new CouponsListService(cmsService);
    });

    it('getCouponByDay - should return coupons based on day of week', () => {
      expect(service['getCouponByDay'](couponSegments)).toEqual(couponSegments[0]);
      expect(service['getCouponByDay'](couponSegmentsByRange)).toEqual({} as any);
    });

    it('getCouponByDateRange - should return coupons based on date range', () => {
      expect(service['getCouponByDateRange'](couponSegments)).toEqual(couponSegments[3]);
      expect(service['getCouponByDateRange'](couponSegmentsByDay)).toEqual({} as any);
    });

    it('getCouponByDate - should return coupons based on current date or day', () => {
      expect(service['getCouponByDate'](couponSegments)).toEqual(couponSegments[3]);
      expect(service['getCouponByDate'](couponSegmentsByRange)).toEqual({} as any);
      expect(service['getCouponByDate']([couponSegments[0]])).toEqual(couponSegments[0]);
    });

    describe('sortCoupons -', () => {
      it('should get Sorted Coupon data', () => {
        expect(service['sortCoupons'](coupons)).toEqual(sortedCoupons);
      });

      it('should return empty array', () => {
        expect(service['sortCoupons']([])).toEqual([]);
      });
    });

    describe('groupCouponBySegment -', () => {
      it('should group coupons based on ids', () => {
        const expected = [{ title: 'Popular Coupons', couponKeys: [], coupons: [] }];

        expect(service.groupCouponBySegment(coupons, couponSegments)).toEqual(featuredSegment);
        expect(service.groupCouponBySegment(coupons, couponSegmentsByRange)).toEqual(popularSegment);
        expect(service.groupCouponBySegment([], couponSegmentsByRange)).toEqual(expected);
      });

      it('should form popularSegment coupons and couponKeys only if no couponSegments', () => {
        spyOn(service, 'getCouponByDate' as any);

        expect(service.groupCouponBySegment(coupons, [])).toEqual(popularSegment);
        expect(service['getCouponByDate']).not.toHaveBeenCalled();
      });
    });

    it('getCouponSegment - should get Coupon Segment data from CMS', fakeAsync(() => {
      service.getCouponSegment()
        .subscribe((data: ICouponSegment[]) => {
          expect(data).toEqual(couponSegments);
          expect(cmsService.getCouponSegment).toHaveBeenCalled();
        });

      flush();
    }));
  });
});
