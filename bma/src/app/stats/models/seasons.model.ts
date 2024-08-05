import { IStatsBase } from './base.model';

export interface IStatsSeasons extends IStatsBase {
  areaId: string;
  competitionId: string;
  endDate: string;
  name: string;
  sportId: string;
  startDate: string;
  uniqueId: string;
  year: string;
}
