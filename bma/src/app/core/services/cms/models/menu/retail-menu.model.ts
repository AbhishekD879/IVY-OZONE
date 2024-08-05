import { IProcessedRequestModel } from '../process-request.model';
import { ISvgFilename } from '../svg-filename.model';
import { IBase } from '../base.model';

export interface IRetailMenu extends IBase, IProcessedRequestModel {
  linkTitleBrand: string;
  sortOrder: number;
  linkTitle: string;
  linkSubtitle: string;
  level: string;
  lang: string;
  showItemFor: string;
  hidden: boolean;
  svg: string;
  svgId: string;
  inApp: boolean;
  disabled: boolean;
  targetUri: string;
  svgFilename: ISvgFilename;
  parent: string;
  upgradePopup: boolean;
}
