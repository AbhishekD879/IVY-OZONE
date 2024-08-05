import { ISportEvent } from '@core/models/sport-event.model';

export interface ITypeSegment {
  categoryId: string;
  className: string;
  categoryName: string;
  categoryCode: string;
  typeName: string;
  typeId: string;
  classDisplayOrder: number;
  typeDisplayOrder: number;
  typeSectionTitleAllSports: string;
  typeSectionTitleOneSport: string;
  typeSectionTitleConnectApp: string;
  eventCount: number;
  eventsIds: number[];
  events: ISportEvent[];

  // TODO Migration Dynamic params
  marketSelector: string;
  sectionTitle?: string;
  deactivated?: boolean;
  groupedByDate?: any; // TODO fix types, as it is an Array, not an Object , should be IGroupedByDateItem[]
  defaultValue?: string;
  isExpanded?: boolean;
  showAll?: boolean;
  showCashoutIcon?: boolean;
  classId?: string;
  eventsByTypeName?: ITypeSegment[];
  subscriptionKey?: string;
  hasGroupedByDateEvents?: boolean; // a way to check groupedByDate events after applying filters and notify parent component
}

export interface IGroupedByDateObj {
  [key: string]: IGroupedByDateItem;
}

export interface IGroupedByDateItem {
  deactivated: boolean;
  startTime: number;
  events: ISportEvent[];
  title: string;
  marketsAvailability: { [key: string]: string };
}

export interface IFlagsGroup {
  [key: string]: boolean;
}
