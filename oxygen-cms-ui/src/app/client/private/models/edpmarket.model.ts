
import { Base } from './base.model';

export interface EdpMarket extends Base {
  sortOrder: number;
  name: string;
  lang: string;
  lastItem: boolean;
}
