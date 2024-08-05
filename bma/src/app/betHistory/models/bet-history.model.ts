import {
  IBet, IPoolBetDetailLeg, IPoolBetDetailLegPart, IWinnings,
  IRefund, IPotentialPayout, IEachWayTerms,
  IStake, IPrice, IFreeBetTokens
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryOutcome, IOutcome } from '@core/models/outcome.model';
import { IHandicapOutcome } from '@betslip/models/betslip-bet-data.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';

export interface IBetHistoryEachWayTerms extends IEachWayTerms {
  value: string;
}

export interface IBetHistoryHandicap extends IHandicapOutcome {
  value: number;
}

export interface IBetHistoryPart extends IPoolBetDetailLegPart {
  outcome: IBetHistoryOutcome; // TODO actually is `IBetHistoryOutcome | IBetHistoryOutcome[]`
  name: string;
  handicap: IBetHistoryHandicap[] | string;
  eachWayTerms: IBetHistoryEachWayTerms[] | IBetHistoryEachWayTerms;
  eachWayPlaces: string;
  price?: IPrice[];
  startTime?: string;
  eventId?: string;
  toteEventId?: string;
  marketId?: string;
  eventInfo?: string;
  outcomeId?: string;
  priceNum?: number;
  priceDen?: number;
  eventDesc?: string;
  eventMarketDesc?: string;
  dispResult: string;
  eachWayNum?: number;
  eachWayDen?: number;
  isBog?: boolean;
  [key: string]: any;
}

export interface IBetHistoryLeg extends IPoolBetDetailLeg {
  poolPart: IBetHistoryPart[];
  part?: IBetHistoryPart[];
  legSort?: { code: string; } | string;
  name: string;
  legType?: {
    code: string;
  };
  isWidgetLiveStreamOpened: boolean;
  orderedOutcomes?: IBetHistoryOutcome[];
  status?: string;
  cashoutId?: string;
  raceNumber?: string;
  eventEntity?: ISportEvent;
  noEventFromSS?: boolean;
  backupEventEntity?: ISportEvent;
  isBetSettled?: boolean;
  allSilkNames?: string[];
  isEventEntity?: boolean;
  id?: string;
  type?: string;
  adjustedResult?: string;
  isResulted?: boolean;
  removedLeg?: boolean;
  resultedBeforeRemoval?: boolean;
  removing?: boolean;
  documentId?: string;
  outcomeResult?: string;
  outcomeClass?: string;
  eventId?: string;
  toteEventId?: string;
  marketId?: string;
  legNo?: string;
  isCashOutUnavailable?: boolean;
  isLiveStreamOpened?: boolean;
  is_off?: boolean;
  myBetsAreas?: IMyBetsAreas;
  matchCmtryDataUpdate?: IMatchCmtryData;
  matchCmtryTimeInterval?: number;
  deadHeatWinDeductions?: string;
  deadHeatEachWayDeductions?: string;
}

export type IMyBetsAreas = {
  [ key in MYBETS_AREAS  ] ?: { isMatchCmtryDataAvailable?: boolean};
 }
