
import { Base } from './base.model';

export interface BottomMenu extends Base {
  disabled: boolean;
  inApp: boolean;
  lang: string;
  linkTitle: string;
  linkTitleBrand: string;
  sortOrder: number;
  targetUri: string;
  section: string;
  authRequired: boolean;
  systemID: number;
  startUrl: string;
}
