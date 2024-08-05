import { ISportServiceRequestConfig } from '@core/models/sport-service-request-config.model';
import { ISportConfig } from '@app/olympics/models/olympics.model';

export interface ISportServiceConfig {
  categoryType?: string;
  eventMethods?: Object;
  name?: string;
  path?: string;
  tier?: number;
  request?: ISportServiceRequestConfig;
  sportModule?: string;
  tabs?: {
    [key: string]: any
  };
  eventRequest?: any;
  inConnectApp?: boolean;
  scoreboardConfig?: any;
  sportConfig?: ISportConfig;
}
