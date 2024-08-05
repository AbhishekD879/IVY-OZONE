import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { IBase } from '../base.model';
import { IFilename } from '../filename.model';
import { IProcessedRequestModel } from '../process-request.model';

export interface IPromotion extends IBase, IProcessedRequestModel {
  title_brand: string;
  sortOrder: number;
  heightMedium: number;
  widthMedium: number;
  uriMedium: string;
  htmlMarkup: string;
  popupTitle: string;
  promotionText: string;
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
  filename?: IFilename;
  competitionId: string[];
  showsitecoreBanner?: boolean;
  sitecoreBanner?: ISiteCoreTeaserFromServer;
}
