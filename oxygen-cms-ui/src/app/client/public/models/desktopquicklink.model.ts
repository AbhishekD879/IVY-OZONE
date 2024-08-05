import {SvgFilename} from './svgfilename.model';

export interface DesktopQuickLink {
  id: string;
  brand: string;
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
}
