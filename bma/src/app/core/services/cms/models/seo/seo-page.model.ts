
import { IBase } from '../base.model';

export interface ISeoPage extends IBase {
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
export interface IEventPageSeo {
  outcomeMeaningMinorCode: number;
  name: string;
  href: string;
}
export interface IAutoSeoPage {
  metaTitle?: string;
  metaDescription?: string;
}

export interface IAutoSeoData {
  isOutright?: boolean;
  typeName?: string;
  categoryName?: string;
  name?: string;
}
