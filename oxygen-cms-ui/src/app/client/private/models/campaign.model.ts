import {Base} from './base.model';

export interface Campaign extends Base {
  name: string;
  displayFrom: string;
  displayTo: string;
  pagesToDisplayOn?: string;
  status: string;
  messagesToDisplayCount: number;
  brand: string;
  isChanged: boolean;
  displayed: boolean;
  highlighted: boolean;
}

export enum CampaignStatus {
  OPEN = 'OPEN',
  LIVE = 'LIVE',
  CLOSED = 'CLOSED'
}
