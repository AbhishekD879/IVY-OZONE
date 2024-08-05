import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';
import { BetSelection } from './bet-selection';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IOutcome } from '@core/models/outcome.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetSelectionService {

  construct(params: IBetSelection): BetSelection | any {
    return new BetSelection(params);
  }

  restoreSelections(selections: IBetSelection[], outcomes: IOutcome[]): BetSelection[] {
    return selections.map(sel => {
      let params = sel;
      if(sel.isLotto) {
        return this.construct(params);
      }
      params = _.extend({
        outcomes: _.compact(_.map(sel.outcomesIds, id => _.findWhere(outcomes, { id })))
      }, sel);

      return this.construct(params);
    });
  }
}
