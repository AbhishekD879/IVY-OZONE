import { ISportConfigRequestTab } from '@app/core/services/cms/models';

export const defaultRequestTabs: ISportConfigRequestTab = {
  live: {},
  coupons: {
    date: 'today',
    isActive: true
  },
  outrights: {
    isActive: true,
    marketsCount: false
  },
  specials: {
    marketsCount: false,
    marketDrilldownTagNamesContains: 'MKTFLAG_SP'
  },
  today: {
    isNotStarted: true
  },
  tomorrow: {},
  future: {}
};

export const footballRequestTabs: ISportConfigRequestTab = {
  ...defaultRequestTabs,
  today: {
    isNotStarted: true,
    templateMarketNameOnlyIntersects: true
  },
  tomorrow: {
    templateMarketNameOnlyIntersects: true
  },
  future: {
    templateMarketNameOnlyIntersects: true
  },
  upcoming: {
    isNotStarted: true
  },
  jackpot: {},
  results: {}
};
