import { IProcessedRequestModel } from '../process-request.model';
import { IBase } from '../base.model';

export interface IHeaderSubMenu extends IBase, IProcessedRequestModel {
  disabled: boolean;
  lang: string;
  linkTitle: string;
  linkTitle_brand: string;
  sortOrder: number;
  targetUri: string;
  inApp: boolean;
}
