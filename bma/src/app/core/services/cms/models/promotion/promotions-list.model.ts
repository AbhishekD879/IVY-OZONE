import { IPromotion } from './promotion.model';

export interface IPromotionsList {
  expandedAmount?: string;
  promotions?: IPromotion[];
  promotionsBySection?: IPromotionSection[];
}

export interface IPromotionSection {
  name: string;
  sortOrder: number;
  promotions: IPromotion[];
  unassigned?: boolean;
  availablePromotions: IPromotion[];
}
