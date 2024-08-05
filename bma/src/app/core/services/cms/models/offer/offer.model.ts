import { IBase } from '../base.model';
import { IProcessedRequestModel } from '../process-request.model';

export interface IOffer extends IBase, IProcessedRequestModel {
  sortOrder: number;
  module: string;
  vipLevelsInput: string;
  targetUri: string;
  routerLink: string[];
  displayTo: string;
  displayFrom: string;
  name: string;
  vipLevels: any[];
  disabled: boolean;
  showOfferTo: string;
  showOfferOn: string;
  useDirectImageUrl: boolean;
  directImageUrl: string;
  imageUri: string;
  image: string;
  moduleName: string;
}
