import { Base } from './base.model';

export interface MarketLink extends Base {
  marketName: string;
  linkName: string;
  tabKey: string;
  overlayKey: string;
  enabled: boolean;
}
