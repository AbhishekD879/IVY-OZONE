import { Base } from './base.model';
import { ISegmentModel } from './segment.model';

export interface NavigationPoint extends Base, ISegmentModel {
  categoryId: string[];
  competitionId: string[];
  homeTabs: string[];
  enabled: boolean;
  targetUri: string;
  title: string;
  bgImageUrl? : string;
  bgAlignmentEnabled?: boolean;
  description: string;
  ctaAlignment?: string;
  shortDescription?: string;
  themes?: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  message?: string;
}

export interface ThemeArray {
  key?: string;
  value?: string;
}

export interface TitleOptions {
  key?: string;
  value?: string;
  config?: {
    title?: { maxLength: number; };
    description?: { maxLength: number; };
    shortDescription?: {
      coral?: { maxLength: number; },
      lads?: { maxLength: number; };
    }
  }
}