import { ISportEventNewspaper } from './sport-event.model';

export interface IRacingFormEvent {
  class?: string;
  distance?: string;
  going?: string;
  overview?: string;
  title?: string;
  postPick?: string;
  newspapers?: [ISportEventNewspaper];
  courseGraphics?: string;
  raceType?: string;
  grade?: string;
}
