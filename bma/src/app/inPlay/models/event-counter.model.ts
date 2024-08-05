export interface IEventCounter {
  livenow: string;
  upcoming: string;
  liveStream: string;
  upcomingLiveStream: string;
}

export interface IEventCounterMap {
  [key: string]: IEventCounter;
}
