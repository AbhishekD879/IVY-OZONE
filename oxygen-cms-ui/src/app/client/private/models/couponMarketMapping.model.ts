import { Base } from './base.model';

export interface CouponMarketMapping extends Base {
  couponId: string;
  marketName: string;
  sortOrder: number;
}