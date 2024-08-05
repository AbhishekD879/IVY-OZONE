import { ICompetition } from '@sb/components/matchResultsSportTab/competition.model';

export interface IDate {
  competitions: ICompetition[];
  opened: boolean;
  loadingMatches: boolean;
  noResults: boolean;
  date: Date;
}
