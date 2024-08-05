import { CashoutBet } from '../betModels/cashoutBet/cashout-bet.class';
import { PlacedBet } from '../betModels/placedBet/placed-bet.class';
import { RegularBet } from '../betModels/regularBet/regular-bet.class';

export interface ICashOutData {
  footballBellActive?: boolean;
  footballAlertsVisible?: boolean;
  winAlertsActive? : boolean;
  eventSource: CashoutBet | RegularBet | PlacedBet;
  location: string;
  optaDisclaimerAvailable?: boolean;
  hasActiveEvent?: boolean;
}

export interface IPayoutUpdate {
  updatedReturns: PayoutResponse[];
}


export interface PayoutResponse{
   returns: number;
   betNo: string;
}
