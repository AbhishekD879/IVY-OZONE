export interface IImgServerData {
  'x-forward-for': string;
  timestamp: number;
}

export interface IImgQueryParams {
  auth?: string;
  eventId: string;
  operatorId: string;
  timeStamp: number;
}

export interface IStreamingUrlResponse {
  rtmpUrl: string;
  hlsUrl: string;
}

export interface IImgConfigModel {
  imgSecret: string;
  operatorId: string;
}
