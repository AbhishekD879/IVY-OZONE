import { IStake } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { PlacedBet } from '../placedBet/placed-bet.class';

export class CashoutBet extends PlacedBet {
  stake?: string | IStake;
  stakePerLine?: string;
  gtmCashoutValue?: number | string;
  bybType?: any;
  source?: string;
  contestId?: string;
  winnings?: { value: string }[];
  livePriceWinnings?: { value: string}[];
  isEWCashoutSuspend?: boolean;

  constructor(bet, betModelService, currency, currencySymbol, cashOutMapIndex, cashOutErrorMessage) {
    super(bet, betModelService, currency, currencySymbol, cashOutMapIndex, cashOutErrorMessage);

    this.setCashoutProperties(bet);
  }
}
