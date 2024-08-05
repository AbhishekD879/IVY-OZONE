import { ITypeSegment } from './type-segment.model';

export interface ISportDataStorage {
  LIVE_EVENT?: {
    [key: number]: {
      data: ITypeSegment;
      lastUpdated: number;
    }
  };
  UPCOMING_EVENT?: {
    [key: number]: {
      data: ITypeSegment,
      lastUpdated: number;
    }
  };
}
