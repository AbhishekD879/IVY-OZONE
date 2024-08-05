import { IQuickbetSelectionPriceModel } from './quickbet-selection-price.model';
import { IQuickbetDeltaObjectModel } from './quickbet-delta-object.model';
import { IClaimedOffer } from '@bpp/services/bppProviders/bpp-providers.model';
import { IBetTags } from '@app/betHistory/models/bet-history.model';

export interface IQuickbetReceiptModel {
  receipt?: IQuickbetReceiptDetailsModel[];
  error?: IQuickbetReceiptErrorModel;
}

export interface IQuickbetReceiptErrorModel {
  code: string;
  description: string;
  subErrorCode?: string;
  handicap?: string;
  stake?: {
    maxAllowed: number;
    minAllowed?: number;
  };
  price?: IQuickbetDeltaObjectModel;
}

export interface IQuickbetReceiptDetailsModel {
  bet?: IQuickbetReceiptBetModel;
  legParts?: IQuickbetReceiptLegPartsModel[];
  payout?: IQuickbetReceiptPayoutModel;
  price?: IQuickbetSelectionPriceModel;
  receipt?: { id: string; };
  betId?:string;
  oddsBoost?: boolean;
  stake?: IQuickbetReceiptStakeModel;
  oddsValue?: string;
  selections?: boolean;
  error?: string;
  errorCode?: string;
  date?: string;
  isBir?: boolean;
  claimedOffers?: IClaimedOffer[];
  betTags?: IBetTags;
  freebetId?: number;
  footballAlertsVisible?: boolean;
  footballBellActive?: boolean;
  categoryId?: string;
}

interface IQuickbetReceiptBetModel {
  id: number;
  isConfirmed: string;
  cashoutValue: string;
}

export interface IQuickbetReceiptLegPartsModel {
  eventDesc: string;
  marketDesc: string;
  outcomeDesc: string;
  outcomeId: string;
  handicap?: string;
  eachWayNum?: string;
  eachWayDen?: string;
  eachWayPlaces?: string;
}

interface IQuickbetReceiptPayoutModel {
  potential: string;
}

export interface IQuickbetReceiptStakeModel {
  amount: string;
  freebet?: string;
  stakePerLine: string;
  freebetOfferCategory?: string;
}

export interface IYCBetReceiptModel {
  selection: {
    freeBetOfferCategory?: string;
    potentialPayout: string;
    oldOddsValue: string;
    freebet: { freebetTokenValue: string; };
  };
  data: { receipt: { id: string; }; totalStake: string; date: string; betId: string };
}
