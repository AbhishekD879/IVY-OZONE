import { ISportEvent } from './sport-event.model';
import { IClassModel } from './class.model';

export interface ISsGetEventsByTypeResponseItemModel {
  event: ISportEvent;
}

export interface IEventClassModel {
  class?: IClassModel;
  event?: ISportEvent;
}
