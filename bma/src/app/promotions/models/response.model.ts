import { IPromotionsList } from '@core/services/cms/models';
import { IAccountFreebetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface ICheckStatusResponse {
  fired: boolean;
  id: string;
  timestamp: string;
  error: any;
}

export type IOffersWithPromotions = (IAccountFreebetsResponse|IPromotionsList)[];
