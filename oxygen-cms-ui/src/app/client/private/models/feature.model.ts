import { Filename } from './filename.model';
import { Base } from './base.model';

export interface Feature extends Base {
  title_brand: string;
  sortOrder: number;
  heightMedium: number;
  widthMedium: number;
  uriMedium: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  shortDescription: string;
  title: string;
  vipLevels: any[];
  lang: string;
  showToCustomer: string;
  disabled: boolean;
  description: string;
  filename: Filename;
}
