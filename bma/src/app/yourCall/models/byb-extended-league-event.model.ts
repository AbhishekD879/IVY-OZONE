import { IYourcallBYBEventResponse } from './byb-events-response.model';

export interface IBybExtendedLeagueEvent extends IYourcallBYBEventResponse {
  id: string;
  teamHome: string;
  teamAway: string;
}
