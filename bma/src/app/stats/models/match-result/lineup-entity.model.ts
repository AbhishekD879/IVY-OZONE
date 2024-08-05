import { IStatsMatchResultPlayersEntity } from './players-entity.model';
import { IStatsMatchResultTeamCommon } from './team-common.model';

export interface IStatsMatchResultLineupEntity {
  substitutes: string;
  team: IStatsMatchResultTeamCommon;
  players?: IStatsMatchResultPlayersEntity[] | null;
}
