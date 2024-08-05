import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { SportsLegPriceService } from '../sportsLegPrice/sports-leg-price.service';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { SportsLegService } from '../sportsLeg/sports-leg.service';
import { RangeLegPartService } from '../rangeLegPart/range-leg-part.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';

@Injectable({ providedIn: BetslipApiModule })
export class HandicapSportsLegService extends SportsLegService {
  static ngInjectableDef = undefined;

  partsType: RangeLegPartService;
  constructor(
    public sportsLegPriceService: SportsLegPriceService,
    public betSelectionService: BetSelectionsService
  ) {
    super(sportsLegPriceService, betSelectionService);
    this.partsType = new RangeLegPartService(this.betSelectionService);
  }

  construct(params: IBetSelection, docId: number): SportsLeg {
    return super.construct(params, docId, this.partsType);
  }
}
