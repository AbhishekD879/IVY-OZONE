import { IBaseObject } from '@app/inPlay/models/base-object.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface IUpdateEvent {
  update: IBaseObject;
  events: ISportEvent[];
}
