import { IStatsBase } from '../base.model';
import { IStatsResult } from '../result.model';
import { IStatsMatchResultScorer } from '../match-result/scorer.model';
import { IStatsSeasonMatchArea } from './area.model';
import { IStatsSeasonMatchRound } from './round.model';
import { IStatsSeasonMatchReferee } from './referee.model';
import { IStatsSeasonMatchCompetition } from './competition.model';
import { IStatsSeasonMatchSeason } from './season.model';
import { IStatsSeasonMatchTeamA } from './team-a.model';
import { IStatsSeasonMatchLineupEntity } from './lineup-entity.model';
import { IStatsSeasonMatchBookingsEntity } from './bookings-entity.model';
import { IStatsSeasonMatchSubstitutionsEntity } from './substitutions-entity.model';

export interface IStatsSeasonMatch extends IStatsBase {
  kickOffTime: string;
  date: number;
  round: IStatsSeasonMatchRound;
  canceled: string;
  postponed: string;
  sport: IStatsSeasonMatchReferee;
  area: IStatsSeasonMatchArea;
  competition: IStatsSeasonMatchCompetition;
  season: IStatsSeasonMatchSeason;
  result: IStatsResult;
  teamA: IStatsSeasonMatchTeamA;
  teamB: IStatsSeasonMatchTeamA;
  correctionDate?: string | Date;
  lineup?: IStatsSeasonMatchLineupEntity[] | null;
  referee: IStatsSeasonMatchReferee;
  bookings?: IStatsSeasonMatchBookingsEntity[] | null;
  substitutions?: IStatsSeasonMatchSubstitutionsEntity[] | null;
  goals?: (IStatsMatchResultScorer)[] | null;
}

