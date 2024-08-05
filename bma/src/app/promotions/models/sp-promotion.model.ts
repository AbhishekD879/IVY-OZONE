import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import { SafeHtml } from '@angular/platform-browser';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';

export interface ISpPromotion extends IPromotion {
  marketLevelFlag: string;
  eventLevelFlag: string;
  useDirectFileUrl: boolean;
  directFileUrl: string;
  overlayBetNowUrl: string;
  flagName: string;
  safeDescription?: SafeHtml;
  safeHtmlMarkup?: SafeHtml;
  safeCongratsMsg?: SafeHtml;
  iconId: string;
  openBetId?: string;
  useCustomPromotionName?: boolean;
  customPromotionName?: string;
  betPack?: IBetpack;
  freeRideConfig?: IFreeRide;
  navigationGroupId?: string;
  templateMarketName?: string;
}

export interface IPromotionsSiteCoreBanner {
  type?: string;
  teasers?: ISiteCoreTeaserFromServer[];
}

export interface INavigationGroup {
  id: string;
  brand: string;
  title: string;
  status: boolean;
  navItems: INavItem[];
}
export interface INavItem {
  name: string;
  url?: string;
  navType:string,
  leaderboardId?:string,
  navigationGroupId?:string,
  descriptionTxt?:string
}

export interface ILeaderBoard {
  id: string;
  name: string;
  topX: string;
  individualRank: boolean;
  genericTxt: string;
  status: boolean;
  columns: IColumns[];
}
export interface IColumns {
  originalName: string;
  displayName: string;
  subtitle: string;
  style: string;
  applyMasking: boolean;
}


export interface IBetpack {
  isBetPack?: boolean;
  bodyText?: string;
  congratsMsg?: string;
  offerId?: string;
  triggerIds?: string;
  betValue?: string;
  lowFundMessage?: string;
  notLoggedinMessage?: string;
  errorMessage?: string;
}

export interface IFreeRide {
  ctaPreLoginTitle?: string;
  ctaPostLoginTitle?: string;
  errorMessage?: string;
  isFreeRidePromo?: boolean;
}
