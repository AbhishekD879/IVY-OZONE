import { IOutcome } from '@core/models/outcome.model';
import { IToteError } from '@app/tote/services/betErrorHandling/tote-errors.model';

export interface IToteOutcome extends IOutcome {
  nonRunner: boolean;
  error?: IToteError;
}
