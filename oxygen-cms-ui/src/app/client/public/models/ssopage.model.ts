import {Filename} from './filename.model';

export interface SsoPage {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  title_brand: string;
  sortOrder: number;
  targetIOS: string;
  title: string;
  showOnIOS: boolean;
  showOnAndroid: boolean;
  disabled: boolean;
  brand: string;
  heightMedium: number;
  uriMedium: string;
  uriOriginal: string;
  widthMedium: number;
  openLink: string;
  filename: Filename;
}
