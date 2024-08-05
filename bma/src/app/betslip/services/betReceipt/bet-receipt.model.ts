import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';


export interface IBetReceiptEntity {
  singles: IBetDetail[];
  multiples: IBetDetail[];
}

export interface IBetObject {
  betId: string;
  price: number | null;
  potentialReturn: number | null;
  odds: number | null;
  startTime: string;
  multiBet: boolean;
  receiptId: string;
  betType: string;
  inplay: boolean;
  sport: string;
  competition: string;
  eventName: string;
  eventId: number;
  selection: string;
  selectionId: string;
  marketName: string;
  marketId: string;
}

export interface IBetSelection {
  eventIsLive: boolean;
  hasBPG: boolean;
  hasEachWay: boolean;
  id: string;
  isRacing: boolean;
  isSuspended: boolean;
  outcomesIds: Array<string>;
  price: IOutcomePrice;
  type: string;
  userEachWay: boolean;
  userFreeBet: string;
  userStake: string;
}

export interface IRacingPostQuickbetReceipt {
  enabled: boolean;
  quickBetReceipt: boolean;
  mainBetReceipt: boolean;
}
