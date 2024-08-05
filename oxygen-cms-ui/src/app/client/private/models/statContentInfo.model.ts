
import { Base } from './base.model';

export interface StatContentInfo extends Base {
  title: string;
  marketType: string;
  content: string;
  enabled: boolean;
  eventId: string;
  marketId: string;
  startTime: string;
  endTime: string;
}

export interface StatOption {
  value: string;
  text: string;
  type: string;
}

export enum StatContentType{
  'BMOB' = 'Big Match Odds Booster',
  'OB' = 'Odds Booster​',
  'PB' = 'Price Boost',
  'SPB' = 'Super Price Boost'

}
export interface StaticEventTitle{
  eventTitle:string;
  marketIds:[];
}