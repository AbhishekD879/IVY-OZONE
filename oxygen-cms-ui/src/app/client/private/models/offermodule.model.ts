
import { Base } from './base.model';

export interface OfferModule extends Base {
  sortOrder: number;
  name: string;
  disabled: boolean;
  showModuleOn: string;
}
