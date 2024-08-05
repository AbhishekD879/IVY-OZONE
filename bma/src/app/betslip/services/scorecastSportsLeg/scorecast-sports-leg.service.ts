import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { SportsLegService } from '../sportsLeg/sports-leg.service';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';

@Injectable({ providedIn: BetslipApiModule })
export class ScorecastSportsLegService extends SportsLegService {
  static ngInjectableDef = undefined;

  constructor(
    public sportsLegPriceService: SportsLegPriceService,
    public betSelectionService: BetSelectionsService
  ) {
    super(sportsLegPriceService, betSelectionService);
  }

  construct(selection: IBetSelection, docId: number): SportsLeg {
    const extendedSelection = this.extendDefault(selection);
    return super.construct(extendedSelection, docId);
  }

  extendDefault(params) {
    return _.extend(params, {
      combi: 'SCORECAST',
      winPlace: 'WIN'
    });
  }
}
