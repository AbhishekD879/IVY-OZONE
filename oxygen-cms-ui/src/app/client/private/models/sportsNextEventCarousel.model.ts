import { Base } from '@app/client/private/models/base.model';

export interface SportsNextEventCarousel extends Base {
  title: string;
  disabled: boolean;
  limit: number;
  classIds:  string;
  typeIds?: number[];
  sportId: number;
  pageId: string;
  pageType: string;
  sortOrder?: number;
  message?: string;
  buttonText?: string;
  redirectionUrl?: string;
  mobileImageId?: string;
  desktopImageId?: string;
}

