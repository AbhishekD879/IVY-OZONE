
import { Base } from './base.model';

export interface Widget extends Base {
  columns: string;
  disabled: boolean;
  showExpanded: boolean;
  showOnDesktop: boolean;
  showOnMobile: boolean;
  showOnTablet: boolean;
  sortOrder: number;
  title: string;
  type: string;
  type_brand: string;
  showFirstEvent: boolean;
  showOn: {
    sports: string[];
    routes: string;
  };
}
