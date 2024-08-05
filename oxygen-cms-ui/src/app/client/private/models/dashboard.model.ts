
import { Base } from './base.model';
export interface Dashboard extends Base {
  estimatedTime: string;
  status: string;
  purgeID: string;
  progressURI: string;
  supportID: string;
  type: string;
  domains: string;
  currentTime: string;
}
