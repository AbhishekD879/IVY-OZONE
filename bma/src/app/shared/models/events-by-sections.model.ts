import { ISportEvent } from '@core/models/sport-event.model';

interface IGroupedByDate {
  title: string;
  startTime: string;
  events: Array<ISportEvent>;
}

export interface IEventsBySections {
  classDisplayOrder: number;
  className: string;
  categoryName: string;
  typeName: string;
  typeDisplayOrder: number;
  groupedByDate: {} | { [index: string]: IGroupedByDate };
  events: Array<ISportEvent>;
  typeId: string;
  sectionTitle?: string;
}
