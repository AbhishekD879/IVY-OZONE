import { Filename } from './filename.model';
import { Base } from './base.model';

export interface HRQuickLink extends Base {
  body: string;
  disabled: boolean;
  heightMedium: number;
  lang: string;
  linkType: string;
  raceType: string;
  sortOrder: number;
  target: string;
  title: string;
  uriMedium: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  widthMedium: number;
  filename: Filename;
}
