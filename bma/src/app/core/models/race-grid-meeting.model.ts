import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';

export interface IRaceGridMeetingTote {
  events: ISportEvent[];
  liveStreamAvailable?: boolean;
  name: string;
  typeDisplayOrder: number;
}

export interface IClassTypeName {
  cashoutAvail: boolean;
  liveStreamAvailable: boolean;
  name: string;
  typeDisplayOrder?: number;
}

export interface IGroupedRacingItem {
  flag: string;
  data: ISportEvent[];
  displayOrder?: number;
}

export interface IRacingModule {
  classIds?: string | Array<string>;
  typeNames: Array<string>;
  collapsedSections: string | Array<string>;
  eventsBySections?: ITypeSegment;
}

export interface IRaceGridMeeting {
  events: ISportEvent[];
  classesTypeNames: { [key: string]: IClassTypeName[] };
  groupedRacing: IGroupedRacingItem[];
  selectedTab: string;
  modules: { [key: string]: IRacingModule };
}

export interface IRacingPoolIndicator {
  id: number;
  startTime: string;
  link: string;
  poolType: string;
}
