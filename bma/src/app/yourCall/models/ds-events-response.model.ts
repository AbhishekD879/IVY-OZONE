import { IYourcallTeamBase } from '@yourcall/models/yourcall-api-response.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface IYourcallDsEventsResponse {
  version: string;
  errors: string[];
  options: {
    currentPage: number;
    totalItemsCount: number;
    totalPagesCount: number;
  };
  data: IYourcallDsEventResponse[];
}

export interface IYourcallDsEventResponse {
  date: string;
  id: number;
  isInPlayEnabled: number;
  leagueId: number;
  minute: number;
  obEventId: number;
  obTypeId: number;
  period: number;
  sportId: number;
  status: number;
  title: string;
  homeTeam: IYourcallTeamBase;
  visitingTeam: IYourcallTeamBase;

  // Dynamic yourcall params
  eventData: ISportEvent;
}
