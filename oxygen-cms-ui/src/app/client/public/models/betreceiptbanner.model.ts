import {Filename} from './filename.model';

export interface BetReceiptBanner {
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
  fileUrl: string;
  useUrl: boolean;
  directUrl: string;
  useDirectUrl: boolean;
  directFileUrl: string;
  useDirectFileUrl: boolean;
  filename: Filename;
}
