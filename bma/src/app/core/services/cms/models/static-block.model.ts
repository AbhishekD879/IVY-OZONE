import { IBase } from './base.model';

export interface IStaticBlock extends IBase {
  title_brand: string;
  uri: string;
  title: string;
  lang: string;
  enabled: boolean;
  htmlMarkup: string;
}
