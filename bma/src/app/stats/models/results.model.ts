import { IStatsRow } from './row.model';

export interface IStatsResults {
  areaId: string;
  competitionId: string;
  rows: IStatsRow[];
  seasonId: string;
  sportId: string;
  tableId: string;
  tableName: string;
  __v: number;
  _id: string;
}
