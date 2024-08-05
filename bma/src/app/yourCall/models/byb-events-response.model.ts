import { IYourcallTeamBase } from '@yourcall/models/yourcall-api-response.model';

export interface IYourcallBYBEventsResponse {
  data: IYourcallBYBEventResponse;
}

export interface IYourcallBYBLeagueEventsResponse {
  data: IYourcallBYBEventResponse[];
}

export interface IYourcallBYBEventResponse {
  date: string;
  homeTeam: IYourcallTeamBase;
  visitingTeam: IYourcallTeamBase;
  obEventId: number;
  obSportId: number;
  obTypeId: number;
  status: number;
  title: string;

  normilized?: boolean;
  categoryName?: string;
  className?: string;
  typeName?: string;
  hasPlayerProps?: boolean;

  expaned?: boolean;
  initiallyExpanded?: boolean;
  eventsLoaded?: boolean;
}
