import { Base } from './base.model';

export interface PaymentMethod extends Base {
  active: boolean;
  identifier: string;
  name: string;
  sortOrder: number;
}
