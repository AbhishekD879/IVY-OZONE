export interface ILsSubscribeParams {
  channel: string[];
  module: string;
  group?: string;
}

export interface ILsUnsubscribeParams {
  module: string;
  group?: string;
}

export interface ISubscribersRouteUpdate {
  [key: string]: {
    [key: string]: string[];
  };
}
