import { Base } from './base.model';

export interface HeaderSubMenu extends Base {
  disabled: boolean;
  lang: string;
  linkTitle: string;
  linkTitle_brand: string;
  sortOrder: number;
  targetUri: string;
  inApp: boolean;
}
