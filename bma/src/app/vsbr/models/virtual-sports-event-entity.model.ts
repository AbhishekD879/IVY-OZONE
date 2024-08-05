import { ISportEvent } from '@core/models/sport-event.model';

export interface IVirtualSportEventEntity {
  id: string;
  title: string;
  event: ISportEvent;
}
