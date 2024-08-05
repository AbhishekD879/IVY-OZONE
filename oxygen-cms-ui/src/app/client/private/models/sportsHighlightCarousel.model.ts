import { Base } from '@app/client/private/models/base.model';
import { Filename } from '@app/client/private/models/filename.model';

export interface SportsHighlightCarousel extends Base {
  disabled: boolean;
  displayOnDesktop: boolean;
  displayFrom: string;
  displayTo: string;
  limit: number;
  title: string;
  inPlay: boolean;
  typeId: number;
  typeIds?: string[];
  sportId: number;
  pageId: string;
  pageType: string;
  events: string[];
  sortOrder?: number;
  svgId?: string;
  svg?: string;
  svgFilename?: Filename;
  message?: string;
  fanzoneInclusions?: string[];
  displayMarketType: string;
}

//if values needs to be changed, check with backend to verify in featured microservice
export const marketTypes: string[] = [
  'Primary Market',
  '2Up Market'
];
