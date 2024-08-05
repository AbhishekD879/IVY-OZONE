import { Filename } from './filename.model';
import { Base } from './base.model';

export interface Football3DBanner extends Base {
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  description: string;
  targetUri: string;
  name: string;
  displayDuration: number;
  disabled: boolean;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
