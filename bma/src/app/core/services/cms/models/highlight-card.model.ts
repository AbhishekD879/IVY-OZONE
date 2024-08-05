import { IProcessedRequestModel } from './process-request.model';
import { IBase } from './base.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface IHighlightCard extends IBase, IProcessedRequestModel {
  event: ISportEvent;
}
