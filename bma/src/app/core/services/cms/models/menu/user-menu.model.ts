import { ISvgFilename } from '../svg-filename.model';
import { IBase } from '../base.model';
import { IProcessedRequestModel } from '../process-request.model';

export interface IUserMenu extends IBase, IProcessedRequestModel {
  activeIfLogout: boolean;
  categoryId?: string;
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
  badge: { name: string };
  filename: ISvgFilename;
  svgFilename: ISvgFilename;
}
