
import { IBase } from '../base.model';

export interface IBYBSwitcher extends IBase {
  sortOrder: number;
  name: string;
  provider: string;
  lang: string;
  enabled: boolean;
  default: boolean;
  updatedBy: string;
}
