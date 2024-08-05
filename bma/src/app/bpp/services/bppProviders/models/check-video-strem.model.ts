// CHECK VIDEO STREAM MODELS
import { IVideoStreamModel } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface ICheckVideoStreamRequest {
  eventId: number;
}

export interface ICheckVideoStreamResponse {
  response: ICheckVideoStreamResponseBody;
}

export interface ICheckVideoStreamResponseBody {
  model: IVideoStreamModel;
  returnStatus: {
    code: string;
    debug: string;
    message: string;
  };
  requestTime: string;
}
