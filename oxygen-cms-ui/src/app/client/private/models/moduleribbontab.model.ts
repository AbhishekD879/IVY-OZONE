
import { Base } from './base.model';

export interface ModuleRibbonTab extends Base {
  internalId: string;
  directiveName: string;
  key: string;
  lang: string;
  sortOrder?: number;
  targetUri: string;
  title: string;
  title_brand: string;
  updatedAt: string;
  updatedBy: string;
  visible: boolean;
  showTabOn: string;
  devices: any;
  url: string;
  bybVisible?:boolean;

  // eventhub properties
  displayFrom?: string;
  displayTo?: string;
  hubIndex?: number;
  exclusionList: string[];
  inclusionList: string[];
  applyUniversalSegments: boolean;
  message?: string;
}
