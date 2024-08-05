import { Base } from './base.model';
import { Filename } from './filename.model';

export interface SportsQuickLink extends Base {
  disabled?: boolean;
  svg?: string;
  svgFilename?: Filename;
  sortOrder?: number;
  destination?: string;
  title?: string;
  sportId?: number;
  pageId?: string;
  pageType?: string;
  validityPeriodEnd?: string;
  validityPeriodStart?: string;
  isValid?: boolean;
  svgId?: string;
  message?: string;
  fanzoneInclusions?: string[];
}
