
import { IBase } from './base.model';

export interface IEdpMarket extends IBase {
  sortOrder: number;
  name: string;
  lang: string;
  lastItem: boolean;
}

export interface IMarketLinks extends IBase {
  linkName: string;
  marketName: string;
  overlayKey: string;
  tabKey: string;
}
