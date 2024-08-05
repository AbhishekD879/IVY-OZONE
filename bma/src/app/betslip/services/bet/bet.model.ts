import { ILeg } from '@betslip/services/models/bet.model';
import { FreeBet } from '@betslip/services/freeBet/free-bet';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { Bet } from '@betslip/services/bet/bet';
import { ILiveServChannels } from '@core/models/live-serv-channels.model';
import { IOutcome } from '@core/models/outcome.model';
import { IBetPayout } from '@core/models/bet-payout.model';
import { IStake } from '@betslip/services/betStake/bet-stake.model';
import { IPrice } from '@core/models/price.model';
import { ITokenPossibleBet } from '@bpp/services/bppProviders/bpp-providers.model';

interface IPayout {
  legType: string;
  potential: number|string;
}

export interface IBetPayload extends IBetPayout {
  raw_hcap: string;
  hcap_values: { [key: string]: string; };
  status: string;
  placeBet: boolean;
  started: string;
  errorMsg: string;
  type: string;
  name: string;
  bet: IBetInfo;
  unique_id: string;
  fc_avail?: string;
  tc_avail?: string;
}

export interface IOddsBoost {
  betBoostMaxStake: string;
  betBoostMinStake: string;
  enhancedOddsPrice: string;
  enhancedOddsPriceDen: string;
  enhancedOddsPriceNum: string;
  expiry: string;
  id: string;
  offerName: string;
  type: string;
  value: string;
  tokenPossibleBets: ITokenPossibleBet[];
  freebetOfferType: string;
  enhancedOdds?: IEnhancedOdds[];
  sorting: ISorting;
}

export interface IEnhancedOdds {
  num: string;
  den: string;
  dec: string;
  id: string;
  documentId?: string;
}

export interface IBet {
  allLegs: ILeg[];
  betOffer?: { isAccaValid?: boolean; };
  docId: string;
  errs?: IBetError[];
  error?: string;
  errorMsg?: string;
  freeBets: FreeBet[];
  legIds: string[];
  lines: number;
  isMocked: boolean;
  eachWayAvailable: string;
  payout: IPayout[];
  placed?: IBetPlaced;
  stake?: BetStake;
  type: string;
  uid: string;
  winPlace: string;
  oddsBoost?: IOddsBoost;
  oddsBoosts?: IOddsBoost[];
  price?: IBetPrice;
  maxPayout?: string;
  lottoData?: any;
}

export interface IBetPlaced {
  id: string;
  docId: string;
  time?: Date;
  confirmed: boolean;
  settled?: boolean;
  provider: string;
  receipt?: string;
  expectedAt?: string;
}


export interface IEventIdsObject {
  outcomeIds: number[];
}

export interface IBetInfo {
  Bet: Bet;
  stakeMultiplier: number;
  stake: BetStake;
  error: string;
  errorMsg: string;
  type: string;
  typeInfo: string;
  potentialPayout: number;
  liveServChannels: ILiveServChannels;
  eventIds: ILeg[] | IEventIdsObject;
  disabled: boolean;
  isRacingSport: boolean;
  outcomes?: Partial<IOutcome>[];
  outcomeId: string;
  outcomeIds: string[];
  handicapError: IBetError;
  combiType: string;
  combiName: string;
  price: IPrice;
  isSP: boolean;
  isSPLP?: boolean;
  pricesAvailable?: boolean;
  legType?: string;
  oddsBoost?: IOddsBoost | boolean;
  isSelected?: boolean;
  isFCTC?: boolean;
  time?: Date;
  localTime?: string;
  eventName?: string;
  id?: string;
  isSuspended?: boolean;
  sport?: string;
  isEachWayAvailable?: boolean;
  eachWayFactorNum?: string;
  eachWayFactorDen?: string;
}

export interface IBetDoc {
  id: string;
  documentId: string;
  betTypeRef: { ordering: string; id: string; };
  freebet: FreeBet[];
  legRef?: ILeg[];
  leg?: ILeg;
  lines: { number: number };
  payout: IPayout[];
  stake: IStake;
  betOfferRef?: { isAccaValid?: boolean; };
  timeStamp: string;
  isConfirmed: string;
  isSettled: string;
  provider: string;
  receipt: string;
  confirmationExpectedAt: string;
  eachWayAvailable: string;
  maxPayout?: string;
  [key: string]: any;
}

export interface IBetPrice extends IPrice {
  type: string;
  props: Partial<IPrice>;
}

export interface ISorting {
  type?: string;
  level?: string;
}
