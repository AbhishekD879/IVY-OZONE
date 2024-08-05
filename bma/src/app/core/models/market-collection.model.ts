import { IMarket } from './market.model';

export interface IMarketCollection {
  displayOrder?: string;
  drilldownTagNames?: string;
  id?: string;
  index?: number;
  markets?: Array<IMarket>;
  name?: string;
  label?: string;
  marketName?: string;
  url?: string;
  isFiveASideNewIconAvailable?: boolean;
  pills?: IPill[];
}

export interface IPill {
  marketName?: string,
  active?: boolean,
  label?: string,
  index?: number;
}
