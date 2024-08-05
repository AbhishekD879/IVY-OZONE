import { IFilename } from '../filename.model';
import { IBase } from '../base.model';
import { IProcessedRequestModel } from '../process-request.model';

export interface IBetReceiptBanner extends IBase, IProcessedRequestModel {
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  disabled: boolean;
  description: string;
  uriMedium: string;
  uriOriginal: string;
  fileUrl: string;
  useUrl: boolean;
  directFileUrl: string;
  useDirectFileUrl: boolean;
  filename: IFilename;
}
