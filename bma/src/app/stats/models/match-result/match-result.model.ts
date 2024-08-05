import { IStatsBase } from '../base.model';
import { IStatsResult } from '../result.model';
import { IStatsMatchResultRound } from './round.model';
import { IStatsMatchResultArea } from './area.model';
import { IStatsMatchResultSport } from './sport.model';
import { IStatsMatchResultCompetition } from './competition.model';
import { IStatsMatchResultSeason } from './season.model';
import { IStatsMatchResultTeam } from './team.model';
import { IStatsMatchResultLineupEntity } from './lineup-entity.model';
import { IStatsMatchResultScorer } from './scorer.model';
import { IStatsMatchResultBookingsEntity } from './bookings-entity.model';

export interface IStatsMatchResult extends IStatsBase {
  kickOffTime: string;
  date: number;
  round: IStatsMatchResultRound;
  canceled: string;
  postponed: string;
  sport: IStatsMatchResultSport;
  area: IStatsMatchResultArea;
  competition: IStatsMatchResultCompetition;
  season: IStatsMatchResultSeason;
  result: IStatsResult;
  teamA: IStatsMatchResultTeam;
  teamB: IStatsMatchResultTeam;
  correctionDate?: string | Date;
  displayOrder?: number;
  lineup?: IStatsMatchResultLineupEntity[] | null;
  bookings?: (IStatsMatchResultBookingsEntity | null)[] | null;
  referee?: IStatsMatchResultSport;
  substitutions?: null[] | any;
  goals?: IStatsMatchResultScorer[];
}
