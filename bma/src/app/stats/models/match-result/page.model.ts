import { IStatsMatchResultCompetition } from './competition.model';

export interface IStatsMatchResultPage {
  date: string | Date;
  loadingMatches: boolean;
  competitions: IStatsMatchResultCompetition[];
  opened: boolean;
  dateString: string | Date;
}
