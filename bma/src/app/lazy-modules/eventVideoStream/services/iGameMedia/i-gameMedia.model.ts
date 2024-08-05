import { IAtrRequestParamsModel } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.models';
import { IImgConfigModel } from '@lazy-modules/eventVideoStream/services/imgService/img.model';
import { IPerformGroupConfig } from '@lazy-modules/eventVideoStream/models/video-stream.model';

export interface IIGameMediaModel {
  streams?: IIGameMediaStream[];
  details?: IIGameMediaError;
  code?: number;
  description?: string;
  meta?: IPerformGroupConfig | IImgConfigModel | IAtrRequestParamsModel;
  priorityProviderCode?: string;
  priorityProviderName?: string;
}

export interface IIGameMediaError {
  failureCode: string;
  failureDebug: string;
  failureKey: string;
}
export interface IIGameMediaDimensionsModel {
  width: string;
  height: string | Number;
}

export interface IIGameMediaDesktopPropsModel {
  isDesktop: boolean;
  videoDimensions: IIGameMediaDimensionsModel;
}

export interface IIGameMediaStream {
  uniqueStreamName: string;
  streamLink: string;
  eventStatusCode: string;
}

export interface IIGameMediaStreamQualities {
  mobile: string[];
  tablet: string[];
  wrapper: string[];
  desktop: string[];
}

export interface IIGameMediaOptHeaders {
  ViewType?: string;
}

export interface IStreamData {
  streams?: IStream[];
}

export interface IStream {
  streamLink: string;
}
export interface IStreamReplayUrls {
  provider: string;
  streamInfo: {
    bitrateLevel: string;
    streamUrl: string;
  }
  status: string;
  message: string;
  closingStage?: boolean;
  startTime?: number;
  endTime?: number;
}
