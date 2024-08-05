import { Iterator } from '@coreModule/services/iterator/iterator.class';
export interface IFanzoneComingBack {
  fzComingBackHeading?: string;
  fzComingBackTitle?: string;
  fzComingBackDescription?: string;
  fzComingBackBadgeUrlMobile?: string;
  fzComingBackBadgeUrlDesktop?: string;
  fzComingBackOKCTA?: string;
  fzComingBackDisplayFromDays?: number;
  fzComingBackBgImageMobile?: string;
  fzComingBackBgImageDesktop?: string;
  fzSeasonStartDate?: string;
  fzComingBackPopupDisplay?: boolean;
  iterator?: Iterator;
}