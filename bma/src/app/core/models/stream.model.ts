export interface IStreamModel {
  eventId: string;
  userId: string;
  partnerCode: string;
  key: string;
  mediaFormat: string;
  Error: {
    ErrorCode: string
  };
  IsOK: boolean;
  EventInfo: string;
  BitrateLevel: string;
}
