import { Filename } from './filename.model';
import { Base } from './base.model';

export interface BetReceiptBannerTablet  extends Base  {
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  disabled: boolean;
  description: string;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
