import { IBase } from '../base.model';

export interface IBybMarket extends IBase {
  id: string;
  brand: string;
  bybMarket: string;
  incidentGrouping: number;
  marketGrouping: number;
  name: string;
  sortOrder: number;
  marketType?: string;
  popularMarket?: boolean;
  marketDescription?: string;
  stat?: string;
}
