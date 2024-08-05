import { ISportSegment } from './sport-segment.model';

export interface IInplayAllSports {
  creationTime: number;
  generation: number;
  liveStream: {
    eventCount: number;
    eventsBySports: ISportSegment[],
    eventsIds: number[];
  };
  livenow: {
    eventCount: number;
    eventsBySports: ISportSegment[],
    eventsIds: number[]
  };
  upcoming: {
    eventCount: number;
    eventsBySports: ISportSegment[],
    eventsIds: number[];
  };
  upcomingLiveStream: {
    eventCount: number;
    eventsBySports: ISportSegment[],
    eventsIds: number[];
  };
}
