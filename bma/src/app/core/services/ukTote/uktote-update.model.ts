import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

export interface IUkToteLiveUpdateModel {
  id: number;
  payload: {
    ev_mkt_id: number;
    ev_id?: number;
    status: string;
  };
  type: string;
}

export interface IUkToteAllChannelsModel {
  event: number[];
  market: string[];
  outcome: string[];
}

export interface IUkToteUpdateFunctionsModel {
  extendEvent(mainEvent: ISportEvent, extendingEvent: ISportEvent): void;
  extendMarket(market: IMarket, extendingMarket: IMarket): void;
  extendOutcome(outcome: IOutcome | {}, extendingOutcome: IOutcome | {}): void;
}
