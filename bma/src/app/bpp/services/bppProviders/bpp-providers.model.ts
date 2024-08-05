import {
  ICheckVideoStreamRequest,
  ICheckVideoStreamResponse
} from '@app/bpp/services/bppProviders/models/check-video-strem.model';
import { Bet } from '@betslip/services/bet/bet';
import { IBetDoc } from '@betslip/services/bet/bet.model';
import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';
import { ILegList } from '@betslip/services/models/bet.model';
import { ISportEvent } from '@core/models/sport-event.model';

import { IPrice as IBasePrice } from '@core/models/price.model';
import { IOutcome, IBetHistoryOutcome } from '@core/models/outcome.model';
import {
  IBetHistoryBet,
  IBetHistoryLeg,
  IBetHistoryStake,
  IBetHistoryPart
} from '@app/betHistory/models/bet-history.model';
import { I24BppResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { IFreebet } from '@bma/components/models/freebet.model';
import { IUserSelectionDetail } from '@lazy-modules/freeRide/models/free-ride';
import { IBetpackLivServeResponse, IfreebetOfferLimits  } from '@root/app/betpackMarket/components/betpack-liveServe.model';

export type IFreebetsTypes = 'SPORTS' | 'ACCESS' | 'BETBOOST';

export interface IPostBody {
  username: string;
  token: string;
}

export interface IRespAccountValidate {
  userName: string;
  accountNo: string;
  status: string;
  firstName: string;
  lastName: string;
  currency: string;
  maxStakeScale: string;
  title: string;
  gender: string;
  dob: string;
  postcode: string;
  channel: string;
  accountType: string;
  crDate: string;
  language: string;
  custId: string;
  temporaryPassword: string;
  temporaryPin: string;
  token: string;
  lastBet: string;
  privateMarkets: string[] & {
    data: IFreebet[]
  };
  betBoosts: string[] & {
      data: IFreebet[];
  };
  freeBets: string[] & {
      data: IFreebet[];
  };
  error?: string;
}

export interface IDocRef {
  documentId: string;
  sportsLeg?: ISportsLeg;
}

export interface IPrice {
  den?: number;
  num?: number;
  priceTypeRef?: IIdRef;
  type?: string;
  priceDecimal?: string;
  priceNum?: string;
  priceDen?: string;
  lp_num?: string;
  lp_den?: string;
  priceStartingNum?: string;
  priceStartingDen?: string;
  priceType?: {
    code: string
  };
}

export interface IPriceUpdate {
  id: string;
  updatePayload: IPrice;
}

export interface IStake {
  currencyRef: IIdRef;
  minAllowed?: string;
  maxAllowed?: string;
  amount?: string;
  stakePerLine?: string;
  value?: number;
  freebetOfferCategory?: string;
}

interface ISlipPlacement {
  ipAddress?: string;
  channelRef: IIdRef;
  IPAddress?: string;
}

export interface IBetslip {
  documentId: string | number;
  clientUserAgent: string;
  stake: IStake;
  slipPlacement: ISlipPlacement;
  betRef: IDocRef[];
  customerRef?: string;
  isAccountBet?: IYesNo | string;
}

export interface IRangeBase {
  low: string;
  high: string;
  rangeTypeRef?: { id: number };
  id?: string;
  type?: string;
}

interface ISubscription {
  number: number;
  free: number | string;
  frequency?: string;
}

export interface IIdRef {
  id: string | number;
}

export interface IOutcomeRef {
  id: string;
  outcomeDesc?: string;
  eventDesc?: string;
  marketDesc?: string;
  marketId?: string;
  eventId?: string;
}

export interface IEachWayTerms {
  eachWayPlaces: string;
}

export interface ILegPart {
  places?: string;
  outcomeRef: IOutcomeRef;
  range?: IRangeBase;
  outcome?: string | IOutcome;
  legType?: string;
  eachWayTerms?: IEachWayTerms[];
  priceNum?: string;
  priceDen?: string;
  priceType?: string;
}

export interface ISportsLeg {
  winPlaceRef: IIdRef;
  legPart: ILegPart[];
  price: IPrice & IBasePrice;
  outcomeCombiRef?: IIdRef;
}

interface IPoolLeg {
  poolRef: { id: string };
  legPart: ILegPart[];
}

export interface ILotteryLeg {
  picks: string;
  gameRef: IIdRef;
  sortRef: IIdRef;
  drawRef: IIdRef;
  subscription: ISubscription;
}

export interface ILeg {
  documentId: string;
  id?: string;
  docId?: string;
  legNo?: string;
  sportsLeg?: ISportsLeg;
  poolLeg?: IPoolLeg;
  removedLeg?: boolean;
  lotteryLeg?: ILotteryLeg;
  parts?: ILegPart[] | any[];
  part?: ILegPart[];
  firstOutcomeId?: string;
}

interface ILines {
  number: number;
}

export interface ILegRef {
  documentId?: string | number;
  ordering?: string;
}

interface IBetTypeRef {
  ordering?: string;
  id: string;
}

interface IEntityRef {
  id: string;
  documentId: string;
  provider: string;
  addr: string;
  version: string;
  ordering: number;
  offerType: string;
  betTypeRef: IBetTypeRef;
  trigger: IIdRef;
}

interface IPayout {
  bonus: string;
  refunds: string;
  winnings: string;
  potential: string;
  legType: string;
}

interface IFBet extends IIdRef {
  offerName: string;
  value: string;
  expiry: string;
  type?:string;
}

interface ISettleInfo {
  value: string;
}

interface IPartialCashout {
  available: string;
  status: string;
}

interface IUplift {
  code: string;
  value: string;
}

export interface ILegChange {
  legNo?: string;
  priceNum: string;
  priceDen: string;
  eachWayNum?: string;
  eachWayDen?: string;
  eachWayPlaces?: string;
  priceType?: string;
  priceTypeRef?: IIdRef;
}

export interface IBetTermsChange {
  date: string;
  changeNo: string;
  reasonCode: string;
  desc: string;
  userId: string;
  userName: string;
  stakePerLine: string;
  stake: IStake;
  potentialPayout: IPotentialPayout;
  winnings: IWinnings;
  cashoutValue: string;
  cashoutDate: string;
  cashoutType: string;
  cashoutLocation: string;
  legChange: ILegChange[];

  // Dynamic params
  stakeUsed?: string;
}

export interface ILottoPayload {
  betslip: IBetslip;
  leg: ILotteryLeg[];
  bet: betRef[];
}

export interface betRef {
  documentId: string | number;
  betTypeRef: IBetTypeRef;
  stake: IStake;
  lines: ILines;
  legRef: ILegRef[]
}
interface IManualBetDetail {
  toSettleAt: string;
  description: string;
}

export interface IBet {
  betOfferRef?: IEntityRef;
  addr?: string;
  documentId: string;
  cashoutBetId?: string;
  newBetStake?: string;
  er?: string;
  id?: number;
  isConfirmed?: IYesNo;
  isFunded?: IYesNo;
  isOffer?: IYesNo;
  isCancelled?: IYesNo;
  isReferred?: IYesNo;
  isSettled?: IYesNo;
  isCashedOut?: IYesNo;
  receipt?: string;
  provider?: string;
  settleDate?: string;
  initialReturns?: string;
  timeStamp?: string;
  confirmationExpectedAt?: string;
  offerExpiresAt?: string;
  // splitted linked parent betID
  dependsOn?: string;
  // splitted not linked and linked base betID
  masterBetId?: string;
  tokenValue?: string;
  betslipRef?: IDocRef;
  betTypeRef: IBetTypeRef;
  stake: IStake | IBetHistoryStake | string;
  payout?: IPayout[];
  lines: ILines;
  cashoutStatus?: string;
  cashoutValue?: ICashoutValue & string;
  leg?: ILeg[] | IBetHistoryLeg[];
  cashoutBetDelayId?: string;
  legRef: ILegRef[];
  freebet?: IFBet[];
  partialCashout?: IPartialCashout;
  oxiStatusPending?: boolean;
  numLinesVoid?: string;
  numLinesWin?: string;
  numLinesLose?: string;
  asyncStatus?: string;
  asyncDesc?: string;
  asyncOriginalStake?: string;
  placedBy?: string;
  userId?: string;
  bonus?: string;
  tax?: string;
  taxType?: string;
  taxRate?: string;
  settleInfoAttribute?: string;
  paid?: string;
  uniqueId?: string;
  winnings?: IWinnings[] | IWinnings;
  refund?: IRefund[] | IRefund;
  potentialPayout?: IPotentialPayout[] | IPotentialPayout | string;
  sogeiInfo?: ISogeiInfo;
  settleInfo?: ISettleInfo;
  uplift?: IUplift;
  betTermsChange?: IBetTermsChange[];
  manualBetDetail?: IManualBetDetail[];
  offer?: IBet;
  claimedOffers?: IClaimedOffer[];
  maxPayout?: string;
}

export interface IClaimedOffer {
  offerCategory: string;
  offerId: string;
  status: string;
}

export interface IBetRef extends IIdRef {
  provider: string;
  documentId?: string;
}

export interface IBetError {
  outcomeRef?: IIdRef;
  errorDesc?: string;
  subErrorCode?: string;
  failureDescription?: string;
  code?: string;
  handicap?: number;
  betRef?: IBetRef[];
  cashoutDelay?: string;
  cashoutBetDelayId?: string;
  price?: IPrice[];
  subCode?: string;
}

export interface IBetsResponse {
  betslip: IBetslip;
  bet: IBet[];
  leg?: ILeg[];
  betError?: IBetError[];
  errs?: IBetError[];
  bets?: IBet[];
  legs?: ILeg[];
}

export interface IBetsRequest {
  betslip: IBetslip;
  leg?: ILeg[];
  bet: IBet[];
}

export interface IReadBetRequest {
  customerRef?: IIdRef;
  betRef: IBetRef[];
}

export interface IReadBetResponse {
  betError: IBetError;
  bet: IBet[];
}

interface ICashoutValue {
  value?: string;
  amount?: string;
  status?: string;
  reason?: string;
  partialCashoutAmount?: string;
  partialCashoutPercentage?: string;
  currencyRef?: IIdRef;
}

export interface ICashoutBetRequest {
  customerRef?: IIdRef;
  betRef: IBetRef;
  channelRef: IIdRef;
  cashoutValue: ICashoutValue;
}

export interface ICashoutBetResponse {
  betError: IBetError;
  bet: IBet;
}

interface IOfferBetActionRef {
  id: string;
}

export interface IOfferBetAction {
  betRef: IBetRef;
  offerBetActionRef: IOfferBetActionRef;

  // dynamic params in betslip overask
  status?: string;
  statusMessage?: string;
}

export interface IOfferBet {
  offerBetAction: IOfferBetAction[];
}

interface IClientAuthModel {
  returnToken: IYesNo;
  user: string;
  password: string;
}

/**
 * getBetDetail
 */
export interface IRequestTransGetBetDetail {
  betId: string[];
}

export interface IResponseTransGetBetDetail {
  response: IGetBetDetailResponse;
}

interface IGetBetDetailResponse {
  returnStatus: IStatusResponse;
  respTransGetBetDetail: IRespTransGetBetDetail;
}

interface IRespTransGetBetDetail {
  transFailure: ITransFailure;
  adminMode: string;
  token: string;
  bet: IBetDetail[];
}

export interface IBetOdds {
  frac: string;
  dec: string;
}

export interface IRemovedLegsMap {
  [key: string]: IBetHistoryLeg[];
}

export interface IBetDetail {
  betId: string;
  betType: string;
  betTypeName: string;
  betTermsChange: IBetTermsChange[];
  bonus: string;
  callId: string;
  cashoutStatus: string;
  cashoutValue: string;
  currency: string;
  date: string;
  eventMarket: string;
  eventName: string;
  ipaddr: string;
  isFootball?: boolean;
  leg: Array<IBetDetailLeg>;
  legType: string;
  name: string;
  numLegs: string;
  numLines: string;
  numLinesLose: string;
  numLinesVoid: string;
  numLinesWin: string;
  numSelns: string;
  odds: IBetOdds;
  oddsBoosted: boolean;
  paid: string;
  placedBy: string;
  partialCashoutAvailable?: string;
  potentialPayout: string | number;
  receipt: string;
  refund: string;
  settleInfo: string;
  settled: string;
  settledAt: string;
  source: string;
  stake: string | IStake;
  stakePerLine: string;
  freebetOfferCategory?: string;
  startTime: string;
  asyncAcceptStatus: string;
  status: string;
  tax: string;
  taxRate: string;
  taxType: string;
  stakeValue: number;
  tokenValue: string;
  uniqueId: string;
  userId: string;
  winnings: string;
  claimedOffers?: IClaimedOffer[];
  isFCTC?: boolean;
  isFavouriteAvailable?: boolean;
  excludedDrillDownTagNames?: string;
  betTags?: IBetTag;
  sortType?: string;
  type?: string;
  footballAlertsVisible?: boolean;
  footballBellActive? : boolean;
  details? : Idetails;
  provider? : string;
  availableBonuses:IavailableBonus;
  bets?: any;
  betTypeRef? : any;
}
export interface IavailableBonus {
  availableBonus:IavailableBonusData[];
  }
export interface IavailableBonusData {
  type:string; 
  num_win: string; 
  multiplier : string;
}
export interface Idetails {
  draws:[]  ;
  footballAlertsVisible?: boolean;
  footballBellActive? : boolean;
}

export interface IFreeBetTokens {
  freebetToken: IFreeBetToken;
}

interface IFreeBetToken{
  freebetTokenId: string;
  freebetOfferCategories: IFreebetOfferCategory;
}

interface IStakeDetail {
  type: string;
  value: string;
  currency: string;
  stakePerLine: string;
  tokenValue: string;
}

interface IBetInitial {
  id: string;
  asyncDesc: string;
  asyncOriginalStake: string;
  asyncStatus: string;
  settleInfoAttribute: string;
  betType: IBetType;
  stake: IStakeDetail;
}

type Diff<T extends keyof any, U extends keyof any> =
  ({ [P in T]: P } & { [P in U]: never } & { [x: string]: never })[T];
type Overwrite<T, U> = Pick<T, Diff<keyof T, keyof U>> & U;

export type IBetDetailInitial = Overwrite<IBetDetail, IBetInitial>

export interface IBetDetailLeg {
  legNo: string;
  legSort: string | any;
  odds?: IBetOdds;
  part: Array<IBetDetailLegPart>;
  excludedDrillDownTagNames?: string;
  legType?: { code: string };
  svgId?: string;
  lotteryLeg? : {
    subscription :ISubscription
  };
  status?: string;
  removedLeg?: boolean;
  eventEntity?: ISportEvent;
}
export interface IBetTag {
  betTag?: Array<IBetTagDetail>;
}
export interface IBetTagDetail {
  tagName: string;
  tagValue: number;
}
export interface IBetTermsChange {
  changeNo: string;
  date: string;
  desc: string;
  reasonCode: string;
}

export interface IOpenBetsCount {
  count: number;
  moreThanTwenty: boolean;
}

export interface IBetDetailLegPart {
  birIndex: string;
  deadHeatEachWayDeductions: string;
  deadHeatWinDeductions: string;
  description: string;
  dispResult: string;
  eachWayDen: string;
  eachWayNum: string;
  eachWayPlaces: string;
  event: ISportEvent;
  eventClassName: string;
  eventDesc: string;
  eventId: string;
  eventMarketDesc: string;
  eventMarketSort: string;
  eventTypeDesc: string;
  fbResult: string;
  handicap: string;
  isFootball?: boolean;
  marketId: string;
  outcome?: string | IOutcome;
  outcomeId: string;
  partNo: string;
  priceDen: string;
  priceNum: string;
  priceType: string;
  result: string;
  resultConf: string;
  resultPlaces: string;
  rule4Deductions: string;
  runnerNum: string;
  startPriceDen: string;
  startPriceNum: string;
  startTime: string;
  eventCategoryId?: string;
  deduction?: IDeduction[];
  isBog?: boolean;
}

export interface IRequestTransGetBetDetails {
  cashoutBets: string;
  status: string;
  returnPartialCashoutDetails: string;
  filter: string;
}

export interface IMatchDayRewardsParamsRequest {
  returnOffers: string;
  returnFreebetTokens: string;
}

interface IRespTransGetBetDetails {
  bets: IBetDetail[];
}

interface IGetBetDetailsResponse {
  returnStatus: IStatusResponse;
  respTransGetBetDetails: IRespTransGetBetDetails;
}

export interface IResponseTransGetBetDetails {
  response: IGetBetDetailsResponse;
}

/**
 * placePoolBet
 */
export interface IPoolBetPlacementRequest {
  channel: string;
  clientUserAgent: string;
  fullDetails: string;
  poolBet: IPoolBet[];
}

export interface IPoolBetPlacementResponse {
  betPlacement: IBetPlacement[];
  betFailure?: any[];
  betError?: any;
  token: string;
}

export interface IBetPlacement {
  betId: string;
  betNo: string;
  currency: string;
  numLines: string;
  receipt: string;
  totalStake: string;
  tokenValue?: string;
}

export interface IPoolBet {
  betNo: number;
  poolItem: IPoolBetItem[];
  poolType: string;
  stakePerLine?: any;
  freebetTokenId?: string;
  freebetTokenValue?: string;
}

interface IPoolBetItem {
  position?: string;
  poolId: number;
  outcome: string;
}

/**
 * poolGetDetail
 */
export interface IRequestTransPoolGetDetail {
  poolBetId: string;
}

export interface IResponseTransPoolGetDetail {
  response: IResponsePoolGetDetail;
  version: string;
}

export interface IResponsePoolGetDetail {
  poolBetDetail: { poolBet: IPoolBetDetail[] };
  returnStatus: IStatusResponse;
}

export interface IPoolBetDetail {
  callId: string;
  ccyStake: string;
  currency: string;
  date: string;
  ipaddr: string;
  leg: IPoolBetDetailLeg[];
  numLegs: string;
  numLines: string;
  numLinesLose: string;
  numLinesVoid: string;
  numLinesWin: string;
  numSelns: string;
  paid: IYesNo;
  placedBy: string;
  poolType: string;
  receipt: string;
  refund: string;
  settleInfo: string;
  settled: IYesNo;
  settledAt: string;
  source: string;
  stake: string;
  stakePerLine: string;
  status: string;
  userId: string;
  winnings: string;
  multiples: any[];
  tokenValue?: string;
   
}

export interface IMatchDayRewardsResponse {
  currentBadgeLocation: number;
  placedBetToday: boolean;
  tokenAmount: string;
  freeBetPositionSequence: number[];
  termsAndConditions: string;
  fullTermsURI: string;
  proxyError: IProxyError;
}

export interface IProxyError {
  code: number;
  status: string;
  error: string;
  message: string;
  url: string;
}

export interface IHowItWorks {
  howItWorks: string;
}

export interface IPoolBetDetailLeg {
  description?: string;
  legDesc?: string;
  legNo?: string;
  poolPart?: IPoolBetDetailLegPart[] | IBetHistoryPart[];
  startTime: string;
  track?: string;
  svgId?: string;
}

export interface IDeduction {
  priceType: string;
  value: string;
  type?: string;
}

export interface IPoolBetDetailLegPart {
  partNo: string;
  outcome: IBetHistoryOutcome;
  description: string;
  result: string;
  price?: string[] | IPrice[];
  deduction?: IDeduction[];
}

interface ITransFailure {
  transFailureCode: string;
  transFailureKey: string;
  transFailureReason: string;
  transFailureDebug: string;
}

export interface IStatusResponse {
  message: string;
  code: string;
  debug: string;
}

export interface ITypedValue {
  type: string;
  value: string;
}

export interface ITypedMessage {
  type: string;
  msg: string;
}

interface IReqTransGetPoolBetDetail {
  token: string;
  poolBetId: string[];
}

interface IGetPoolBetDetailRequest {
  reqClientAuth: IClientAuthModel;
  reqTransGetPoolBetDetail: IReqTransGetPoolBetDetail;
}

export interface IRequestTransGetPoolBetDetail {
  request: IGetPoolBetDetailRequest;
}

interface IReqTransGetBetsPlaced {
  token: string;
  eventId: string;
}

interface IGetBetsPlacedRequest {
  reqClientAuth: IClientAuthModel;
  reqTransGetBetsPlaced: IReqTransGetBetsPlaced;
}

export interface IRequestTransGetBetsPlaced {
  request: IGetBetsPlacedRequest;
}

export interface IRespTransGetBetsPlaced {
  bets: IBet[];
  token: string;
  ids?: number[];
}

interface IGetBetsPlacedResponse {
  returnStatus: IStatusResponse;
  respTransGetBetsPlaced: IRespTransGetBetsPlaced;
}

export interface IResponseTransGetBetsPlaced {
  response: IGetBetsPlacedResponse;
}

interface IAuthModel {
  clientAuthModel: IClientAuthModel;
}

interface IGetVideoStreamModel extends IAuthModel {
  accountVideoStreams: IVideoStreamModel;
}

interface IAccountFailureSpecifics {
  content: any[];
}

interface IAccountFailureElement {
  value: string;
}

interface IAccountFailureInfo {
  name: string;
  value: string;
}

interface IAccountFailure {
  accountFailureCode: string;
  externalId: string;
  accountFailureKey: string;
  accountFailureReason: string;
  accountFailureDebug: string;
  accountFailureElement: IAccountFailureElement[];
  accountFailureInfo: IAccountFailureInfo[];
  accountFailureSpecifics: IAccountFailureSpecifics;
}

export interface IVideoStreamModel {
  streamDetails: IStreamDetails;
  eventId: string;
  token: string;
  error: IAccountFailure;
}

interface IStreamDetails {
  startTime: string;
  endTime: string;
  streamId: string;
  providerName: string;
}

interface IStreamResult {
  requestTime: string;
  returnStatus: IStatusResponse;
}

interface IVideoStreamResult extends IStreamResult {
  successModel: IVideoStreamModel;
}

export interface IGetVideoStreamRequest {
  requestModel: IGetVideoStreamModel;
}

export interface IGetVideoStreamResponse {
  result: IVideoStreamResult;
}

export interface INetverifyRequest {
  customerInternalReference?: string;
  merchantScanReference?: string;
  successUrl: string;
  errorUrl: string;
  userReference?: string;
  customerId?: string;
  country?: string;
}

export interface INetverifyResponse {
  timestamp: string;
  authorizationToken: string;
  redirectUrl: string;
  jumioIdScanReference: string;
  httpStatus: string;
  message: string;
  requestURI: string;
  clientRedirectUrl: string;
}

export interface IFreebetTrigger {
  freebetTriggerId: string;
  freebetTriggerType: string;
  freebetTriggerPromoCode: string;
  freebetTriggerRank: string;
  freebetTriggerQualification: string;
  freebetTriggerDescription: string;
  freebetTriggeredDate: string;
  freebetTriggerProgress: string;
  freebetTriggerTarget: string;
  freebetTriggerCumulative: string;
  freebetTriggerRelativeExpiry: string;
  freebetTriggerAbsoluteExpiry: string;
  freebetTriggerMinimumPriceNum: string;
  freebetTriggerMinimumPriceDen: string;
  freebetTriggerDefinesTokenValue: string;
}

/**
 * freebetTrigger
 */
export interface IRequestTransFreebetTrigger {
  value: string;
  source: string;
}

export interface IRequestTransBetpackTrigger {
  value: string;
  source: string;
  extTriggerId: string;
}

export interface IResponseTransFreebetTrigger {
  response: IFreebetTriggerResponse;
  version: string;
  error?: string;
}

export interface IResponseTransBetpackTrigger {
  response: IFreebetTriggerResponse;
  version: string;
  error?: string;
}

export interface IFreebetTriggerResponse {
  freebetResponseModel: IFreebetResponseModel;
  requestTime: string;
  returnStatus: IStatusResponse;
}

export interface IBetPackTriggerResponse {
  freebetResponseModel: IFreebetResponseModel;
  requestTime: string;
  returnStatus: IStatusResponse;
}

interface IFreebetResponseModel {
  freebetCalledTrigger: IFreebetCalledTrigger;
  token: string;
}

interface IFreebetCalledTrigger {
  freebetCalledTriggerId: string;
  freebetTriggerId: string;
}


interface IResult {
  requestTime: string;
  returnStatus: IStatusResponse;
}

interface ITokenRestrictedSet {
  level: string;
  id: string;
}
export interface IFreebetOfferCategory{
  freebetOfferCategory?:string;
}

export interface IFreebetToken {
  formatDate?: string;
  freebetOfferCategories?: IFreebetOfferCategory;
  tokenId?: string;
  freebetTokenId?: string;
  freebetOfferId?: string;
  freebetOfferName?: string;
  freebetOfferDesc?: string;
  freebetTokenDisplayText?: string;
  freebetTokenValue?: string;
  freebetAmountRedeemed?: string;
  freebetTokenRedemptionDate?: string;
  freebetRedeemedAgainst?: string;
  freebetTokenExpiryDate?: string;
  freebetMinPriceNum?: string;
  freebetMinPriceDen?: string;
  freebetTokenAwardedDate?: string;
  freebetTokenAwardedLongDate?: Date;
  freebetTokenStartDate?: string;
  freebetTokenType?: string;
  freebetTokenRestrictedSet?: ITokenRestrictedSet;
  freebetGameName?: string;
  freebetTokenStatus?: string;
  freebetMaxStake?: string;
  currency?: string;
  tokenPossibleBet?: ITokenPossibleBet;
  tokenPossibleBets?: ITokenPossibleBet[];
  freebetOfferType?: string;
  name?: string;
  redirectUrl?: string;
  amount?: string;
  usedBy?: string;
  expires?: string;
  betNowLink?: string;
  categoryName?: string;
  categoryId?: string;
  pending?: boolean;
  tokenPossibleBetTags?: ITokenPossibleBetTags;
  value?: string;
  expireAt?: Date;
  group?: string | number;
  freebetMinStake?:string;
  offerName?: string;
  id?: string;
  expiry?: string;
  type?: string;
  possibleBets?: ITokenPossibleBet[];
  freeBetType?:string;
  svgId?:string;
}

export interface IFreebetGroup {
  [key: string]: IFreebetToken[];
}

export interface ITokenPossibleBet {
  name: string;
  betLevel: string;
  betType: string;
  betId: string | number;
  singleOnly?: string;
  winOnly?: string;
  channels?: string;
  gameClass?: string;
  gameGroupId?: string;
}

interface IFreebetTokenHolder {
  freebetToken: IFreebetToken;
}

export interface IAccFreebetsResponseModel {
  currency: string;
  freebetToken: IFreebetToken[];
  redeemedFreebetTokens?: IFreebetTokenHolder;
  freebetOffer?: IOffer[];
  freebetCalledOffer?: ICalledOffer;
  freebetCalledTrigger?: ICalledTrigger;
  freebetWageringRequirement?: IWageringRequirement;
  error?: IAccountFailure;
  token: string;
}

interface IWageringRequirement {
  tokenId: string;
  freebetTokenId: string;
  freebetWRTarget: string;
  freebetWRBalance: string;
  freebetWRHeldFunds: string;
  freebetWRLockedFundsInitial: string;
  freebetWRLockedFundsBalance: string;
  freebetWRCreationDate: string;
  freebetWRExpiryDate: string;
  freebetWRStatus: string;
  freebetWRId: string;
  freebetWRProvider: string;
  freebetWRInitBalance: string;
}

interface ICalledOffer {
  freebetCalledOfferId: string;
  freebetOfferId: string;
  freebetOfferStatus: string;
  freebetOfferShow: string;
}

interface ICalledTrigger {
  freebetCalledTriggerId: string;
  freebetTriggerId: string;
  freebetOfferId: string;
  freebetTriggerStatus: string;
  freebetNumFulfilledActions: string;
}

export interface IOffer {
  freebetOfferId: string;
  freebetOfferName: string;
  startTime: string;
  endTime: string;
  description: string;
  freebetOfferRepeatable: string;
  entryExpiryTime: string;
  earliestTokenAwardDate: string;
  earliestTokenRedemptionDate: string;
  freebetOfferReward: IOfferReward;
  freebetTrigger: IFreebetTrigger[];
  freebetOfferLimits?: IfreebetOfferLimits;
  freebetOfferContent: IOfferContent;
  offerGroup: IOfferGroup;
}

export interface IOfferGroup{
  offerGroupId: string;
  offerGroupName: string

}

interface IOfferContent {
  contentLinkDisporder: string;
  contentName: string;
  contentType: string;
  contentLocation: string;
  contentDescription: string;
}

interface IOfferReward {
  tokenId: string;
  tokenType: string;
  tokenAmount: string;
  tokenAmountPercent: string;
  tokenAmountMax: string;
}

interface IAccFreebetsResult extends IResult {
  model: IAccFreebetsResponseModel;
  version: string;
}

export interface IAccountFreebetsResponse {
  response: IAccFreebetsResult;
}

interface IToken {
  type: string;
  value: string;
}

export interface IAccountHistoryRequest {
  returnAvaliableFilters: string;
  token: IToken;
  betGroupId: string[];
  filtersOrder: any[];
}

interface IBetBase {
  id: string;
  date: string;
  source: string;
  status: string;
  settled: string;
  settledAt: string;
  receipt: string;
}

export interface IWinnings {
  value: string | number;
}

export interface IRefund {
  value: string | number;
}

export interface IPotentialPayout {
  value: string;
}

interface ISogeiInfo {
  receiptId: string;
  id: string;
  timestamp: string;
  externalWager: string;
  externalReturns: string;
  ticketId: string;
  status: string;
}

interface IBetSummary extends IBetSummaryBase {
  winnings: IWinnings[];
  refund: IRefund[];
  potentialPayout: IPotentialPayout[];
  sogeiInfo: ISogeiInfo;
}

interface IBetType {
  code: string;
  name: string;
}

interface IBetSummaryBase extends IBetBase {
  numLines: string;
  numLegs: string;
  numSelns: string;
  callId: string;
  betType: IBetType;
  stake: IStake;
}

interface IFootballPoolBetSummary {
  id: string;
  subId: string;
  footballPoolName: string;
  date: string;
  source: string;
  settled: string;
  settledAt: string;
  numLines: string;
  numSelns: string;
  stake: IStake;
  winnings: IWinnings;
  refund: IRefund;
}

interface IFootballPoolBet {
  id: string;
}

interface IPoolBetSummary extends IBetBase {
  poolType: string;
  poolName: string;
  numLegs: string;
  numLines: string;
  numSelns: string;
  stake: IStake;
  winnings: IWinnings;
  refund: IRefund;
}

interface ILotteryBet extends IBet {
  id: number;
}

interface IManualAdjustment {
  id: string;
}

interface IPaging {
  blockSize: string;
  token: string;
}

interface IPayment {
  id: string;
}

interface IAccountHistoryPoolBet extends IBet {
  id: number;
  receipt: string;
}

interface ITransfer {
  id: string;
}

interface IWagerReqt {
  id: string;
}

interface IBackgammonBetSummary {
  id: string;
  date: string;
  name: string;
  type: string;
  status: string;
  stake: IStake;
  winnings: IWinnings;
}

interface IBallsBetSummary {
  date: string;
  numDraws: string;
  firstDrawId: string;
  lastDrawId: string;
  desc: string;
  stake: IStake;
  winnings: IWinnings;
}

interface IPayment {
  id: string;
}

interface IRemoteSystem {
  id: string;
  systemName: string;
  gameName: string;
}

interface ITransferSummary {
  id: string;
  date: string;
  amount: string;
  desc: string;
  source: string;
  remoteUniqueId: string;
  remoteAction: string;
  remoteReference: string;
  remoteAccount: string;
  heldAmount: string;
  tokenAmount: string;
  remoteSystem: IRemoteSystem;
  sogeiInfo: ISogeiInfo;
}

interface ILotteryBetSummary {
  id: string;
  subId: string;
  lotteryName: string;
  drawName: string;
  date: string;
  source: string;
  settled: string;
  settledAt: string;
  numLines: string;
  numSelns: string;
  betType: IBetType;
  stake: IStake;
  winnings: IWinnings;
  refund: IRefund;
}

interface IGameSummary {
  id: string;
  date: string;
  finished: string;
  name: string;
  stakes: string;
  winnings: IWinnings;
}

interface IFund {
  id: string;
}

interface IGame {
  id: string;
}

interface IJournalEntry {
  id: string;
  group: string;
  date: string;
  amount: string;
  balance: string;
  refId: string;
  description: string;
}

interface IMethodInfo {
  item: string;
  methodInfo: string;
  value: string;
}

interface IPayMethod {
  id: string;
  nickname: string;
  type: string;
  methodInfo: IMethodInfo;
}

interface IPaymentBase {
  id: string;
  sort: string;
  status: string;
  source: string;
  amount: string;
  commission: string;
  date: string;
  settledAt: string;
  processedAt: string;
  processDate: string;
  ipAddr: string;
  callId: string;
  reversible: string;
  payMethod: IPayMethod;
  sogeiInfo: ISogeiInfo;
}

interface IPaymentSummary extends IPaymentBase {
  subMethod: string;
}

interface IManualAdjustmentSummary {
  id: string;
  date: string;
  amount: string;
  display: string;
  pending: string;
  withdrawable: string;
  type: string;
  desc: string;
}

interface IConfiguration {
  group: IGroup[];
}

interface IIssuerCard {
  id: string;
}

interface IIssuerCardSummary {
  id: string;
  lifecycleId: string;
  issuerTxnId: string;
  issuerMessageType: string;
  messageClass: string;
  messageFunction: string;
  functionCode: string;
  messageTypeDesc: string;
  jrnlDesc: string;
  totalAmount: string;
  crDate: string;
  billAmount: string;
  commissionAmount: string;
  padAmount: string;
  billConvRate: string;
  actionCode: string;
  txnCode: string;
  merchantDate: string;
  merchantCcy: string;
  merchantAmount: string;
  merchantCashback: string;
  merchantName: string;
  merchantCity: string;
  merchantCountry: string;
  desc: string;
  note: string;
}

export interface IAccountHistoryResponse {
  accountFailure?: IAccountFailure;
  betSummary?: IBetSummary[];
  bet: IBetHistoryBet[];
  footballPoolBetSummary?: IFootballPoolBetSummary[];
  footballPoolBet?: IFootballPoolBet[];
  poolBetSummary?: IPoolBetSummary[];
  poolBet?: IAccountHistoryPoolBet[];
  backgammonBetSummary?: IBackgammonBetSummary[];
  transfer?: ITransfer[];
  transferSummary?: ITransferSummary[];
  lotteryBetSummary?: ILotteryBetSummary[];
  lotteryBet?: ILotteryBet[];
  lottoBetResponse?: ILotteryBet[];
  ballsBetSummary?: IBallsBetSummary[];
  gameSummary?: IGameSummary[];
  game?: IGame[];
  payment?: IPayment[];
  paymentSummary?: IPaymentSummary[];
  journalEntry?: IJournalEntry[];
  manualAdjustment?: IManualAdjustment[];
  manualAdjustmentSummary?: IManualAdjustmentSummary[];
  wagerReqt?: IWagerReqt[];
  fund?: IFund[];
  configuration?: IConfiguration[];
  issuerCard?: IIssuerCard[];
  issuerCardSummary?: IIssuerCardSummary[];
  paging: IPaging;
  token: string;
  betListNotNull?: boolean;
}

export interface ICurrencyDetail {
  currency: string;
  currencyName: string;
  minimumDeposit: string;
  maximumDeposit: string;
  minimumWithdrawal: string;
  maximumWithdrawal: string;
  exchangeRate: string;
}

export interface ICurrenciesResponse {
  currencyDetail: ICurrencyDetail;
}

export interface ICurrenciesResponse {
  currencyDetail: ICurrencyDetail;
}

export interface IFreeBetOfferRequest {
  freebetOfferId: string;
}

/**
 * freeBetBetslip
 */
export interface IFreeBetOfferBetslip {
  freebetOfferId: string;
  freebetOfferName: string;
  startTime: string;
  endTime: string;
  description: string;
  freebetOfferCcyCodes: string;
  freebetTrigger: IFreeBetTriggerBetslip[];
  freebetToken: {
    freebetTokenId: string;
    freebetTokenDisplayText: string;
  };
}

export interface IFreeBetTriggerBetslip {
  freebetTriggerId: string;
  freebetTriggerType: string;
  freebetTriggerRank: string;
  freebetTriggerQualification: string;
  freebetTriggerAmount: {
    currency: string;
    value: string;
  };
  freebetTriggerBetType: string;
  freebetTriggerMinPriceNum: string;
  freebetTriggerMinPriceDen: string;
  freebetTriggerMinLegPriceNum: string;
  freebetTriggerMinLegPriceDen: string;
  freebetTriggerMinLoseLegs: string;
  freebetTriggerMaxLoseLegs: string;
  freebetTriggerBonus: string;
  freebetTriggerMaxBonus: string;
  freebetTriggerCalcMethod: string;
}

export interface IFreeBetOfferResponseBetslip {
  response: {
    respFreebetGetOffers: {
      freebetOffer: IFreeBetOfferBetslip[];
    };
    requestTime: string;
    returnStatus: {
      message: string;
      code: string;
      debug: string;
    };
  };
  version: string;
}

export interface IFreebetOffer {
  freebetOfferId: string;
  freebetOfferName: string;
  startTime: string;
  endTime: string;
  description: string;
  freebetOfferRepeatable: IYesNo;
  freebetOfferCcyCodes: string;
  freebetTrigger: IFreebetTrigger[];
  freebetToken: IFreebetToken;
}

export interface IFreeBetOfferResponse {
  freebetOffer: IFreebetOffer[];
}

export interface IBuildBetResponse {
  legs: ILegList;
  betErrors: IBetErrorDoc[];
  bets?: IBetDoc[];
  bet?: IBetDoc[];
  betOfferRef: string;
  outcomeDetails?: IOutcomeDetailsResponse[];
}

export interface IOutcomeDetailsResponse {
  id: string;
  priceNum: string;
  priceDen: string;
  priceType?: string;
  startPriceNum: string;
  startPriceDen: string;
  fbResult:  string;
  eventMarketSort: string;
  handicap: string;
  eachWayNum: string;
  eachWayDen: string;
  eachWayPlaces: string;
  previousOfferedPlaces:string;
  name: string;
  marketId: string;
  marketDesc: string;
  eventId: string;
  eventDesc: string;
  typeId: string;
  typeDesc: string;
  classId: string;
  className: string;
  categoryId: string;
  category: string;
  status: string;
  birIndex: string;
  accMin: string;
  accMax: string;
  isStarted?: boolean;
  isMarketBetInRun?: boolean;
  isLpAvailable?: boolean;
  isSpAvailable?: boolean;
  isGpAvailable?: boolean;
  eventStatusCode?: string;
  marketStatusCode?: string;
  outcomeStatusCode?: string;
  outcomeMeaningMinorCode?: string;
  marketDrilldownTagNames?: string;
  eventDrilldownTagNames?: string;
}

export interface IBuildBetRequest {
  docId: number;
  stake: IStake;
  bets: Bet[];
  legs: ILeg[];
  errs: IBetError[];
  doc: any;
}

export interface IGetBetHistoryRequest {
  detailLevel?: string;
  blockSize?: string | number;
  pagingToken?: string;
  fromDate?: string;
  toDate?: string;
  group?: string;
  betGroupId?: string[] | string;
  pagingBlockSize?: string | number;
}

export interface IValidateBetResponse {
  bet: IValidatedBets[];
  betError?: IBetError[];
}

export interface IValidatedBets {
  id: number;
  betNo: string;
  subjectToCashout: INewStake;
  betMinStake: string;
  betMaxStake: string;
  freebetToken: IFreebetToken[];
  betPotentialWin: string;
  isConfirmed: string;
  confirmationExpectedAt: string;
}

export interface INewStake {
  newBetStake: string;
}

export interface IValidateParams {
  stake: IBetHistoryStake | string;
  cashoutBetId: string;
  currency: string;
  leg: ILeg[];
}

export interface ICashoutBets {
  bets: IBetDetail[];
  fromMS: boolean;
}

export interface ITokenPossibleBetTags {
  tagName?: string;
}

export interface IAccGetLimitsResponse {
  response : IAccGetLimit;
}

export interface IAccGetLimit extends IResult {
  model: IAccGetLimitGroup;
  version: string;
}
export interface IAccGetLimitGroup {
  activeLimits : IAccGetLimits;
}
export interface IAccGetLimits {
  limitEntry : ILimitEntry;
}
export interface ILimitEntry {
  limitId : number;
  limitSort: string;
  limitFrom: string;
  limitTo: string;
  limitRemaining: number;
  limitResetTime: string;
  limitDefinition: ILimitDefinition;
}

export interface ILimitDefinition {
  limitComponent : ILimitComponent;
}
export interface ILimitComponent {
  limitParam : IlimitParam[];
}
export interface IlimitParam {
  name : string;
  value: number
}

export interface IApiGetLimitsResponse {
  response : IBetpackGetLimitsResponse;
}

export interface IBetpackGetLimits {
  freebetOffer : IBetpackLivServeResponse[];
}
export interface IBetpackGetLimitsResponse extends IResult{
  respFreebetGetOffers : IBetpackGetLimits;
  version: string;
}
export interface IGetLimitsRequest {
  freeBetTriggerType : string;
  freebetOfferIds : string[];
  ignoreStartDate: string;
  returnLimits: string;
}

type IYesNo = 'Y' | 'N';
export type IType = 'proxy' | 'oxi' | 'bet' | 'auth';
type IGroup = 'BET' | 'LOTTERYBET' | 'POOLBET';

export type IBppRequest = IAccountHistoryRequest
  | IBetsRequest
  | ICashoutBetRequest
  | ICheckVideoStreamRequest
  | IFreeBetOfferRequest
  | IGetVideoStreamRequest
  | INetverifyRequest
  | IOfferBet
  | IOfferBetAction
  | IPoolBetPlacementRequest
  | IReadBetRequest
  | IRequestTransFreebetTrigger
  | IRequestTransBetpackTrigger
  | IRequestTransGetBetDetail
  | IRequestTransGetBetDetails
  | IRequestTransGetBetsPlaced
  | IRequestTransPoolGetDetail
  | IBuildBetRequest
  | IGetBetHistoryRequest
  | IMatchDayRewardsParamsRequest
  | IUserSelectionDetail
  | string
  | IAccGetLimitsResponse
  | IApiGetLimitsResponse
  | IGetLimitsRequest;

export type IBppResponse = I24BppResponse
  | IAccountFreebetsResponse
  | IAccountHistoryResponse
  | IBetsResponse
  | ICashoutBetResponse
  | ICheckVideoStreamResponse
  | ICurrenciesResponse
  | IFreebetTrigger
  | IFreeBetOfferResponse
  | IFreeBetOfferResponseBetslip
  | IGetVideoStreamResponse
  | INetverifyResponse
  | IValidateBetResponse
  | IOfferBet
  | IOfferBetAction
  | IPoolBetPlacementResponse
  | IReadBetResponse
  | IResponseTransFreebetTrigger
  | IResponseTransGetBetDetails
  | IResponseTransGetBetDetail
  | IResponseTransGetBetsPlaced
  | IResponseTransPoolGetDetail
  | IBuildBetResponse
  | IBetHistoryBet
  | IMatchDayRewardsResponse
  | IHowItWorks
  | IAccGetLimitsResponse
  | IApiGetLimitsResponse;

  export interface IFreebetExpiredTokenIds{
    freebetTokenId?:string;
    tokenExpire?:boolean;
  }
export interface IStreamFlag {
  flag: boolean;
  legId: string;
  isUsedFromWidget:boolean;
}