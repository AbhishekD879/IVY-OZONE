import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { IOutcome } from '@core/models/outcome.model';
import { IBetSelection, IParams } from '../betSelection/bet-selection.model';
import { LegPartService } from '../legPart/leg-part.service';
import { PlaceLegPart } from './place-leg-part';
import { BetSelectionsService } from '../betSelections/bet-selections.service';

@Injectable({ providedIn: BetslipApiModule })
export class PlaceLegPartService {

  constructor(
    private legPartService: LegPartService,
    public betSelections: BetSelectionsService,
  ) {
  }

  construct(outcome: IOutcome | IBetSelection, params: IParams): PlaceLegPart {
    if (params.legParts && params.legParts.length > 0 &&
      (params.combi === 'FORECAST' || params.combi === 'TRICAST')) {
      const childrens = _.reduce(params.legParts, (all: any, part: any) => {
        all[part.outcomeRef.id] = part.places;
        return all;
      }, {});
      params.places = childrens[outcome.id];
    }

    const parent = this.legPartService.construct(outcome);

    return new PlaceLegPart(this.betSelections, parent.outcome, params);
  }
}
