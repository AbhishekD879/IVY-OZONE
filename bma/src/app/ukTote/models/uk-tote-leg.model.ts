import { IRacingEvent } from '@core/models/racing-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';

export interface IUkToteLeg {
  SUSPENDED_STATUS_CODE: string;
  event: IRacingEvent;
  eventEntity: IRacingEvent;
  filled: boolean;
  index: number;
  isSuspended: boolean;
  linkedMarketId: string;
  marketId: string;
  name: string;
  outcomesMap: { [key: string]: IOutcome; };
  selectedOutcomes: Array<IOutcome>;
  selectedOutcomesIds: Array<string>;
  selectionsCount: number;
  ukToteService: UkToteService;
  isOutcomeSelected: Function;
  selectOutcome: Function;
  deselectOutcome: Function;
}
