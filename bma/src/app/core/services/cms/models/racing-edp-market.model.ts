import { IBase } from './base.model';

export interface IRacingEdpMarket extends IBase {
  name: string;
  lang: string;
  description: string;
  birDescription?: string;
  isHR: boolean;
  isGH: boolean;
  isNew: boolean;
}
