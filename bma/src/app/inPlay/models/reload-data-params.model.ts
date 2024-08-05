import { IRequestParams } from './request.model';

export interface IReloadDataParams {
  useCache?: boolean;
  additionalParams?: IRequestParams;
}
