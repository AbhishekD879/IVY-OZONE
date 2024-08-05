import { SvgFilename } from './svgfilename.model';
import { Base } from './base.model';
import { ISegmentModel } from './segment.model';

export interface FooterMenu extends Base, ISegmentModel {
  desktop: boolean;
  disabled: boolean;
  heightMedium: number;
  heightSmall: number;
  imageTitle: string;
  imageTitle_brand: string;
  inApp: boolean;
  lang: string;
  linkTitle: string;
  linkTitle_brand: string;
  mobile: boolean;
  path: string;
  showItemFor: string;
  sortOrder?: number;
  spriteClass: string;
  svg: string;
  svgId: string;
  tablet: boolean;
  targetUri: string;
  uriMedium: string;
  uriSmall: string;
  widthMedium: number;
  widthSmall: number;
  collectionType: string;
  itemType: string;
  heightLarge: number;
  widthLarge: number;
  uriLarge: string;
  authRequired: boolean;
  systemID: number;
  filename: SvgFilename;
  svgFilename: SvgFilename;
  message?: string;
}
