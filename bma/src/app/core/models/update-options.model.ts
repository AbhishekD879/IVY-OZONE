import { ISportEvent } from '@core/models/sport-event.model';
import { IDelta } from '@core/models/delta-object.model';

export interface IDeleteMarketEventOptions {
  selectionId: string;
  marketId: string;
  eventId: string;
}

export interface IScoreUpdateEventOptions {
  event: ISportEvent;
}

export interface IClocksUpdateEventOptions {
  event: ISportEvent;
  clockData: IDelta;
}
