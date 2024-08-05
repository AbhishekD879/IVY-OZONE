
import { Base } from './base.model';

export interface HeaderContactMenu extends Base {
  disabled: boolean;
  inApp: boolean;
  lang: string;
  linkTitle: string;
  linkTitleBrand: string;
  sortOrder: number;
  targetUri: string;
  label: string;
  authRequired: boolean;
  systemID: number;
  startUrl: string;
}
