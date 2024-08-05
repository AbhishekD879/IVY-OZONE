import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { ISportEvent } from '@app/core/models/sport-event.model';

export interface IEventEntity {
    id: string;
    event: ISportEvent;
    market: IMarket;
    outcome: IOutcome;
}
