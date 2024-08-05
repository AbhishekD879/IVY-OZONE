import { IProcessedRequestModel } from './process-request.model';
import { ISvgFilename } from './svg-filename.model';
import { IBase } from './base.model';

export interface IDesktopQuickLink extends IBase, IProcessedRequestModel {
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
  filename: ISvgFilename;
  isAtoZQuickLink?: boolean;
}
