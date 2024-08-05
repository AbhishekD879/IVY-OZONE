import {Filename} from './filename.model';

export interface Feature {
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
  validityPeriodEnd: string;
  validityPeriodStart: string;
  shortDescription: string;
  title: string;
  vipLevels: any[];
  lang: string;
  brand: string;
  showToCustomer: string;
  disabled: boolean;
  description: string;
  filename: Filename;
}
