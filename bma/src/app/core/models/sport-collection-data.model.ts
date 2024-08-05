import { IMarket } from '@core/models/market.model';

export interface ISportCollectionData {
  id?: string;
  drilldownTagNames?: string;
  name?: string;
  displayOrder?: string;
  markets?: IMarket[];
}
