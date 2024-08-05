import {IInplayConfig} from './homeInplayConfig.model';
import {IRpgConfigModel} from '@app/client/private/models/rpgConfig.model';
import {IRacingConfig} from '@app/client/private/models/racingConfig.model';
import {IAemBannersConfig} from '@app/client/private/models/sport-modules/aem-banners-config.modul';
import { IPrePlayPopularBets } from './prePlaypopularBets.model';

export class SportsModule {
  id: string;
  brand: string;
  identifier: string;
  moduleType?: string;
  title: string;
  href?: string;
  enabled: boolean;
  disabled?: boolean;
  sportId?: number;    // deprecated
  pageType?: string; // "sport" or "eventhub"
  pageId?: string;   // sport id or eventhubIndex
  sortOrder: number;
  publishedDevices: string[] = [];
  inplayConfig?: IInplayConfig;
  rpgConfig?: IRpgConfigModel;
  moduleConfig?: IAemBannersConfig;
  racingConfig?: IRacingConfig;
  teamAndFansBetsConfig :any;
  popularBetConfig?: IPrePlayPopularBets;

  constructor(sportId: number,
              pageType: string,
              moduleType: string,
              title: string,
              enabled: boolean,
              sortOrder: number,
              inplayConfig?: IInplayConfig,
              rpgConfig?: IRpgConfigModel,
              moduleConfig?: IAemBannersConfig,
              racingConfig?: IRacingConfig,
              popularBetConfig?: IPrePlayPopularBets) {
    this.sportId = sportId;
    this.pageId = sportId.toString();
    this.pageType = pageType;
    this.moduleType = moduleType;
    this.title = title;
    this.enabled = enabled;
    this.sortOrder = sortOrder;
    this.inplayConfig = inplayConfig || null;
    this.rpgConfig = rpgConfig || null;
    this.moduleConfig = moduleConfig || null;
    this.racingConfig = racingConfig || null;
    this.popularBetConfig = popularBetConfig || null;
  }
}

