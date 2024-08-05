import { ISportCategory } from '../cms/models';
import { ISportsConfigObject } from '../../models/sports-config.model';

import { ISportBaseConfig, ISportCMSConfig } from '@app/olympics/models/olympics.model';

export interface IModuleExtension {
  extendsModule: string;
  name: string;
  menuConfig: ISportCategory[] | ISportCMSConfig[];
  sportsConfig: ISportsConfigObject | ISportBaseConfig;
}
