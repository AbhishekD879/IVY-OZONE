export const extraPlaceConfig = {
  cacheInterval: 5 * 60 * 1000, // 5 min
  cacheName: 'extraPlaceEventsHR',
  request: {
    siteChannels: 'M',
    categoryId: '21',
    marketDrilldownTagNamesContains: 'MKTFLAG_EPR',
    templateMarketNameOnlyEquals: '|Win or Each Way|',
    isNotFinished: true,
    isRawIsOffCodeNotY: true,
    isNotResulted: true,
    isNotLiveNowEvent: true,
    isNotStarted: true,
    hasOpenEvent: 'true',
    siteServerEventsCount: 3,
    limitOutcomesCount: 1
  }
};
