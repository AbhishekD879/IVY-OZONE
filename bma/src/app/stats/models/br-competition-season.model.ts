import { IStatsCompetitions } from './competitions.model';
export interface IAllSeasons {
  areaId: string;
  competitionIds: string[];
  endDate: string;
  id: string;
  name: string;
  sportId: string;
  startDate: string;
  year: string;
  _id: string;
}
export interface IStatsBRCompetitionSeason {
  status?: string;
  sportId: number;
  sportName: string;
  areaId: number;
  areaName: string;
  competitionId: number;
  competitionName: string;
  allCompetitions?: IStatsCompetitions[] | null;
  allSeasons: IAllSeasons[];
}
