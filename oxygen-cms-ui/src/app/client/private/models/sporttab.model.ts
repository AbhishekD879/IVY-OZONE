import {Base} from '@app/client/private/models/base.model';
import {SportTabFilters,ISportTabPopularBetsFilter} from '@app/client/private/models/sporttabFilters.model';
 
export interface SportTab extends Base {
  SportTab: Event;
  brand: string;
  sportId: number;
  name: string;
  displayName: string;
  enabled: boolean;
  checkEvents: boolean;
  filters?: SportTabFilters;
  marketsNames?: any;
  href:string;
  trendingTabs?: trendingTabs[] ;
  popularTabs?: PopularTabs[];
  interstitialBanners?: InterstitialBanners;
}

export interface InterstitialBanners {
  desktopBannerId: string;
  mobileBannerId: string;
  bannerPosition: string;
  bannerEnabled: boolean;
  ctaButtonLabel: string;
  redirectionUrl: string;
}
export interface Markets {
  templateMarketName?: string;
}
export interface trendingTabs {
  id?: string,
  trendingTabName?: string,
  headerDisplayName?: string,
  enabled?: boolean,
  href?: string,
  popularTabs?:PopularTabs[],
}
export interface PopularTabs {
  enabled: boolean;
  headerDisplayName: string;
  popularTabName: string;
  showNewFlag: boolean;
  startsInText: string;
  backedInLastText: string;
  showMoreText: string;
  showLessText: string;
  backedUpTimesText: string;
  informationTextDesc: string;
  numbOfDefaultPopularBets: number;
  numbOfShowMorePopularBets: number;
  priceRange: string;
  lastUpdatedTime: string;
  noPopularBetsMsg: string;
  betSlipBarDesc: string;
  betSlipBarCTALabel: string;
  betSlipBarBetsAddedDesc: string;
  betSlipBarRemoveBetsCTALabel: string;
  suspendedBetsAddedText: string;
  suspendedBetsDesc: string;
  backedInLastFilter: ISportTabPopularBetsFilter[];
  eventStartsFilter: ISportTabPopularBetsFilter[];
  enableAddToBetSlipBar?: boolean;
  enableArrowIcon: boolean;
  enableBackedUpTimes: boolean;
  noBettingDescTitle:string;
  href?:string;
  id?:string;
}

export interface IsportTable {
    href: string,
    enable: boolean,
    tabname:string
}