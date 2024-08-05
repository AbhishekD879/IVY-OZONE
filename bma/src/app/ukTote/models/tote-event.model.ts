import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IToteOutcome } from '@app/tote/models/tote-outcome.model';
import { IRaceGridMeetingTote } from '@core/models/race-grid-meeting.model';
import { IToteError } from '@app/tote/services/betErrorHandling/tote-errors.model';

export interface IPool {
  currencyCode: string;
  id: string;
  isActive: string;
  legCount: string;
  marketIds: string;
  maxStakePerLine: string;
  maxTotalStake: string;
  minStakePerLine: string;
  minTotalStake: string;
  poolValue: string;
  provider: string;
  label: string;
  url: string;
  stakeIncrementFactor: string;
  type: string;
  poolType?: string;
  guides?: IPoolGuides[];
}

export interface IToteEvent extends ISportEvent {
  pools?: IPool[];
  country?: string;
  defaultPoolType?: string;
  poolsTypesOrdered?: string[];
  markets: IToteMarket[];
  showDistance?: boolean;
  serviceError?: IToteError;
  displayName?: string;
}

export interface IToteEvents {
  events: IToteEvent[];
  meetings: IRaceGridMeetingTote[];
}

export interface IToteMarket extends IMarket {
  outcomes: IToteOutcome[];
}

export interface IPoolGuides {
  poolValue: IPoolValue;
}

export interface IPoolValue {
  id: string;
  poolType: string;
  poolId: string;
  runnerNumber1: string;
  runnerNumber2: string;
  value: string;
}

export interface IExpandedSummary {
  [id: string]: {
    [id: string]: boolean
  };
}
