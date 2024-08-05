import { Filename } from './filename.model';
import { Base } from './base.model';

export interface QuickLink extends Base {
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  target: string;
  body: string;
  title: string;
  disabled: boolean;
  lang: string;
  linkType: string;
  raceType: string;
  uriMedium: string;
  filename: Filename;
}
