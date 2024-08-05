import { IStatsMatchResult } from './match-result.model';

export interface IStatsMatchResultMatchesWithGoalScorers {
  goalScorerIds: string[];
  matches: IStatsMatchResult[];
}
