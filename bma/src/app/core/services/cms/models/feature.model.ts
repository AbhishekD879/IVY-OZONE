import { IFilename } from './filename.model';
import { IBase } from './base.model';
import { IProcessedRequestModel } from './process-request.model';

export interface IFeature extends IBase, IProcessedRequestModel {
  title_brand: string;
  sortOrder: number;
  heightMedium: number;
  widthMedium: number;
  uriMedium: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  shortDescription: string;
  title: string;
  vipLevels: any[];
  lang: string;
  showToCustomer: string;
  disabled: boolean;
  description: string;
  filename: IFilename;
}
