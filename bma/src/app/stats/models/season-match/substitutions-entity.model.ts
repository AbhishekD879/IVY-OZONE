import { IStatsMatchResultAssistant } from '../match-result/assistant.model';

export interface IStatsSeasonMatchSubstitutionsEntity {
  outgoing: IStatsMatchResultAssistant;
  incoming: IStatsMatchResultAssistant;
  time: string;
  team: string;
  id: string;
}
