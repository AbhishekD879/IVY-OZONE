import { IIGameMediaModel } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';

export interface IPerformGroupConfig {
  partnerId?: string;
  seed?: string;
  CSBIframeEnabled: boolean;
  CSBIframeSportIds: string;
}

export interface IQuantumLeapTimeRangeConfig {
  startTime: string;
  endTime: string;
}

export interface I24BppResponse {
  response: {
    model: {
      betSummary: { date: string; }[];
    }
  };
}

export type IStreamResponse = string | IStreamResponseObject;

export interface IStreamResponseObject {
  eventInfo?: {
    availableMediaFormats?: {
      mediaFormat: IStreamMediaFormat[]
    }
  };
}

export interface IStreamMediaFormat {
  playerAlias: string;
  stream: IStreamLanchData[];
}

interface IStreamLanchData {
  streamLaunchCode: string[];
}

export interface IStreamProvidersResponse extends IIGameMediaModel {
  listOfMediaProviders: IStreamProvidersData[];
  SSResponse: IMediaProvidersData;
  priorityProviderName: string;
  priorityProviderCode: string;
  stream: string;
  error: string;
}

// STREAM PROVIDERS
export interface IStreamProvidersData {
  children: IStreamProvider[];
  name: string;
}

export interface IStreamProvider {
  media: {
    accessProperties
  };
}

// MEDIA PROVIDERS
export interface IMediaProvidersData {
  children: IMediaProvider[];
}

interface IMediaProvider {
  mediaProvider: {
    children: IStreamProvider[];
    name: string;
  };
}

export interface IPerformGroupParams {
  userId: string;
  partnerId: string;
  eventId: string;
  key?: string;
}

export interface IPerformIframeDimensions {
  width: number;
  height: number;
}

export interface IStreamRequestConfig {
  performGroupId: string;
  isNormalInteger: boolean;
  partnerId: string;
  userId: string;
  key: string;
}

export interface IStreamRequestParams {
  baseUrl: string;
  queryString: string;
}

export interface IStreamDetail {
  detail: IDetails;
}

interface IDetails {
  selectionId: string;
  settingValue: boolean;
  isOpen: boolean;
}
