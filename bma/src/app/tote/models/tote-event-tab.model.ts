import { IMarket } from '@core/models/market.model';

export interface IToteEventTab {
  categoryId: string;
  id: number;
  label: string;
  url: string;
  isStarted: boolean;
  isResulted: boolean;
  markets: IMarket[];
}

export interface IToteTabsTitle {
  [key: string]: string;
}
