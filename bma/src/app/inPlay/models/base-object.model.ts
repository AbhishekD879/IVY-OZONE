import { IEvent } from './in-play-event.model';

export interface IBaseObject {
  publishedDate: string;
  type: string;
  event: IEvent;
}
