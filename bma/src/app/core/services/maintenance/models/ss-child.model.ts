import { IHealthCheck } from './healthcheck.model';
import { IResponseFooter } from './response-footer.model';

export interface ISSChild {
  healthCheck?: IHealthCheck;
  responseFooter?: IResponseFooter;
}
