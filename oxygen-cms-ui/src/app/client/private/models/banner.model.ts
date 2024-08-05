import { Filename } from './filename.model';
import { VipLevel } from './viplevel.model';
import { Base } from './base.model';

export interface Banner extends Base {
  // id: string;
  alt: string;
  categoryId: string;
  categoryName?: string;
  desktopHeightMedium: string;
  desktopTargetUri: string;
  desktopUriMedium: string;
  desktopUriSmall: string;
  desktopWidthMedium: string;
  disabled: boolean;
  imageTitle: string;
  imageTitle_brand: string;
  inApp: boolean;
  lang: string;
  showToCustomer: string;
  sortOrder: number;
  targetUri: string;
  uriMedium: string;
  uriSmall: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  vipLevelsInput: string;
  desktopEnabled: boolean;
  desktopInApp: boolean;
  enabled: boolean;
  desktopFilename: Filename;
  filename: Filename;
  vipLevels: VipLevel[];
}
