export interface IEventsIds {
  eventsIds: string;
  simpleFilters?: string;
}

export interface IDividends {
  [eventId: number]: {
    FC: string;
    TC?: string;
  };
}

export interface IRacingResult {
  racingResult: {
    categoryCode: string;
    categoryId: string;
    categoryName: string;
    children: Array<IFinalPositionResponse | INcastDividendResponse | IRuleDeductionResponse>;
    classDisplayOrder: string;
    classFlagCodes: string;
    classId: string;
    className: string;
    classSortCode: string;
    displayOrder: string;
    eventSortCode: string;
    eventStatusCode: string;
    id: string;
    isFinished: string;
    isResulted: string;
    name: string;
    rawIsOffCode: string;
    responseCreationTime: string;
    siteChannels: string;
    sportId: string;
    startTime: string;
    typeDisplayOrder: string;
    typeFlagCodes: string;
    typeId: string;
    typeName: string;
  };
}

export interface IFinalPositionResponse {
  finalPosition: {
    id: string;
    marketId: string;
    name: string;
    outcomeId: string;
    position: string;
    runnerNumber: string;
    siteChannels: string;
    startingPriceDec: string;
    startingPriceDen: string;
    startingPriceNum: string;
  };
}

export interface INcastDividendResponse {
  ncastDividend: {
    dividend: string;
    id: string;
    marketId: string;
    runnerNumbers: string;
    siteChannels: string;
    type: string;
  };
}

export interface IRuleDeductionResponse {
  rule4Deduction: {
    deduction: string;
    deductionType: string;
    fromDate: string;
    id: string;
    marketId: string;
    siteChannels: string;
    toDate: string;
  };
}
