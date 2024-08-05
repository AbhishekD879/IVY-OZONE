import {SvgFilename} from './svgfilename.model';
import {Base} from './base.model';

export interface DesktopQuickLink extends Base {
  collectionType: string;
  disabled: boolean;
  heightMedium: number;
  heightSmall: number;
  lang: string;
  sortOrder: number;
  spriteClass: string;
  target: string;
  title: string;
  uriMedium: string;
  uriSmall: string;
  widthMedium: number;
  widthSmall: number;
  filename: SvgFilename;
  isAtoZQuickLink: boolean;
}
