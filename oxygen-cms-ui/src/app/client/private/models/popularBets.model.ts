import { Base } from '@app/client/private/models/base.model';

export interface PopularBets extends Base {
  active: boolean;
  displayForAllUsers: boolean;
  mostBackedIn: string;
  eventStartsIn: string;
  maxSelections: number;
  betRefreshInterval: number;
  isTimeInHours: boolean;
  type: string;
  isQuickBetReceiptEnabled: boolean;
  enableBackedUpTimes: boolean;
}
