import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IPrice } from '@core/models/price.model';

export interface IHorse {
  horseName: string;
  weight: string;
}

export interface IRacingFormOutcome {
  silkName: string;
  age?: string;
  draw?: string;
  formGuide?: string;
  formProviderRating?: string;
  id?: string;
  jockey?: string;
  overview?: string;
  refRecordId?: string;
  refRecordType?: string;
  runnerStatusCode?: string;
  form?: IRacingPostForm[];
  trainer?: string;
  weight?: string;
  officialRating?: string;
  imgError?: boolean;
  starRating?: number;
  rprRating?: string;
  isBeatenFavourite: boolean;
  allowance?:number;
}

export interface IRacingPostForm {
  condition: string;
  course: string;
  date: string;
  jockey: string;
  officialRating: string;
  outcome: string;
  raceid: number;
  rpr: string;
  topspeed: string;
  weight: string;
  weightLbs: number;
  odds?: string;
  comment?: string;
  position?: string;
  noOfRunners?: string;
  distanceToWinner?: string;
  other?: IHorse;
  courseName?: string;
  raceTitle?: string;
  raceClass?: string;
  saddle?:string;
}

export interface IToteRacingOutcome extends IRacingFormOutcome {
  formGuide?: string;
  courseDistanceWinner: string;
}

export interface IToteOutcome extends IOutcome {
  racingFormOutcome: IToteRacingOutcome;
}

interface IOutcomeBase {
  racingFormOutcome: IRacingFormOutcome | IToteRacingOutcome;
}

export interface IOutcome extends IOutcomeBase {
  correctPriceType: string;
  correctedOutcomeMeaningMinorCode: number;
  displayOrder: any;
  fakeOutcome: boolean;
  icon: boolean;
  id: string;
  isUS?: boolean;
  liveServChannels: string;
  liveServChildrenChannels: string;
  name: string;
  horseName: string;
  position?: string;
  resultCode?: string;
  isMostTipped: boolean;
  outcomeMeaningMajorCode: string;
  outcomeMeaningMinorCode: string | string[] | number;
  outcomeStatusCode: string;
  filteredName?: string;
  prices: IOutcomePrice[];
  teamExtIds?: string;
  isFanzoneMarket?: boolean;

  // ToDo: Discuss with Maks
  runnerNumber: string;
  silkName: string;
  trainer?: string;
  racingFormOutcome: IRacingFormOutcome;

  // TODO: Dynamic properties remove dynamic param
  modifiedPrice?: IPrice;
  linkedOutcomeId?: string;
  isFavourite?: boolean;
  details: IOutcomeDetails | any;
  children?: any;
  externalId?: string;
  priceType?: string;
  marketRawHandicapValue?: any;
  amount?: string;
  marketsNames?: string;
  priceTypeCodes?: string;
  marketStatusCode?: string;
  alphabetName?: string;
  numbersName?: string;
  rawHandicapValue?: string;
  sortOrder?: number;
  cashoutAvail?: string;
  racerId?: string;
  drawNumber?: string;
  jockey?: string;
  price?: Partial<IOutcomePrice> | IOutcomePrice[];
  isEachWayAvailable?: boolean;
  eachWayFactorDen?: string;
  eachWayFactorNum?: string;
  oldModifiedPrice?: string;
  originalPrice?: IOutcomePrice;
  errorMsg?: string;
  eventId?: string;
  marketId?: string;
  outcomeMeaningScores?: string;
  isDisplayed?: boolean;
  isResulted?: boolean;
  isValidRunnerNumber?: boolean;
  marketIndex?: any;
  event?: ISportEvent;
  day?: string;
  lp_num?: number;
  lp_den?: number;
  eventName?: string;
  time?: string;
  dateTime?: string;
  nonRunner?: boolean;
  trapNumber?: number;
  market: IMarket;
  timeformData?: any;
  linkedEntityId?: string | number;
  results?: any;
  favourite?: any;
  isSuspended?: boolean;
  wasPrice?: string;
  description?: string;
  active?: boolean;
  isRacing?: boolean;
  originalOutcomeMeaningMinorCode?: string;
  marketliveServChannels?: string;
  isMarketBetInRun?: string | boolean;
  csOutcomeOrder?: number;
  teamName?: string;
  fc_avail?: string;
  tc_avail?: string;
  totePrices?: IOutcomePrice[];
  displayed?: string;
  flags?: Array<string>;
}

export interface IOutcomeResult {
  confirmed: string;
  value: string;
  time?: string;
}

export interface IHorseOutcome  {
  outcome: IOutcome;
}

export interface IBetHistoryOutcome extends IOutcome {
  id: string;
  outcomeResult?: string;
  eventType?: {
    name: string;
  };
  eventClass?: {
    name: string;
  };
  eventCategory?: {
    id: string;
  };
  result?: IOutcomeResult;
  results?: any;
  favourite?: any;
  externalStatsLink?: IExternalStatsLink;
  flags?:Array<string>;
}

export interface IExternalStatsLink {
  statCategory: string;
  statValue: string;
  playerId?: string;
  contestantId?: string;
}

export interface IOutcomeDetails {
  categoryId: string;
  classId: number;
  eachwayCheckbox: boolean;
  eventId: number;
  eventStatusCode: string;
  eventliveServChannels: string;
  marketliveServChannels: string;
  outcomeliveServChannels: string;
  isEachWayAvailable: boolean;
  isGpAvailable: boolean;
  isMarketBetInRun: boolean | string;
  isRacing: boolean;
  isSPLP: boolean;
  market: string;
  marketId: string;
  eventDrilldownTagNames: string;
  marketDrilldownTagNames: string;
  isAvailable?: string | boolean;
  cashoutAvail: string;
  marketCashoutAvail: string;
  outcomeMeaningMinorCode: string | string[] | number;
  info: {
    sportId?: string;
    time: string;
    localTime?: string;
    isStarted?: boolean;
  };
  marketPriceTypeCodes?: string;
}
