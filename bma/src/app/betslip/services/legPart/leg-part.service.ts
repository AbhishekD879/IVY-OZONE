import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { IOutcome } from '@core/models/outcome.model';
import { LegPart } from '@betslip/services/legPart/leg-part';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

@Injectable({ providedIn: BetslipApiModule })
export class LegPartService {

  outcome: IOutcome | IBetSelection;
  constructor(
    public betSelectionsService: BetSelectionsService
  ) {
  }

  construct(outcome: IOutcome | IBetSelection, selection?: IBetSelection): LegPart {
    this.outcome = outcome;
    return new LegPart(this.betSelectionsService, outcome);
  }
}
