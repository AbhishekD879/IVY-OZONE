import { Filename } from './filename.model';
import { Base } from './base.model';

export interface SsoPage extends Base {
  title_brand: string;
  sortOrder: number;
  targetIOS: string;
  targetAndroid: string;
  title: string;
  showOnIOS: boolean;
  showOnAndroid: boolean;
  disabled: boolean;
  heightMedium: number;
  uriMedium: string;
  uriOriginal: string;
  widthMedium: number;
  openLink: string;
  filename: Filename;
}
