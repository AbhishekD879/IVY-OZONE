import { IStatsMatchResultAssistant } from './assistant.model';

export interface IStatsMatchResultScorer {
  date: number;
  playerID: string;
  playerName: string;
  time: string;
  team: string;
  id: string;
  score: string;
  shootout: string;
  awayTeamScore: string;
  homeTeamScore: string;
  playerLastname: string;
  injuryTime?: string | null;
  type?: string | null;
  assistant?: IStatsMatchResultAssistant | null;
}
