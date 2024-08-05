import { ISeoPagesPaths } from './seo/seo-pages-paths';
import { IProcessedRequestModel } from './process-request.model';
import { ISystemConfig } from './system-config';
import { ISportCategory } from './sport-category.model';
import { IPromotionLite } from './promotion/promotion-lite.model';
import { IFeature } from './feature.model';
import { INavigationPoint } from './navigation-point.model';
import { IFooterMenu } from './menu/footer-menu.model';
import { IOddsBoostConfig } from './odds-boost-config.model';
import { IQuizPopupSettings } from '@core/services/cms/models/quiz-settings.model';
import { IVirtualSportAliasesDto } from '@core/services/cms/models/virtual-sports.model';
import { ITimelineSettings } from '@core/services/cms/models/timeline-settings.model';

export interface IInitialData extends IProcessedRequestModel {
  [name: string]: any;
  seoPages: ISeoPagesPaths;
  footerMenu: IFooterMenu[];
  systemConfiguration: ISystemConfig;
  sportCategories?: ISportCategory[];
  sports?: ISportCategory[];
  initSignposting?: IPromotionLite[];
  features?: IFeature[];
  navigationPoints?: INavigationPoint[];
  oddsBoost: IOddsBoostConfig;
  quizPopupSetting?: IQuizPopupSettings;
  vsAliases: IVirtualSportAliasesDto[];
  timelineConfig?: ITimelineSettings;
  svgSpriteContent: string;
  extraNavigationPoints?:INavigationPoint[];
}
