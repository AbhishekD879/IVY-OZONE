import { Base } from './base.model';

export interface RacingEdpMarket extends Base {
  name: string;
  lang: string;
  description: string;
  isHR: boolean;
  isGH: boolean;
  isNew: boolean;
  racing?: string;
  birDescription?: string;
}
