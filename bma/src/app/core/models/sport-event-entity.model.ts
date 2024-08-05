import { IAggregation } from '@core/models/aggregation.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRacingFormOutcome } from '@core/models/outcome.model';

export interface ISportEventEntity {
  event: ISportEvent;
  aggregation?: IAggregation;
  coupon?: any;
  title?: any;
  id?: any;
  racingFormOutcome?: IRacingFormOutcome
}
