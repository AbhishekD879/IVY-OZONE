import { Base } from './base.model';

export interface MarketSelector extends Base {
  title: string;
  templateMarketName: string;
  header: string[];
  sortOrder: number;
}

/**
 *  uiModel differs from backend
 *  input field for headers is string, backend model requires array (see above)
 */
export interface MarketSelectorExt extends MarketSelector {
  headerStr: string;
}
