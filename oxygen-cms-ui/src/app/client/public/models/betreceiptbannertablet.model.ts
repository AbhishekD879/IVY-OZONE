import {Filename} from './filename.model';

export interface BetReceiptBannerTablet {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  disabled: boolean;
  brand: string;
  description: string;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
