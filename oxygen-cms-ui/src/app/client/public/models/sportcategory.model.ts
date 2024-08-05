import {SvgFilename} from './svgfilename.model';

export interface SportCategory {
  _id: string;
  alt: string;
  brand: string;
  categoryId: number;
  disabled: boolean;
  heightMedium: number;
  heightMediumIcon: number;
  heightSmall: number;
  heightSmallIcon: number;
  imageTitle: string;
  inApp: boolean;
  isTopSport: boolean;
  key: string;
  lang: string;
  link: string;
  path: string;
  showInMenu: boolean;
  sortOrder: number;
  spriteClass: string;
  ssCategoryCode: string;
  svg: string;
  svgId: string;
  targetUri: string;
  updatedAt: string;
  updatedBy: string;
  uriMedium: string;
  uriMediumIcon: string;
  uriSmall: string;
  uriSmallIcon: string;
  widthMedium: number;
  widthMediumIcon: number;
  widthSmall: number;
  widthSmallIcon: number;
  collectionType: string;
  showInAZ: boolean;
  showInHome: boolean;
  showInPlay: boolean;
  heightLarge: number;
  heightLargeIcon: number;
  uriLarge: string;
  widthLarge: number;
  widthLargeIcon: number;
  scoreBoardUri: string;
  filename: SvgFilename;
  icon: SvgFilename;
  svgFilename: SvgFilename;
  highlightCarouselEnabled: boolean;
  quickLinkEnabled: boolean;
  inplayEnabled: boolean;
  messageLabel?: string;
}
