import { IBase } from './base.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPrice } from '@core/models/price.model';

export interface IEdpSurfaceBetDto extends IBase {
  selectionEvent: ISportEvent;
  content: string;
  price: IPrice;
  svg: string;
  svgId: string;
  title: string;
  svgBgId: string;
  svgBgImgPath: string;
  contentHeader: string;
}
