import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { ForecastSportsLegService } from '../forecastSportsLeg/forecast-sports-leg.service';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { SportsLeg } from '../sportsLeg/sports-leg';

@Injectable({ providedIn: BetslipApiModule })
export class ComplexLegService {

  constructor(
    private forecastSportsLegService: ForecastSportsLegService
  ) {

  }

  getTricastForecastLegs(selection: IBetSelection, legsEntity: SportsLeg[]): SportsLeg[] {
    const lastDocId = this.getLastDocId(legsEntity);
    const leg = this.forecastSportsLegService.construct(selection, lastDocId + 1);

    if (_.includes(['FORECAST', 'TRICAST'], selection.type)) {
      this.setParts(leg);
    }

    return [leg];
  }

  private getLastDocId(legs: SportsLeg[]): number {
    return legs.length ? _.max(legs, leg => leg.docId).docId : 0;
  }

  private setParts(leg: SportsLeg): void {
    _.forEach(leg.parts, (part, i) => {
      part.places = i + 1;
    });
  }
}
