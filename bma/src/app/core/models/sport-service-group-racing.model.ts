import { ISportEvent } from '@core/models/sport-event.model';

export interface ISportServiceGroupRacing {
  flag: string;
  data: ISportEvent[];
}
