import { Filename } from './filename.model';
import { Base } from './base.model';

export interface Promotion extends Base {
  title_brand: string;
  sortOrder: number;
  heightMedium: number;
  widthMedium: number;
  uriMedium: string;
  htmlMarkup: string;
  promotionText: string;
  popupTitle: string;
  requestId: string;
  vipLevelsInput: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  shortDescription: string;
  promoKey: string;
  title: string;
  vipLevels: undefined[];
  lang: string;
  categoryId: string[];
  showToCustomer: string;
  disabled: boolean;
  description: string;
  filename?: Filename;
  competitionId: string[];
  isSignpostingPromotion: false;
  promotionId: string;
  openBetId: string;
  useDirectFileUrl?: boolean;
  directFileUrl?: string;
  useCustomPromotionName?: boolean;
  customPromotionName?: string;
  betPack: BetPack;
  templateMarketName: string;
  blurbMessage: string;
  freeRideConfig: FreeRideConfig;
  navigationGroupId?: string;
}

export interface BetPack {
  isBetPack?: boolean;
  bodyText?: string;
  congratsMsg?: string;
  offerId?: string;
  triggerIds?: string;
  betValue?: string;
  lowFundMessage?: string;
  notLoggedinMessage?: string;
  errorMessage?: string;
  redirectUrl?: string;
}

export interface FreeRideConfig {
  isFreeRidePromo?: boolean;
  errorMessage?: string;
  ctaPreLoginTitle?: string;
  ctaPostLoginTitle?: string;
}
