import { TableLink } from './table.link.model';

export interface TableColumn {
  name: string;
  property: string;
  width?: number;
  link?: TableLink;
  type?: string;
  isReversed?: boolean;
  subtypes?: string[];
  customOnClickHandler?: Function;
  alignment?: string;
  activeValue?: string;
}
