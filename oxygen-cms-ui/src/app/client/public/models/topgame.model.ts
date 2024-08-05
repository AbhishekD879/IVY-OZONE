import {SvgFilename} from './svgfilename.model';

export interface TopGame {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  sortOrder: number;
  widthMediumIcon: number;
  heightMediumIcon: number;
  widthSmallIcon: number;
  heightSmallIcon: number;
  widthMedium: number;
  heightMedium: number;
  widthSmall: number;
  heightSmall: number;
  spriteClass: string;
  imageTitle: string;
  lang: string;
  brand: string;
  collectionType: string;
  disabled: boolean;
  path: string;
  alt: string;
  targetUri: string;
  uriMedium: string;
  uriMediumIcon: string;
  uriSmall: string;
  uriSmallIcon: string;
  heightLarge: number;
  heightLargeIcon: number;
  widthLarge: number;
  widthLargeIcon: number;
  uriLargeIcon: string;
  uriLarge: string;
  filename: SvgFilename;
  icon: SvgFilename;
}
