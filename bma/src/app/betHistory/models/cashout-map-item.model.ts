import { RegularBetBase } from '@app/betHistory/betModels/regularBetBase/regular-bet-base.class';

export interface ICashoutMapItem {
  id: string;
  isSettled: boolean;
}

export interface ICashoutBetsMap {
  cashoutIds: ICashoutMapItem[],
  placedBets: RegularBetBase[]
}
