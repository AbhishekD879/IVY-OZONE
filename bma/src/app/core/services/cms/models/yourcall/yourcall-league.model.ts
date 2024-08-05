
import { IBase } from '../base.model';

export interface IYourCallLeague extends IBase {
  sortOrder: number;
  name: string;
  lang: string;
  enabled: boolean;
  typeId: number;
  updatedBy: string;
}
