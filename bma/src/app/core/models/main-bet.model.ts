import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { IBetPayout } from './bet-payout.model';
import { BetStake } from '@betslip/services/betStake/bet-stake';

export interface IMainBet {
  isMocked: boolean;
  storeId?: string;
  uid?: string;
  placed?: any;
  bsId: number;
  docId: string;
  type: string;
  lines: number;
  stake: BetStake;
  freeBet: any;
  freeBets: IFreeBet[];
  legs: any[];
  betOffer: {
    isAccaValid: boolean
  };
  errs?: any[];
  error?: string;
  errorMsg?: string;
  payout?: IBetPayout[];
  isEachWay: boolean;
  price: any;
  betComplexName: string;
  info: Function;
  update: Function;
  clearErr: Function;
  clearUserData: Function;
  clone: Function;
  updateHandicap: Function;
  oddsBoost: IOddsBoost;
  maxPayout?: string;
}

interface IOddsBoost {
  enhancedOddsPrice: number;
  enhancedOddsPriceNum: number;
  enhancedOddsPriceDen: number;
}
