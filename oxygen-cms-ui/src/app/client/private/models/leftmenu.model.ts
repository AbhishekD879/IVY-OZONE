import { SvgFilename } from './svgfilename.model';
import { Base } from './base.model';

export interface LeftMenu extends Base {
  linkTitleBrand: string;
  sortOrder: number;
  linkTitle: string;
  level: string;
  lang: string;
  showItemFor: string;
  svg: string;
  svgId: string;
  inApp: boolean;
  disabled: boolean;
  targetUri: string;
  svgFilename: SvgFilename;
}
