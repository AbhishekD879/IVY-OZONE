
import { IBase } from './base.model';

export interface IModuleRibbonTab extends IBase {
  devices?: Array<string>;
  directiveName: string;
  id: string;
  showTabOn: string;
  title: string;
  url: string;
  visible: boolean;

  // TODO: dynamic property
  modules?: any;
  hubIndex?: number;
}
