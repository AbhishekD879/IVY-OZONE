import {SvgFilename} from './svgfilename.model';
import {Filename} from './filename.model';

export interface RightMenu {
  id: string;
  brand: string;
  collectionType: string;
  createdAt: string;
  createdBy: string;
  disabled: boolean;
  heightMedium: number;
  heightSmall: number;
  iconAligment: string;
  inApp: boolean;
  lang: string;
  linkTitle: string;
  linkTitle_brand: string;
  menuItemView: string;
  path: string;
  section: string;
  showItemFor: string;
  sortOrder: number;
  spriteClass: string;
  targetUri: string;
  type: string;
  updatedAt: string;
  updatedBy: string;
  uriMedium: string;
  uriSmall: string;
  widthMedium: number;
  widthSmall: number;
  showOnlyOnIOS: boolean;
  showOnlyOnAndroid: boolean;
  heightLarge: number;
  widthLarge: number;
  svg: string;
  svgId: string;
  qa: string;
  uriLarge: string;
  authRequired: boolean;
  systemID: number;
  filename: SvgFilename;
  svgFilename: Filename;
}
