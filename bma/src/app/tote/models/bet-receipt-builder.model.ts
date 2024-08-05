import { IPoolBet } from './pool-bet.model';

export interface IFailedAndSuccessBets {
  successBets: IPoolBet[];
  failedBets: IPoolBet[];
}

export interface IBetReceiptBuilder extends IFailedAndSuccessBets {
  totalStake: number;
  unsuccessfulBetReceiptMsg: string;
  successfulBetReceiptMsg: string;
}
