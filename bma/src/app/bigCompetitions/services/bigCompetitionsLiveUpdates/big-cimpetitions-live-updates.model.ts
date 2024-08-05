export interface IBCLiveUpdates {
  type: string;
  message: string;
  channel: {
    id: string;
    name: string;
  };
  subChannel: {
    type: string;
  };
  event: {
    id: string;
  };
}

export interface IUpdatedObject {
  channel: string;
  channel_number: string;
  payload: string;
  subject_number: string;
  subject_type: string;
}
