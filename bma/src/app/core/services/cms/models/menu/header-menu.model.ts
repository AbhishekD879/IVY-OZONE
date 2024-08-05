import { IProcessedRequestModel } from './../process-request.model';

import { IBase } from '../base.model';

export interface IHeaderMenu extends IBase, IProcessedRequestModel {
  disabled: boolean;
  lang: string;
  level: string;
  linkTitle: string;
  linkTitle_brand: string;
  sortOrder: number;
  targetUri: string;
  parent: string;
  inApp: boolean;

  isActive: boolean;
}
