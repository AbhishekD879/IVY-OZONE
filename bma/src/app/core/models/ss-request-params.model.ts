export interface ISSRequestParamsModel {
  categoryId?: string;
  eventSortCode?: string;
  siteChannels?: string;
  hasOpenEvent?: string;
  typeId?: string;
  simpleFilters?: string;
  couponsIds?: string;
  id?: string;
  isNotStarted?: boolean;
  isNotFinished?: boolean;
  ids?: string;
  eventId?: number;
  eventsIds?: any; // string|number|
  outcomesIds?: any; // [string | number] | string
  marketIds?: number[];
  marketIdArr?: string[];
  classIds?: any;
  count?: string;
  categoriesIds?: string;
  typeIds?: string | number[];
  poolsIds?: string;
  simpleFilter?: any;
  racingFormOutcome?: any;
  racingFormEvent?: any;
  startTime?: string;
  timeRange?: string;
  endTime?: string;
  suspendAtTime?: string;
  display?: string;
  limitOutcomesCount?: number;
  marketsCount?: any;
  childCount?: boolean;
  isRacing?: boolean;
  date?: any;
  resultsDay?: any;
  marketName?: any;
  resultedMarketName?: any;
  eventsCount?: any;
  poolTypes?: string;
  includeUndisplayed?: boolean;
  externalKeysEvent?: boolean;
  siteServerEventsCount?: number;
  priceHistory?: boolean;
  isVirtualRacesEnabled?: boolean;
  virtualRacesIncluded?: string[];
  isValidFzSelection?: boolean;
}
