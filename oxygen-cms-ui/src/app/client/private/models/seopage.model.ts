
import { Base } from './base.model';

export interface SeoPage extends Base {
  changefreq: string;
  description: string;
  disabled: boolean;
  lang: string;
  staticBlock: string;
  title: string;
  url: string;
  urlBrand: string;
  priority: string;
  staticBlockTitle: string;
}
export interface AutoSeoPage extends Base {
  uri?: string;
  metaTitle?: string;
  metaDescription?: string;
}
