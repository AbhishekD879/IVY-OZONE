import { IStatsMatchResultPlayersEntity } from './players-entity.model';
import { IStatsMatchResultStatistics } from './statistics.model';
import { IStatsCountry } from '../country.model';
import { IStatsMatchResultScorer } from './scorer.model';

export interface IStatsMatchResultTeam {
  country: IStatsCountry;
  id: string;
  type: string;
  name: string;
  gender: string;
  betradarTeamId: string;
  bench?: IStatsMatchResultPlayersEntity[] | null;
  lineup?: IStatsMatchResultPlayersEntity[] | null;
  statistics?: IStatsMatchResultStatistics | null;
  formation?: string | null;
  goals?: IStatsMatchResultScorer[];
  goalScorers?: string;
  score?: string;
}
