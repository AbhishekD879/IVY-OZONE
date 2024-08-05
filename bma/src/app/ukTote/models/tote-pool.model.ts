import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';
import { IOutcome } from '@core/models/outcome.model';

export interface IUkTotePoolBet {
  currencyCode: string;
  guides: any;
  id: number;
  isActive: boolean;
  legCount: string;
  marketIds: string[];
  maxStakePerLine: string;
  maxTotalStake: string;
  minStakePerLine: string;
  minTotalStake: string;
  poolType: string;
  provider: string;
  responseCreationTime: string;
  stakeIncrementFactor: string;
  type: string;
  poolValue: string;
}

export interface IUkTotePoolOptions {
  betModel: TotePotBet | IOutcome[];
  currentPool?: IUkTotePoolBet;
  poolType: string;
}

export interface IUkTotePoolBetsMap {
  [ key: string ]: IUkTotePoolBet;
}
