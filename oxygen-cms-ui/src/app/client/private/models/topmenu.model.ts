
import { Base } from './base.model';

export interface TopMenu extends Base {
  key: string;
  targetUri: string;
  linkTitle: string;
  disabled: boolean;
  sortOrder: number;
  lang: string;
}
