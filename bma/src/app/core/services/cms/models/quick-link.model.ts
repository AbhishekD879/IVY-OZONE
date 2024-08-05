import { IProcessedRequestModel } from './process-request.model';
import { IFilename } from './filename.model';
import { IBase } from './base.model';

export interface IQuickLink extends IBase, IProcessedRequestModel {
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
  filename: IFilename;
}
