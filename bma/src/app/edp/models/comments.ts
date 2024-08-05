import { ITeams } from '@core/models/team.model';

export default interface IComments {
  teams: ITeams;
  facts: any[];
  latestPeriod: { [index: string]: any };
  setsScores: { [key: string]: number; }[];
  runningSetIndex: number;
  runningGameScores: { [index: string]: any };
}
