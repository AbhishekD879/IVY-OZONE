
import { Base } from './base.model';

export interface YourCallLeague extends Base {
  sortOrder: number;
  name: string;
  lang: string;
  enabled: boolean;
  activeFor5aSide: boolean;
  typeId: number;
  updatedBy: string;
}
