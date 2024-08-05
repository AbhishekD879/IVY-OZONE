import { ICoupon } from '@sb/components/couponsListSportTab/coupons.model';

export interface ICouponSegment {
  title: string;
  couponKeys: string | string[];
  coupons?: ICoupon[];
  dayOfWeek?: string; // Required if `from` and `to` are not defined
  from?: string; // ISO-8601, required if `dayOfWeek` is not
  to?: string; // ISO-8601, required if `dayOfWeek` is not defined
}
