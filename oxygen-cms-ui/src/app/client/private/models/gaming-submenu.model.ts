import { Base } from './base.model';

export interface GamingSubMenu extends Base {
  title: string;
  url: string;
  target: string;
  sortOrder: number;
  externalImageId: string;
  pngFilename: string;
  isNative: Boolean;
}
