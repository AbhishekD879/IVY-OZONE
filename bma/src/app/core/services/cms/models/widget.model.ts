
import { IBase } from './base.model';

export interface IWidget extends IBase {
  columns: string;
  directiveName: string;
  disabled: boolean;
  showExpanded: boolean;
  showOnDesktop: boolean;
  showOnMobile: boolean;
  showOnTablet: boolean;
  sortOrder: number;
  title: string;
  type: string;
  type_brand: string;
  showOn: {
    sports: string[];
    routes: string;
  };

  // TODO: dynamic params
  componentName?: string;
}
