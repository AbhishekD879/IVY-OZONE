import { IMarket } from '@core/models/market.model';

export interface IYourcallTab {
  name: string;
  marketName: string;
  url: string;
  markets: IMarket[];
}
