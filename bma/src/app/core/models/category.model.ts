import { ISportEvent } from '@core/models/sport-event.model';

export interface ICategory {
  id?: number;
  categoryCode: string;
  displayOrder: number;
  events: ISportEvent[];
  name: string;
}
