import { ITeams } from './teams.model';

export interface IDelta {
  isDisplayed?: boolean;
  priceDec?: number;
  priceDen?: number;
  priceNum?: number;
  status?: string;
  lp_num?: string | number;
  lp_den?: string | number;
  outcomeStatusCode?: string;
  marketStatusCode?: string;
  eventStatusCode?: string;
  eventIsLive?: boolean;
  resulted?: boolean;
  raceStage?: string;
  clock_seconds?: string;
  score?: ITeams;
  ev_id?: string;
  last_update?: string;
  last_update_secs?: string;
  offset_secs?: string;
  period_code?: string;
  sport?: string;
  start_time_secs?: string;
  state?: string;
  originalName?: string;
  priceType?: string;
  fcMktAvailable?: string;
  tcMktAvailable?: string;
  updateEventId?: string;
}