export interface IBetType {
  name: string;
  code: string;
}
export interface IBetTags {
  betTag: IBetTag[]
}
export interface IBetTag {
  tagName: string;
  tagValue: string;
}
export interface IBetHistoryBet extends IBet {
  id: number;
  poolLeg?: IBetHistoryLeg[];
  leg?: IBetHistoryLeg[];
  ycStatus?: number;
  ycBet?: boolean;
  settled?: string;
  status?: string;
  winnings?: IWinnings;
  refund?: IRefund;
  poolType?: string;
  totalStake?: string;
  totalReturns?: string;
  outcome?: string[];
  currency?: string;
  lotteryName?: string;
  potentialPayout?: IPotentialPayout | IPotentialPayout[] | string;
  legType?: string;
  externalRefId?: {
    value: string;
    lotteryDraw:string;
  };
  partialCashoutAvailable?: string;
  data?: { id: string }[];
  betType?: IBetType | string;
  betTags?: IBetTags;
  poolName?: string;
  poolSource?: string;
  numLines?: number;
  numLegs?: number;
  betGroupOrder?: string;
  betGroupId?: string;
  betGroupType?: string;
  date?: string;
  stake: IBetHistoryStake | string;
  freebetTokens?: IFreeBetTokens;
  cashoutStatus?: string;
  cashoutValue?: string & ICashoutValue;
  currencySymbol?: string;
  betId?: string;
  type?: string;
  source: string;
  isCashOutUnavailable?: boolean;
  isPartialCashOutAvailable?: boolean;
  isCashOutBetError?: boolean;
  isPartialActive?: boolean;
  allSilkNames: string[];
  removedLegs?: IBetHistoryLeg[];
  markets?: IMarket[];
  events?: ISportEvent[];
  event?: string[];
  outcomes?: IOutcome[];
  isSuspended?: boolean;
  emaPriceError?: boolean;
  isUkToteBet?: boolean;
  isAccaEdit?: boolean;
  isToteBet?: boolean;
  inProgress?: boolean;
  validateBetStatus?: 'pending' | 'ok' | 'fail';
  totalStatus?: string;
  settledAt?: string;
  isCashOutedBetSuccess?: boolean;
  cashoutSuccessMessage?: string;
  resetCashoutSuccessState?: Function;
}

export interface ICashoutValue {
  amount?: string;
  status?: string;
}

export interface ICashoutError {
  errorCode: string;
  errorDictionary: string;
}

export interface IPageBets {
  bets: IBetHistoryBet[];
  pageToken: string;
  timeStamp?: string;
}

export interface IFilteredPageBets {
  data: IPageBets;
  filter: string;
}

export interface IBetCount {
  betCount: string;
}

export type IBetHistoryPoolBet = ITotePoolBet | IFootballJackpotBet;

interface ITotePoolBet extends IBetHistoryBet {
 new(bet: IBetHistoryBet,
     service1: any,
     service2: any,
     service3: any,
     service4: any,
     service5: any,
     service6: any,
     service7: any);
}

export interface IFootballJackpotBet extends ITotePoolBet {
  numSelns: string;
}

export interface IDetailedBetObject {
  betType: string;
  poolType: string;
  poolName: string;
  lines: number;
  receipt: string;
  stake: string;
  totalStake: number;
  tokenValue: number;
  winLines: string;
  currency: string;
  legs: any[];
  numLegs: number;
}

export interface IBetReturns {
  returns: number;
  refund: number;
  estReturn: number;
}

export interface IBetReturnsValue {
  status: string;
  value: number | string;
}

export interface IBetHistoryStake extends IStake {
  value?: number;
  tokenValue?: number;
  poolStake?: number;
  stakePerLine?: string;
  freebetOfferCategory?: string;
}

export interface ILegItemPrice {
  startingPrice: IBasePrice;
  price: IPriceTaken;
}

export interface IBasePrice {
  num: number;
  den: number;
}

interface IPriceTaken extends IBasePrice { dec?: number; }

export interface IMatchCmtryData {
  matchCmtryEventId?: string;
  matchfact?: string;
  feed?: string;
  varIconData?: IVarIconData;
  teamName?: string;
  playerName?: string;
  playerOnName?:string;
  playerOffName?:string;
  minutes?:string;
  clock?:string;
}
export interface IVarIconData {
  svgId?: string;
  description?: string;
}
export interface IRunnerStallNumber {
  runnerNumber?: string;
  stallNumber?: string
}

export interface ICelebration {
  congratsBannerImage?: string,
  displayCelebrationBanner?: boolean,
  celebrationMessage?: string,
  winningMessage?: string,
  cashoutMessage?: string,
  duration?: number
}

export interface ISiteCoreBanner {
  type?: string;
  teasers?: ISiteCoreTeaserFromServer[];
}