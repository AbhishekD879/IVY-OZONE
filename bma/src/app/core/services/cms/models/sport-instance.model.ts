import { ISportConfig } from './sport-config.model';
import { GamingService } from '@app/core/services/sport/gaming.service';

export interface ISportInstance extends GamingService {
  sportConfig: ISportConfig;
}

export interface ISportInstanceMap {
  [key: string]: ISportInstance;
}
