import { Base } from './base.model';

export interface Game extends Base {
  sortOrder: number;
  id: string;
  status: string;
  displayFrom: string;
  displayTo: string;
  highlighted: boolean;
  enabled: boolean;
  events: any;
  prizes: any;
  title: string;
  seasonId?: string;
  isNonPLTeam?:string;
}
