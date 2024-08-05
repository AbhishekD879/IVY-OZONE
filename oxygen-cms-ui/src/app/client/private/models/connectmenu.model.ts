import { SvgFilename } from './svgfilename.model';
import { Base } from './base.model';
export interface ConnectMenu extends Base {
  linkTitleBrand: string;
  sortOrder: number;
  linkTitle: string;
  level: string;
  lang: string;
  showItemFor: string;
  svg: string;
  svgId: string;
  inApp: boolean;
  upgradePopup: boolean;
  disabled: boolean;
  targetUri: string;
  linkSubtitle: string;
  svgFilename: SvgFilename;
  parent: string;
}
