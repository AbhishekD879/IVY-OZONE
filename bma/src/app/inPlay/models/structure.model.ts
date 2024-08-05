import { ISportSegment } from '@app/inPlay/models/sport-segment.model';

export interface IStructureCache {
  data: IStructureCacheData;
  lastUpdated: number;
}

export interface IStructureCacheData {
  liveStream?: IStructureTopLevelTypeData;
  livenow?: IStructureTopLevelTypeData;
  upcoming?: IStructureTopLevelTypeData;
}

export interface IStructureTopLevelTypeData {
  eventCount: number;
  eventsBySports: ISportSegment[];
  eventsIds: number[];
}

export interface IStructureData {
  creationTime: number;
  generation: number;
  liveStream: IStructureTopLevelTypeData;
  livenow: IStructureTopLevelTypeData;
  upcoming: IStructureTopLevelTypeData;
  upcomingLiveStream:  IStructureTopLevelTypeData;
}
