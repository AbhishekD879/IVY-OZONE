import { ISportEvent } from '@core/models/sport-event.model';

export interface ICoupon {
  categoryName: string;
  classDisplayOrder: number;
  className: string;
  events: ISportEvent[];
  groupedByDate: any[];
  typeDisplayOrder: number;
  typeId: number;
  typeName: number;
  couponSortCode: string;
  name: string;
  id: string;
}
