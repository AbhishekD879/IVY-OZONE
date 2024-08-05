import { ISportEvent } from '@core/models/sport-event.model';

export interface IMatchesByDate {
  date: string;
  matches: ISportEvent[];
}
