import { IOutcome } from './outcome.model';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';

export interface IMarket {
  cashoutAvail: string;
  correctPriceTypeCode: string;
  dispSortName: string;
  eachWayFactorNum: string | number;
  eachWayFactorDen: string | number;
  eachWayPlaces: string;
  header?: string | string[];
  id: string;
  isAntepost?: string;
  isGpAvailable: boolean;
  isResulted?: boolean;
  isLpAvailable: boolean;
  isMarketBetInRun: boolean | string;
  isSpAvailable: boolean;
  isDisplayed?: boolean;
  liveServChannels: string;
  isEachWayAvailable: boolean;
  liveServChildrenChannels: string;
  marketsNames: string;
  marketStatusCode: string;
  name: string;
  originalMarketName: string;
  nextScore: number;
  outcomes: IOutcome[];
  periods: Array<any>;
  players?: {
    scores: { number: number; score: string; outcomeid: string; }[],
    filteredScore: {}[],

    // TODO: Dynamic properties. remove dynamic properties set
    activeScoreOutcome: string;
  }[];
  priceTypeCodes: string;
  terms: string;
  templateMarketId: number;
  templateMarketName: string;
  viewType: string;
  filteredOutcomes?: IOutcome[];
  marketOptaLink?: IMarketLinks;
  collectionIds?: string;
  correctedEachWayPlaces?: string;
  customOrder?: any;
  collapseMarket?: boolean;
  siteChannels?: string;

  // TODO: Dynamic properties. remove dynamic properties set
  rawHandicapValue?: any;
  resulted?: boolean;
  handicapValues?: string;
  new?: boolean;
  allShown?: boolean;
  eventId?: string;
  children?: { outcome: IOutcome, scorecast?: any, outcomeMeaningMinorCode?: number, referenceEachWayTerms?: IReferenceEachWayTerms }[];
  displayOrder?: any;
  marketName?: string;
  sectionTitle?: string;
  sortOrder?: string;
  template?: string;
  marketMeaningMinorCode?: string;
  marketMeaningMajorCode?: string;
  outcomeMeaningMinorCode?: string[] | string;
  hidden?: boolean;
  drilldownTagNames?: string;
  linkedMarketId?: string;
  timeformData?: any;
  selections?: any[];
  linkedEntityId?: string | number;
  correctPriceType?: string;
  showLimit?: number;
  isAllShown?: boolean;
  marketsGroup?: boolean;
  groupedOutcomes?: IOutcome[];
  path?: string;
  label: string;
  isTopFinish: boolean;
  isToFinish: boolean;
  insuranceMarkets: boolean;
  isOther: boolean;
  isWO: boolean;
  isSmartBoosts?: boolean;
  markets?: any;
  ncastTypeCodes?: string;
  marketliveServChannels?: string;
  index?: number;
  description?: string;
  isHR?: boolean;
  isGH?: boolean;
  isNew?: boolean;
  birDescription?: string;
  teamName?: string;
  fcMktAvailable?: string;
  tcMktAvailable?: string;
  isSCAvailable?:boolean;
  referenceEachWayTerms?: IReferenceEachWayTerms;
  displayed?: string;
  isAggregated?: boolean;
  isOutcomesFetched?: boolean;
  isLuckyDip?: boolean;
  templateType?: string
}

export interface ICashoutMarket {
  cashoutAvail: string;
}
export interface IReferenceEachWayTerms {
  id: string;
  places: string;
}

export interface IMarketTemplate {
  id?: string | number;
  marketIds: string[];
  eventId: string;
  name: string;
  displayOrder: number;
  marketMeaningMinorCode?: string;
  viewType?: string;
  cashoutAvail?: string;
  drilldownTagNames?: string;
  hidden?: boolean;
}