import { ColumnLink } from './columnLink';

export interface DataTableColumn {
  name: string;
  property: string;
  link?: ColumnLink;
  type?: string;
  width?: number;
  subtypes?: string[];
  isReversed?: boolean;
  customOnClickHandler?: Function;
  alignment?: string;
  activeValue?: string;
  disableSorting?: boolean;
  tab?: string;
}
