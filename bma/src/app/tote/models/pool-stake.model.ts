import { IPool } from './tote-event.model';
import { IStakeValidationState } from '@app/tote/services/betErrorHandling/tote-errors.model';


export interface IPoolStake extends Partial<IStakeValidationState> {
  outcomeId: string;
  value: string;
  poolData: IPool;
}
