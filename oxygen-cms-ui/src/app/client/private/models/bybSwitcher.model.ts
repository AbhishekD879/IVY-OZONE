
import { Base } from './base.model';

export interface BYBSwitcher extends Base {
  sortOrder: number;
  name: string;
  provider: string;
  lang: string;
  enabled: boolean;
  default: boolean;
  updatedBy: string;
}
