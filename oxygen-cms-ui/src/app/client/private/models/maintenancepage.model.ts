import { Filename } from './filename.model';
import { Base } from './base.model';

export interface MaintenancePage extends Base {
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  desktop: boolean;
  tablet: boolean;
  mobile: boolean;
  targetUri: string;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
