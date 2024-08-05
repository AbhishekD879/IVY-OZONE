import {Base} from './base.model';

export interface StaticTextOtf extends Base {
  lang: string;
  enabled: boolean;
  pageName: string;
  title: string;
  ctaText1: string;
  ctaText2: string;
  pageText1: string;
  pageText2: string;
  pageText3: string;
  pageText4: string;
  pageText5: string;
}
