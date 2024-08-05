import { IBase } from "@app/core/services/cms/models/base.model";
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
  fanzoneConfiguration: FanzoneConfig
}

export interface FanzoneConfig {
  showCompetitionTable: boolean,
  showNowNext: boolean,
  showStats: boolean,
  showClubs: boolean,
  showGames: boolean,
  showSlotRivals: boolean,
  showScratchCards: boolean,
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
  description: string
}

export interface IEmailOptin{
  fanzoneUser?: boolean;
  remindMeLaterCount?: number; 
  remindMeLaterPrefDate?: string; 
  dontShowMeAgainPref?: boolean;
  undisplayFanzoneGamesPopup?: boolean;
  undisplayFanzoneGamesTooltip?: boolean;
  newSignPostingSeenDate?: string;
  showRelegatedPopupDate?: string;
  showSYCPopupDate?: string;
}