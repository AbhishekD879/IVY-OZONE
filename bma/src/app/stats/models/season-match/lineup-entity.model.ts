import { IStatsSeasonMatchTeam } from './team.model';
import { IStatsSeasonMatchPlayersEntity } from './players-entity.model';

export interface IStatsSeasonMatchLineupEntity {
  substitutes: string;
  team: IStatsSeasonMatchTeam;
  players?: IStatsSeasonMatchPlayersEntity[] | null;
}
