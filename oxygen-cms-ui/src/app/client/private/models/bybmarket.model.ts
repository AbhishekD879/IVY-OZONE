import { Base } from './base.model';

export interface BybMarket extends Base {
  id: string;
  brand: string;
  bybMarket: string;
  incidentGrouping: number;
  marketGrouping: number;
  name: string;
  sortOrder: number;
  marketType: string;
  popularMarket: boolean;
  marketDescription: string;
  stat: string;
}
