import { Filename } from './filename.model';
import { Base } from './base.model';

export interface Offer extends Base {
  sortOrder: number;
  module: string;
  vipLevelsInput: string;
  targetUri: string;
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
  image: Filename;
  moduleName: string;
}
