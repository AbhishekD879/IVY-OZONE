
import { Base } from './base.model';

export interface StaticBlock extends Base {
  title_brand: string;
  uri: string;
  title: string;
  lang: string;
  enabled: boolean;
  htmlMarkup: string;
}
