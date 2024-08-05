import { IStatsMatchResultStatistics } from '../match-result/statistics.model';
import { IStatsCountry } from '../country.model';
import { IStatsSeasonMatchBenchEntity } from './bench-entity.model';
import { IStatsMatchResultScorer } from '../match-result/scorer.model';

export interface IStatsSeasonMatchTeamA {
  statistics: IStatsMatchResultStatistics;
  country: IStatsCountry;
  id: string;
  type: string;
  name: string;
  gender: string;
  formation: string;
  betradarTeamId: string;
  score?: string;
  goals?: IStatsMatchResultScorer[];
  bench?: IStatsSeasonMatchBenchEntity[] | null;
  lineup?: IStatsSeasonMatchBenchEntity[] | null;
}
