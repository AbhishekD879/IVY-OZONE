import {Base} from './base.model';
import {Filename} from '@app/client/private/models/filename.model';

export interface EndPage extends Base {
  title: string;
  brand: string;
  backgroundSvgImage: Filename;
  gameDescription: string;
  submitMessage: string;
  noLatestRoundMessage: string;
  noPreviousRoundMessage: string;
  upsellBetInPlayCtaText: string;
  upsellAddToBetslipCtaText: string;
  submitCta: string;
  successMessage?: string;
  errorMessage?: string;
  redirectionButtonLabel?: string;
  redirectionButtonUrl?: string;
  bannerSiteCoreId?: string;

  showUpsell: boolean;
  showResults: boolean;
  showAnswersSummary: boolean;
  showPrizes: boolean;
  isChanged: boolean;
}
