import { ISportEvent } from '@core/models/sport-event.model';

export interface ICompetitionGroupFormatted {
  categoryName: string;
  events: ISportEvent[];
}
