import { IItemDateModel } from './item-date.model';

export interface IVipItemModel extends IItemDateModel {
  vipLevels: number[];
  showToCustomer: string;
}
