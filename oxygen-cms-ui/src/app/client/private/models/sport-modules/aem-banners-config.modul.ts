import {ISportModuleConfig} from '@app/client/private/models/sport-modules/sport-module-config.module';

export interface IAemBannersConfig extends ISportModuleConfig {
  maxOffers: number;
  timePerSlide: number;
  displayFrom: string;
  displayTo: string;
}
