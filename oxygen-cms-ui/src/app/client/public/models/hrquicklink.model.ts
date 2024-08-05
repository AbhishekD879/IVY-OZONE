import {Filename} from './filename.model';

export interface HRQuickLink {
  id: string;
  body: string;
  brand: string;
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
