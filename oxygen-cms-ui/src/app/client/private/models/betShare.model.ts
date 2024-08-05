import { Base } from '@app/client/private/models/base.model';

export interface UserPreferncesArray {
  name: string;
  isSelected: boolean;
}

export interface LuckyDipBetSharingConfigs {
  enable: boolean;
  header: string;
  backgroundImageUrl: string;
  luckyDipLabel: string;
  wonLabel: string;
  potentialReturnsLabel: string;
  luckyDipAffiliateLink: string;
  openBetControl: UserPreferncesArray[];
  wonBetControl: UserPreferncesArray[];
  lostBetControl: UserPreferncesArray[];
}
export  interface FTPBETSHARING_CONFIG  {
  enable: boolean;
  header: string;
  subHeader: string;
  playLabel: string;
  backgroundImageUrl: string;
  affiliateLink: string;
  teamDetails : teamDetails[];
} 
export interface teamDetails {
    teamName: string;
    teamLogoUrl: string;
    activated: boolean;
}

export interface BetShare extends Base {
  genericSharingLink: string;
  popUpDesc: string;
  openBetShareCardStatus: boolean;
  openBetShareCardMessage: string;
  openBetShareCardSecondMessage: string;
  shareCardImageFileName: string;
  wonBetShareCardStatus: boolean;
  wonBetShareCardMessage: string;
  lostBetsShareCardMessage: string;
  cashedOutBetsShareCardMessage: string;
  horseRacingUrl: string;
  footBallUrl: string;
  url5ASide: string;
  settledBetsGenericUrl: string;
  openBetsGenericUrl: string;
  extensionUrl: string;
  beGambleAwareLogoUrl: string;
  brandLogoUrl: string;
  openBetControl: UserPreferncesArray[];
  wonBetControl: UserPreferncesArray[];
  lostBetControl: UserPreferncesArray[];
  cashedOutBetControl: UserPreferncesArray[];
  luckyDipBetSharingConfigs : LuckyDipBetSharingConfigs;
  ftpBetSharingConfigs? :FTPBETSHARING_CONFIG;
}
