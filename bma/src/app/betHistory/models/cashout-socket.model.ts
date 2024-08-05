import { ICashOutBet } from '@app/betHistory/models/bet-history-cash-out.model';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface ICashoutSocketError {
  error?: {
    code: string;
  };
}

export interface ICashoutSocketBets extends ICashoutSocketError {
  bets: IBetDetail[];
}

export interface ICashoutSocketBetUpdate extends ICashoutSocketError {
  bet: ICashOutBet;
}
export interface ICashoutSocketEventUpdate extends ICashoutSocketError {
  event: ISocketEventFinshedUpdate;
}
export interface ISocketCashoutUpdateMessage extends ICashoutSocketError {
  cashoutData: ISocketCashoutValueUpdate;
}
export interface ISocketTwoUpMessage extends ICashoutSocketError {
  twoUp: ISocketTwoUpUpdate;
}

export interface ISocketCashoutValueUpdate {
  betId: string;
  cashoutValue: string;
  cashoutStatus: string;
  shouldActivate?: boolean;
}
export interface ISocketEventFinshedUpdate {
  eventId: string; 
  vod: boolean;
}

export interface ISocketTwoUpUpdate {
  betIds: string[]; 
  selectionId:string;
  twoUpSettled: boolean;
}