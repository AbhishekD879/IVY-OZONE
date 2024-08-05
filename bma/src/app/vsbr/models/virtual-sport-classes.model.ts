import { ISportEventEntity } from '@core/models/sport-event-entity.model';

export interface ITab {
  event: ISportEventEntity;
  id: string;
  title: string;
}

