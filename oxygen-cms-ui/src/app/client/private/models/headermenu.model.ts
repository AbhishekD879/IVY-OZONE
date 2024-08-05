
import { Base } from './base.model';

export interface HeaderMenu extends Base {
  disabled: boolean;
  lang: string;
  level: string;
  linkTitle: string;
  linkTitle_brand: string;
  sortOrder: number;
  targetUri: string;
  parent: string;
  inApp: boolean;
}
