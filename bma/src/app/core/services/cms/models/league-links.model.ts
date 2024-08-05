import { IBase } from './base.model';

export interface ILeagueLink extends IBase {
  obLeagueId: string;
  dhLeagueId: string;
  couponId: string;
  linkName: string;
}
