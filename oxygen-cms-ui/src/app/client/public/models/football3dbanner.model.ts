import {Filename} from './filename.model';

export interface Football3DBanner {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  sortOrder: number;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  description: string;
  targetUri: string;
  name: string;
  displayDuration: number;
  disabled: boolean;
  brand: string;
  uriMedium: string;
  uriOriginal: string;
  filename: Filename;
}
