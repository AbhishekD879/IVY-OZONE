import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IHandicapOutcome } from '@betslip/models/betslip-bet-data.model';
import { SportsLegPriceModel } from '@betslip/services/sportsLegPrice/sports-leg-price';
import { IGtmEvent } from '@core/models/gtm.event.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { IPrice as IBasePrice } from '@core/models/price.model';
import { IBet } from '@betslip/services/bet/bet.model';

export interface IBetSelection {
  accaBets? : AccaBets[],
  outcomesIds?: string[];
  goToBetslip: boolean;
  price: IOutcomePrice;
  hasBPG?: boolean;
  eventIsLive: boolean;
  isSuspended: boolean;
  winPlace?: string;
  errs?: IBetError[];
  id: number | string;
  outcomes?: IOutcome[];
  params?: IParams;
  type: string;
  typeName: string;
  handicap: IHandicapOutcome | string;
  eachWayOn?: IBetSelection;
  hasEachWay: boolean;
  isRacing: boolean;
  userEachWay: boolean;
  userFreeBet: string;
  userStake: string;
  combi?: string;
  correctPriceType?: string;
  docId?: string;
  details?: IOutcomeDetails | any;
  places?: number | string;
  doNotRemove?: boolean;
  isFCTC?: boolean;
  eventName?: string;

  // dynamic params in betslip
  outcomeId: string | number[];
  GTMObject?: IGtmEvent;
  reuseSelection?: boolean;
  isYourCallBet?: boolean;
  combiName?: string;
  isVirtual?: boolean;
  

  // TODO extend selection for tote
  isTote?: boolean;
  Bet?: IBet;

  eventId: number;
  isOutright: boolean;
  isSpecial: boolean;
  isLotto?: boolean;
}

interface IHandicap {
  type: string;
  raw: string;
  rangeTypeRef: {id: string};
  low: string;
  height: string;
}

export interface IParams {
  id?: string;
  combi?: string;
  docId: string;
  eventIsLive?: string;
  handicap?: IHandicap;
  legParts: ILegPart[];
  outcomes: IOutcome[];
  outcomeIds?: string[];
  price: IBasePrice;
  type?: string;
  isRacing?: boolean;
  isSuspended?: boolean;
  winPlace?: string;
  userStake?: number;
  userEachWay?: boolean;
  places?: string;
  GTMObject?: IGtmEvent;
  outcomesIds?: string[];
}

export interface IParseResponse {
  docId: string;
  legParts: ILegPart[];
  winPlace: string;
  price: SportsLegPriceModel;
  combi: string;
  outcomes: {
    id: string;
    price: SportsLegPriceModel
  }[];
}

export interface AccaBets {
  userStake: string;
  betType: string;
  id: string;
  betLineSummary: BetLineSummary;
  betTypeRef: { id: string };
  lines: { number: number };
  winningAmount: string;
  stake: string;
}
export interface BetLineSummary {
  betTypeRef: { id: string };
  lines: { number: number }
  numPicks: number;
}