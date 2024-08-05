import { IStatsMatchResultTeam } from './team.model';

export interface IStatsMatchResultGoal {
  playerLastname: string;
  score: string;
  playerID?: string;
  playerName?: string;
  time?: string;
  team?: string;
  teamA?: IStatsMatchResultTeam;
  teamB?: IStatsMatchResultTeam;
}
