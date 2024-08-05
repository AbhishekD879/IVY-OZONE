import { ISportEvent } from '@core/models/sport-event.model';

export interface IGoalscorerCoupon {
  categoryName: string;
  classDisplayOrder: number;
  className: string;
  events: ISportEvent[];
  groupedByDate: any[];
  typeDisplayOrder: number;
  typeId: number;
  typeName: string;
  isExpanded?: boolean;
}
