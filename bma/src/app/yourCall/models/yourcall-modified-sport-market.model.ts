import { IMarket } from '@core/models/market.model';

export interface IYourcallModifiedSportMarketModel extends IMarket {
  showLimit: number;
  isAllShown: boolean;
}
