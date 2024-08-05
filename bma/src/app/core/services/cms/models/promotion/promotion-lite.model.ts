import { IProcessedRequestModel } from '../process-request.model';

export interface IPromotionLite extends IProcessedRequestModel {
  eventLevelFlag: string;
  marketLevelFlag: string;
  promoKey: string;
  promotionText: string;
  requestId: string;
  title: string;
  vipLevels: string[];
  showToCustomer: string[];
  blurbMessage?: string;
  templateMarketName?: string;
}
