import { SvgFilename } from './svgfilename.model';
import { Base } from './base.model';

export interface UserMenu extends Base {
  activeIfLogout: boolean;
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
  uriMedium: string;
  uriSmall: string;
  widthMedium: number;
  widthSmall: number;
  collectionType: string;
  heightLarge: number;
  showUserMenu: string;
  svg: string;
  svgId: string;
  uriLarge: string;
  widthLarge: number;
  qa: string;
  filename: SvgFilename;
  svgFilename: SvgFilename;
}
