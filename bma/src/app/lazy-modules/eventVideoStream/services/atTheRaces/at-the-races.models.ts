export interface IAtrStreamModel {
  Url: string;
  BitrateLevel: string;
  Bitrate: number;
  MediaFormat: string;
  StreamID: number;
}

export interface IAtrRequestParamsModel {
  eventId: string;
  userId: string;
  key: string;
  partnerCode?: string;
  mediaFormat: string;
  secret?: string;
}

export interface IAtrResponseModel {
  IsOK: boolean;
  EventInfo?: {
    Streams: IAtrStreamModel[];
    ContentTypeID: number;
    Country: string;
    Description: string;
    EndDateTime: string;
    EventNumber: number;
    EventType: string;
    GeoRule: { RuleType: string; Countries: string []; };
    ID: string;
    LiveEventStatus: string;
    Location: string;
    StartDateTime: string;
    VOD: boolean;
    VenueCode: string;
  };
  Error?: {
    ErrorCode: string;
    ErrorMessage: string;
  };
}
