import { IStatsMatchResult } from './match-result.model';

export interface IStatsMatchResultGroupedMatches {
  showButton: boolean;
  matches?: IStatsMatchResultGroup;
}

export interface IStatsMatchResultGroup {
  [key: string]: IStatsMatchResult[];
}
