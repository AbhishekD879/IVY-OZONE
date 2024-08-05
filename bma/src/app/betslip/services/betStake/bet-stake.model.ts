import { BetStake } from '@betslip/services/betStake/bet-stake';

export interface IStake {
  storeId?: string;
  amount: string|number;
  currency: string;
  lines: number;
  max: string;
  min: string;
  perLine: string | BetStake;
  [ key: string ]: any;
}
