import {Filename} from './filename.model';

export interface MaintenancePage {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  name: string;
  desktop: boolean;
  tablet: boolean;
  mobile: boolean;
  targetUri: string;
  brand: string;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
