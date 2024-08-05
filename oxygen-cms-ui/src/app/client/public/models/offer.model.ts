import {Filename} from './filename.model';

export interface Offer {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  sortOrder: number;
  module: string;
  vipLevelsInput: string;
  targetUri: string;
  displayTo: string;
  displayFrom: string;
  name: string;
  vipLevels: any[];
  brand: string;
  disabled: boolean;
  showOfferTo: string;
  showOfferOn: string;
  useDirectImageUrl: boolean;
  directImageUrl: string;
  imageUri: string;
  image: Filename;
}
