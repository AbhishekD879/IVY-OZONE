import { IStatsBase } from './base.model';

export interface IStatsCompetitions extends IStatsBase {
  areaId: string;
  name: string;
  sportId: string;
  uniqIdentifier: string;
  displayOrder?: string;
  title?: string;
  hidden?: boolean;
}
