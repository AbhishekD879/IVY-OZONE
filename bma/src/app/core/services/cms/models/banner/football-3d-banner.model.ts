import { IFilename } from '../filename.model';
import { IBase } from '../base.model';

export interface IFootball3DBanner extends IBase {
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
  filename: IFilename;
}
