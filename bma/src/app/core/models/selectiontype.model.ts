import { SafeHtml } from '@angular/platform-browser';
import { IEventEntity } from '@app/core/models/event-entity.model';

export interface ISelectionType {
  htmlCont?: SafeHtml;
  isSelectionIdAvailable: boolean;
  selection?: string;
  eventInfo?: IEventEntity;
}

