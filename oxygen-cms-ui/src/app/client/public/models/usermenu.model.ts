import {SvgFilename} from './svgfilename.model';

export interface UserMenu {
  id: string;
  activeIfLogout: boolean;
  brand: string;
  disabled: boolean;
  heightMedium: number;
  heightSmall: number;
  lang: string;
  linkTitle: string;
  linkTitle_brand: string;
  path: string;
  sortOrder: number;
  spriteClass: string;
  targetUri: string;
  updatedAt: string;
  uriMedium: string;
  uriSmall: string;
  widthMedium: number;
  widthSmall: number;
  collectionType: string;
  heightLarge: number;
  showUserMenu: string;
  svg: string;
  svgId: string;
  updatedBy: string;
  uriLarge: string;
  widthLarge: number;
  qa: string;
  filename: SvgFilename;
  svgFilename: SvgFilename;
}
