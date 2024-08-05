export interface IRacingResultedEventResponse {
  resultedEvent: {
    children: IResultedMarketResponse[];
    categoryCode: string;
    categoryId: string;
    categoryName: string;
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
    siteChannels?: string;
    sportId: string;
    startTime: string;
    typeDisplayOrder: string;
    typeFlagCodes?: string;
    typeId: string;
    typeName: string;
    isReplayStreamAvailable?:boolean;
    drilldownTagNames?:string;
  };
}

export interface IResultedMarketResponse {
  resultedMarket: {
    children: IResultedOutcomeResponse[];
    collectionIds: string;
    collectionNames: string;
    displayOrder: string;
    eachWayFactorDen: string;
    eachWayFactorNum: string;
    eachWayPlaces: string;
    eventId: string;
    id: string;
    isEachWayAvailable: string;
    isFinished: string;
    isResulted: string;
    isSpAvailable: string;
    marketMeaningMajorCode: string;
    marketMeaningMinorCode: string;
    marketStatusCode: string;
    maxAccumulators: string;
    name: string;
    ncastTypeCodes?: string;
    priceTypeCodes?: string;
    siteChannels?: string;
    templateMarketId: string;
  };
}

export interface IResultedOutcomeResponse {
  resultedOutcome: {
    children: IRacingResultedPriceResponse[];
    id: string;
    isFinished: string;
    isResulted: string;
    marketId: string;
    name: string;
    outcomeMeaningMajorCode: string;
    resultCode: string;
    runnerNumber: string;
    siteChannels?: string;
    position?: string;
  };
}

export interface IRacingResultedPriceResponse {
  resultedPrice: {
    id: string;
    outcomeId: string;
    priceDec?: string;
    priceDen?: string;
    priceNum?: string;
    priceTypeCode: string;
  };
}
