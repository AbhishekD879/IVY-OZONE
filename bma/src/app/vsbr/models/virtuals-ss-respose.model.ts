import { ISportEvent } from '@core/models/sport-event.model';
import { IRacingFormOutcome } from '@core/models/outcome.model';
import { IClassModel } from '@core/models/class.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';

export interface ISsResponse {
  event?: ISportEvent;
  racingFormOutcome?: IRacingFormOutcome;
}

export interface ISsResponseWrapper {
  children: ISsResponse[];
}

export interface IEventWithRacingFormResponse {
  SSResponse: ISsResponseWrapper;
}

export interface IEventSSResponse {
  SSResponse: {
    children: ISportEventEntity[];
  };
}

export interface ITournamentClass {
  alias: string;
  name: string;
  startTimeUnix?: number;
  timeLeft?: number;
  id?: string;
}

export interface ICategoryClass {
  class: IClassModel | ITournamentClass;
}

export interface ISportEventGroup {
  [key: string]: ISportEventEntity[];
}

export interface IVirtualSportsEventsData {
  events: ISportEventGroup | ISportEvent[];
  categories: ICategoryClass[];
}
