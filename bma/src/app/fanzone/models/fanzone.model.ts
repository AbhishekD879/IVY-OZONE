import { ISiteCoreTeaserFromServer } from "@app/core/models/aem-banners-section.model";
import { IBase } from "@app/core/services/cms/models/base.model";
import { ITeamAsset } from "@app/lazy-modules/fanzone/models/fanzone-team-asset.model";

export interface IFanzoneSiteCoreBanner {
  type?: string;
  teasers?: ISiteCoreTeaserFromServer[];
}

export interface FanzoneDetails extends IBase {
  pageName: string;
  name: string;
  teamId: string;
  openBetID: string;
  assetManagementLink: string;
  launchBannerUrl: string;
  fanzoneBanner: string;
  ctaBtnText: string;
  description: string;
  primaryCompetitionId: string;
  secondaryCompetitionId: string;
  clubIds: string;
  location: string;
  nextGamesLbl: string;
  outRightsLbl: string;
  premierLeagueLbl: string;
  active: boolean;
  fanzoneConfiguration: FanzoneConfig;
  asset?: ITeamAsset;
}

export interface FanzoneConfig {
  showCompetitionTable: boolean,
  showNowNext: boolean,
  showStats: boolean,
  showClubs: boolean,
  showGames: boolean,
  sportsRibbon: boolean,
  homePage: boolean,
  footballHome: boolean,
  atozMenu: boolean,
  launchBannerUrlDesktop?: string,
  fanzoneBannerDesktop?: string
}

export interface FanzoneClub extends IBase {
  pageName: string,
  active: boolean,
  validityPeriodStart: string,
  validityPeriodEnd: string,
  title: string,
  bannerLink: string,
  description: string,
  bannerImgSrc?:string
}
export interface fanzoneStorageData {
  teamId: string,
  teamName: string
}

export interface IFanzoneGameTooltipConfig {
  Delay: number;
  Message: string;
  Enable: boolean;
}


export interface IFanzoneGameTooltipArgs {
  message: string;
  show: boolean;
}
