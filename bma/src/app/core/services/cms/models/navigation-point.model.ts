import { IBase } from './base.model';

export interface INavigationPoint extends IBase {
  categoryId: number[];
  competitionId: string[];
  homeTabs: string[];
  enabled: boolean;
  targetUri: string;
  title: string;
  description: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  ctaAlignment?: string;
  shortDescription?: string;
  themes?: string;
  featureTag?:string;
}

export interface ThemeArray {
  caseVal?: string;
  classVal?: string;
  descVal?: string;
}
