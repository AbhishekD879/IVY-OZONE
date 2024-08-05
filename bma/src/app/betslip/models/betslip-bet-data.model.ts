import { IBet, ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetOffer } from '@betslip/services/acca/acca.models';
import { Bet } from '@betslip/services/bet/bet';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { ILegList } from '@betslip/services/models/bet.model';
import { IComplexBet } from '@core/models/complex-bet.model';
import { IOutcome } from '@core/models/outcome.model';
import { IPrice } from '@core/models/price.model';
import { IFreeBet, IFreeBetGroupObj } from '@betslip/services/freeBet/free-bet.model';

export interface IBetslipBetData extends IComplexBet {
  isConfirmed: boolean;
  isSelected: boolean;
  isTraderDeclined: boolean;
  isTraderAccepted: boolean;
  isTraderOffered: boolean;
  isTraderChanged: boolean;
  isOfferRemovable?: boolean;
  traderChangedPriceType: boolean;
  traderChangedLegType: boolean;
  traderChangedOdds: boolean;
  traderChangedStake: boolean;
  overaskMessage: string;
  betId: number;
  outcomeId: string;
  combiName: string;
  dependsOn: number;
  masterBetId?: number;
  selectedFreeBet: any;
  availableFreeBets?: IFreeBet[];
  groupedFreebets?: IFreeBetGroupObj;
  availableFanzone?:IFreeBet[];
  availableBetTokens?: IFreeBet[];
  freeBetTooltipAvailable: boolean;
  oldLegs: IBetslipLeg[];
  legType: string;
  isEachWay: boolean;
  potentialPayout: string;
  eachWayFactorNum: number;
  eachWayFactorDen: number;
  children?: number[];
  tokenValue?: number;
  maxPayout?: string;
}

export interface IBetslipPairs {
  betData: IBetslipBetData;
  bet: IBet;
}

export interface IBetslipLeg {
  outcomeId: number | string;
  price: { props?: IPrice } & IPrice;

  traderChangedPrice?: boolean;
  changedPrice?: IPrice;
  outcome?: IOutcome;
  firstOutcomeId?: string;
  parts?: IBetslipLegPart[];
  sportsLeg?: {
    legPart: ILegPart[];
    price: IPrice
  };
  docId?: string;
  betData?: any;
}

export interface IBetslipLegPart {
  outcome: IOutcome;
}

export interface IBetslipState {
  off: string;
  onTradersReview: string;
  traderMadeDecision: string;
  customerActionTimeExpired: string;
}

export interface IHandicapOutcome {
  type: string;
  raw: string;
}

export interface IBetslipData {
  bets: Bet[];
  legs?: ILegList;
  errs?: IBetError[];
  betOffers?: IBetOffer[] | string;
  tempBets?: Bet[];
  docId?: number;
}
