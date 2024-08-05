import { ISportEvent } from '@core/models/sport-event.model';

export interface IOffersRacingEvent extends ISportEvent {
  link: string;
  odds: string;
}

export interface IOffersRacingGroup {
  [key: string]: {
    title: string;
    name: string;
    svgId: string;
    events: ISportEvent[];
  };
}

