import { Base } from '@app/client/private/models/base.model';
import { Filename } from '@app/client/private/models/filename.model';
import { Price } from '@app/client/private/models/price.model';
import { SportsModule } from '@app/client/private/models/homepage.model';

export interface SurfaceBet extends Base {
  content: string;
  contentHeader: string;
  disabled: boolean;
  displayFrom: string;
  displayTo: string;
  title: string;
  selectionId: string;
  price: Price;
  sortOrder: number;
  svg: string;
  svgFilename: Filename;
  svgBgId: string;
  svgBgImgPath: string;
  highlightsTabOn: boolean;
  edpOn: boolean;
  displayOnDesktop: boolean;
  references: Reference[];

  categoryIDs?: number[];
  fanzoneInclusions?: string[];
  eventIDs?: string[];
  sportsString?: string;
  message?: string;
}

export interface Reference {
  id: string;
  refId: string;
  relatedTo: string;
  enabled: boolean;
  sortOrder?: number;
}

export interface ActiveSurfaceBets extends SportsModule {
  disabled: boolean;
  highlightsTabOn: boolean;
  edpOn: boolean;
  displayOnDesktop: boolean;
}

export interface FanzoneInclusionList {
  teamId: string;
  active: boolean;
  name: string;
}

export interface SurfaceBetTitle extends Base {
 title ?: string;
}