import { IPayload } from '@core/models/live-serve-update.model';

interface ILiveUpdateChannel {
  id: number;
  name: string;
  type: string;
}

export interface ILiveUpdatePrice {
  lp_num: string;
  lp_den: string;
  raw_hcap?: string;
  ew_avail?: string;
}

interface ILiveUpdateSubChannel {
  type: string;
  id: number;
  name: string;
}

export interface ILiveUpdateResponseSubscribed {
  type: 'SUBSCRIBED';
  channel: string;
}

export interface ILiveUpdateResponseMessage {
  type: 'MESSAGE';
  channel: ILiveUpdateChannel;
  event: { id: number };
  message: ILiveUpdatePrice | IPayload;
  subChannel: ILiveUpdateSubChannel;
}

export interface ILiveUpdateCallback {
  channels: string[];
  handler: Function;
}

export type ILiveUpdateResponse = ILiveUpdateResponseMessage | ILiveUpdateResponseSubscribed;

