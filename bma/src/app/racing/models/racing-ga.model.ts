import { ISportEvent } from '@core/models/sport-event.model';

export interface IRacingGaEvent {
  eventCategory: string;
  eventAction: string;
  eventLabel: string;
  eventDetails?: string;
}

export interface IRacingGroup {
  groupName: string;
  cashoutAvailable: boolean;
  liveStreamAvailable: boolean;
  events: ISportEvent[];
  subRegion?: string;
  bogAvailable?: boolean;
  typeDisplayOrder: number;
}

export interface IRacingMap {
  events: ISportEvent[];
  typeNames?: ITypeNamesEvent[];
}

export interface ITypeNamesEvent {
  cashoutAvail: string;
  displayOrder: number;
  typeName: string;
  typeNameEvents: ISportEvent[];
}

export interface IEventsOptions {
  selectedTab: string;
  additionalEventsFromModules?: string[];
  filterByDate?: string;
  drilldownTagNames?: string;
}

export interface IFutureEvent extends ISportEvent {
  link: string;
  date: string;
}

export interface IFilterType {
  name: string;
  typeDisplayOrder: number;
  isExpanded?: boolean
}
