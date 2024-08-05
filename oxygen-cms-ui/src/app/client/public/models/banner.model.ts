import {Filename} from './filename.model';
import {VipLevel} from './viplevel.model';

export interface Banner {
  id: string;
  alt: string;
  brand: string;
  categoryId: string;
  createdAt: string;
  createdBy: string;
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
  updatedAt: string;
  updatedBy: string;
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
