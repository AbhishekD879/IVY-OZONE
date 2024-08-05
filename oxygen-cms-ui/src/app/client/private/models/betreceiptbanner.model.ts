import { Filename } from './filename.model';
import { Base } from './base.model';

export interface BetReceiptBanner extends Base {
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  disabled: boolean;
  description: string;
  uriMedium: string;
  uriOriginal: string;
  fileUrl: string;
  useUrl: boolean;
  directFileUrl: string;
  useDirectFileUrl: boolean;
  filename: Filename;
}
