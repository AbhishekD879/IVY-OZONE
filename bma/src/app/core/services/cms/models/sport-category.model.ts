import { IProcessedRequestModel } from './process-request.model';
import { IBase } from './base.model';
import { ISportConfig } from './sport-config.model';
import { FanzoneDetails } from '@app/fanzone/models/fanzone.model';

export interface ISportCategory extends IBase, IProcessedRequestModel {
  alt: string;
  categoryId: number;
  categoryCode: string;
  displayOrder: number;
  disabled: boolean;
  heightSmall: number;
  id: string;
  imageTitle: string;
  inApp: boolean;
  isTopSport: boolean;
  path: string;
  scoreBoardUrl: string;
  showInAZ: boolean;
  showInHome: boolean;
  showInPlay: boolean;
  showScoreboard: boolean;
  ssCategoryCode: string;
  svg: string;
  svgId: string;
  targetUri: string;
  uri: string;
  iconClass?: string;
  linkTitle?: string;
  isExpanded?: boolean;
  sportConfig: ISportConfig;

  // ToDo: Dinamyc properties
  hidden: boolean;
  targetUriParts?: string[];
  isActive: boolean;
  selectedFanzone?: FanzoneDetails;
  sortOrder: number;
  fzDisabled?: boolean;
}

