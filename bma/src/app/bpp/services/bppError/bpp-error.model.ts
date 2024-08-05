export interface IErrorData {
  code?: number;
  status?: string;
  error: string;
}

export interface IErrorResponse {
  data: IErrorData;
  config?: {
    url: string;
  };
  error?: IErrorData;
}

export interface IErrorDataParsed {
  code: string;
  msg: string;
}
