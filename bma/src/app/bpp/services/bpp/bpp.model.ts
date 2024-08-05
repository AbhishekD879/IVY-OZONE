import { IAccountFreebetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IError {
  data: IErrorStatus;
  error?: IErrorStatus;
}

interface IErrorStatus {
  status: string;
  message?: string;
}

export interface IFreebestsResponsesCache {
  [key: string]: IAccountFreebetsResponse;
}
