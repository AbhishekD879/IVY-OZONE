import {Base} from './base.model';

export interface PromotionsSections extends Base {
  name: string;
  promotionIds: string;
  disabled: boolean;
}
