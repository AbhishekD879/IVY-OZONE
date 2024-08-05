import { IClassModel } from '@core/models/class.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface ICompetitionPage {
  data: {
    events: ISportEvent[];
    type: IClassModel;
  };
  outrights: ISportEvent[];
}

export interface ICompetitionPageTab {
  id: string;
  label: string;
  name: string;
}
