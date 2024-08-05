import { ISportEvent } from '@core/models/sport-event.model';
import { IPrice } from '@core/models/price.model';

export interface ISurfaceBetEvent extends ISportEvent {
  svg: string;
  svgId: string;
  svgBgId: string;
  svgBgImgPath: string;
  oldPrice: IPrice;
  title: string;
  content: string;
  contentHeader: string;
}
