import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { IBetSelection } from '../betSelection/bet-selection.model';
import { LegPartService } from '@betslip/services/legPart/leg-part.service';
import { SportsLegService } from '../sportsLeg/sports-leg.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';
import { PlaceLegPartService } from '@betslip/services/placeLegPart/place-leg-part.service';

@Injectable({ providedIn: BetslipApiModule })
export class ForecastSportsLegService extends SportsLegService {
  static ngInjectableDef = undefined;

  partsType: any;
  constructor(
    public sportsLegPriceService: SportsLegPriceService,
    public legPartService: LegPartService,
    public betSelectionService: BetSelectionsService
  ) {
    super(sportsLegPriceService, betSelectionService);
    this.partsType = new PlaceLegPartService(this.legPartService, this.betSelectionService);
  }

  construct(params: IBetSelection, docId: number): SportsLeg {
    const extendedParams = this.extendDefault(params);
    return super.construct(extendedParams, docId, this.partsType);
  }

  extendDefault(params: IBetSelection): IBetSelection {
    return _.extend({
      combi: params.type,
      places: '',
    }, params, {
      price: _.extend({
        props: {}
      }, params.price, { priceType: 'DIVIDEND', type: 'DIVIDEND' } ),
      winPlace: params.winPlace ? params.winPlace : 'EXPLICIT_PLACES'
    });
  }
}
