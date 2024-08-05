import {Filename} from './filename.model';

export interface Promotion {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  title_brand: string;
  sortOrder: number;
  heightMedium: number;
  widthMedium: number;
  uriMedium: string;
  htmlMarkup: string;
  requestId: string;
  vipLevelsInput: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  shortDescription: string;
  promoKey: string;
  title: string;
  vipLevels: undefined[];
  lang: string;
  brand: string;
  categoryId: string[];
  showToCustomer: string;
  disabled: boolean;
  description: string;
  filename: Filename;
}
