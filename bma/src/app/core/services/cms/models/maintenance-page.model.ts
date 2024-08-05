import { IFilename } from './filename.model';
import { IBase } from './base.model';

export interface IMaintenancePage extends IBase {
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  desktop: boolean;
  tablet: boolean;
  mobile: boolean;
  targetUri: string;
  uriMedium: string;
  uriOriginal: string;
  filename: IFilename;
}
