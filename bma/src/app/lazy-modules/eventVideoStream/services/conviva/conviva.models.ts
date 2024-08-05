import { ISportEvent } from '@core/models/sport-event.model';
import { IConstant } from '@core/services/models/constant.model';
import { Subscription } from 'rxjs';

// Conviva
export interface IConviva {
  Constants: IConstant;
  Analytics: IAnalytics;
}

// Conviva.Analytics
export interface IAnalytics {
  init: (customerKey: string, callbackFunctions?: IConstant, settings?: IConstant) => void;
  buildVideoAnalytics: () => IVideoAnalytics;
  setDeviceMetadata: (deviceMetadata: IConstant) => void;
}

// Conviva VideoAnalytics
export interface IVideoAnalytics {
  setPlayer: (player: IPlayer) => void;
  reportPlaybackRequested: (contentInfo?: IConstant) => void;
  reportPlaybackEnded: () => void;
  setContentInfo: (contentInfo?: IConstant) => void;
  release: () => void;
}

export interface IVideoJsPlayer {
  currentSrc: () => string;
  on: (event: string, callback: Function) => void;
  off: (event: string, callback: Function) => void;
}

export type IPlayer = HTMLVideoElement | IVideoJsPlayer;

export interface IAnalyticsInstance {
  id: string;
  player?: IPlayer;
  videoAnalytics?: IVideoAnalytics;
  eventEntity?: ISportEvent;
  listeners: Function[];
  requested?: boolean;
  subscription?: Subscription;
}
