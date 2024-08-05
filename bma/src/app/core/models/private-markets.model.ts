import { ISportEvent } from '@core/models/sport-event.model';

export interface IMarketsResponse {
  SSResponse: {
    children: IMarketsChildResponse[]
    xmlns: string;
  };
}

export interface IMarketsChildResponse {
  event: ISportEvent;
  responseFooter: {
    cost: string;
    creationTime: string;
  };
}

export interface ILiveUpdate {
  channel: {
    id: number;
    name: string;
    type: string;
  };
  event: {
    id: number;
  };
  message: {
    lp_den: string;
    lp_num: string;
    status ?: string;
    displayed ?: string;
  };
  subChannel: {
    id: number;
    name: string;
    type: string;
  };
  type: string;
}

