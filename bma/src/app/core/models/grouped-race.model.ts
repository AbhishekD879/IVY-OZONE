import { ISportEvent } from '@core/models/sport-event.model';

export interface IGroupedRace {
  [key: string]: {
    flag: string;
    data: ISportEvent[];
  };
}
