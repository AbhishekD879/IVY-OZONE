import { YourCallMarketPlayer } from './markets/yourcall-market-player';
import { IYourcallSelectedInfo } from './yourcall-market-player.model';
export interface IYourcallSeletionBase {
  relatedTeamType: number;
  relatedPlayerId: number;
  title: string;
  status: number;
  odds: string | { type: number, condition: number, value: string };
  bettingValue1: string;
  bettingValue2: string;
  displayOrder: number;
  id: number;
  playerId: number;
  statistic: string;
  value: number | string;
  type: number;
  idd:any;
}

export interface IYourcallSelection extends IYourcallSeletionBase {
  // DYNAMIC VALUES
  dashboardTitle?: string;
  statisticId?: any;
  error?: boolean;
  errorMessage?: string[];
  game1Id?: string;
  player1Id?: string;
  player?: any;
  group?: any;
  stat?: any;
  disable?: boolean;
  edit?: boolean;
  statVal?: string;
  condition?: string | number;
  key?: string;
  obtainedPlayerFeed: any;
  selectedInfo: IYourcallSelectedInfo;
  obtainedStatValues: any;
  obtainedStatValuesToDisplay: any;
  marketType: string;
  players: YourCallMarketPlayer[];
  playerObj: any;
  statObj: any;
  gameId: string;
  idd: any;
  iddInc:any;
}
