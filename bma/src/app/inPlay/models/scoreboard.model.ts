import { IEventDetails } from './in-play-event-details.model';

export interface IScoreboard {
  in_periods: number;
  subperiod: IEventDetails[];
  current: IEventDetails[];
  all: IEventDetails[];
}
