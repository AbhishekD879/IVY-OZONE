import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IPoolBet } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IToteBet extends IBetSelection {
  channelIds: string[];
  events: IRacingEvent[];
  isTote: boolean;
  outcomes: IOutcome[];
  poolBet: IPoolBet;
  toteBetDetails: IToteBetDetails;
  poolCurrencyCode: string;
}

export interface IToteLeg {
  eventTitle: string;
  name: string;
  outcomes: IOutcome[];
  svgId?: string;
}

export interface IToteBetDetails {
  poolName: string;
  stakeRestrictions: IStakeRestrictions;
  betName?: string;
  correctedDay?: string;
  eventTitle?: string;
  isPotBet?: boolean;
  numberOfLines?: number;
  orderedLegs?: IToteLeg[];
  orderedOutcomes?: IOutcome[];
  showOrderPosition?: boolean;
  svgId?: string;
}

export interface IStakeRestrictions {
  maxStakePerLine: string;
  maxTotalStake: string;
  minStakePerLine: string;
  minTotalStake: string;
  stakeIncrementFactor: string;
}

export interface IfreebetOfferCategories {
  freebetOfferCategory: string;
}

export interface ItokenPossibleBet {
  betId: string;
  betLevel: string;
  betType: string;
  channels: string;
  inPlay: string;
  name: string;
}

export interface ItokenPossibleBets {
  betId: string;
  betLevel: string;
  betType: string;
  channels: string;
  inPlay: string;
  name: string;
}
export interface ItoteFreeBets {
  freebetAmountRedeemed: string;
  freebetMaxStake: string;
  freebetMinStake: string;
  freebetOfferCategories: IfreebetOfferCategories; 
  freebetOfferDesc: string;
  freebetOfferId: string;
  freebetOfferName: string;
  freebetOfferType: string;
  freebetTokenAwardedDate: string;
  freebetTokenDisplayText: string;
  freebetTokenExpiryDate: string;
  freebetTokenId: string;
  freebetTokenStartDate: string;
  freebetTokenType: string;
  freebetTokenValue: string;
  tokenId: string;
  tokenPossibleBet: ItokenPossibleBet;
  tokenPossibleBets: ItokenPossibleBets[];
}
