import { Base } from './base.model';

export interface LeagueLink extends Base {
  obLeagueId: string; // OpenBet League ID
  dhLeagueId: string; // DataHub League ID
  enabled: boolean;
  linkName: string;
  couponIds: Array<number>;
  id: string;
}
