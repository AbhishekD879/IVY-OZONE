import {Filename} from './filename.model';

export interface QuickLink {
  id: string;
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  target: string;
  body: string;
  title: string;
  disabled: boolean;
  lang: string;
  brand: string;
  linkType: string;
  raceType: string;
  uriMedium: string;
  filename: Filename;
}
