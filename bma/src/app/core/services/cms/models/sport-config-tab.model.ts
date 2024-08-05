import { ISportConfigSubTab } from './sport-config-sub-tab.model';

export interface ISportConfigTab {
  label: string;
  enabled?: boolean;
  index?: number;
  id?: string;
  url?: string;
  name?: string;
  hidden?: boolean;
  sortOrder?: number;
  subTabs?: ISportConfigSubTab[];
  displayInConnect?: boolean;
  filters?: {
    time?: number[];
    league?: ILeagueFilter[];
  };
  marketsNames?: IMarketNames[];
  interstitialBanners?: InterstitialBanners;
}

export interface ILeagueFilter {
  leagueName: string;
  leagueIds: number[];
}

export interface IMarketNames {
  templateMarketName: string;
  title: string
}

export interface InterstitialBanners {
  bannerEnabled: true;
  bannerPosition: string;
  ctaButtonLabel: string;
  desktopBannerId: string;
  mobileBannerId: string;
  redirectionUrl: string;
}
