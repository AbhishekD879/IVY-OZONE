import { ISportEvent } from '@core/models/sport-event.model';
import { IModuleDataSelection } from './module-data-selection.model';

export interface IHighlightsCarousel {
  _id: string;
  typeId: number;
  data: ISportEvent[];
  outcomeColumnsTitles: string[];
  svgId: string;
  title: string;
  sportId: number;
  inPlay: boolean;
  eventIds: number[];
  dataSelection: IModuleDataSelection;
}

export interface IEagerLoadCMSCount {
  SiteCoreBannerMobile: number;
  SiteCoreBannerDesktop: number;
  HCMobile: number;
  HCDesktop: number
}