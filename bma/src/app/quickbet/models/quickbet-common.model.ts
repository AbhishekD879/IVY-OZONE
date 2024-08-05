// QB Bet Model
import { IQuickbetSelectionPriceModel } from './quickbet-selection-price.model';
import { IGtmEvent } from '@core/models/gtm.event.model';

export interface IQuickbetIdModel {
  id: string;
}

export interface IQuickbetBetModel {
  addr: string;
  betTypeRef: IQuickbetIdModel;
  cashoutValue: IQuickbetCashoutValue;
  documentId: string;
  id: number;
  isConfirmed: string;
  isReferred: string;
  isSettled: string;
  leg: IQuickbetLeg[];
  lines: IQuickbetLines;
  payout: IQuickbetPayout[];
  receipt: string;
  stake: IQuickbetStake;
  timeStamp: string;
}

interface IOutcomeRef {
  eventDesc: string;
  id: string;
  marketDesc: string;
  outcomeDesc: string;
}

interface IQuickbetCashoutValue {
  amount: string;
}

interface IQuickbetPayout {
  bonus: string;
  potential: string;
  refunds: string;
  winnings: string;
}

interface IQuickbetStake {
  amount: string;
  currencyRef: IQuickbetIdModel;
  stakePerLine: string;
}

interface IQuickbetLeg {
  documentId: string;
  sportsLeg: IQuickbetSportsLeg;
}

interface IQuickbetSportsLeg {
  legPart: ILegPartModel[];
  outcomeCombiRef: IQuickbetIdModel;
  price: IQuickbetSportsLegPrice;
  prices: IQuickbetSportsLegPrice[];
  winPlaceRef: IQuickbetIdModel;
}

export interface ILegPartModel {
  outcomeRef: IOutcomeRef;
}

export interface IQuickbetSportsLegPrice {
  priceDen: string;
  priceNum: string;
  priceTypeRef: IQuickbetIdModel;
}

interface IQuickbetLines {
  number: number;
}

export interface ISelectionForStorageModel {
  outcomesIds: string[];
  userStake: string;
  userEachWay: boolean;
  userFreeBet: string;
  goToBetslip: boolean;
  id: string;
  price: IQuickbetSelectionPriceModel | { priceType: string; };
  type: string;
  typeName: string;
  eventIsLive: undefined | boolean;
  hasBPG: boolean;
  hasEachWay: boolean;
  isSuspended: boolean;
}

export interface IQuickbetOddsSelectorModel {
  name: string;
  value: string;
}

export interface IQuickbetOverlayStateModel {
  overlay?: boolean;
  spinner?: boolean;
}

export interface IBetslipSelection {
  outcomeId: number[];
  userEachWay: boolean;
  userStake: null | string;
  type: string;
  price: IQuickbetSelectionPriceModel;
  GTMObject: IGtmEvent | null;
  isVirtual?: boolean;

  eventId: number;
  isOutright: boolean;
  isSpecial: boolean;
}

export interface ISBbetslipGATracking {
  GTMObject: IGtmEvent | null;
  outcomeId: string[] | number[]
}