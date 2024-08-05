import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IHandicapOutcome } from '@betslip/models/betslip-bet-data.model';
import * as _ from 'underscore';

import { modelByType, handicapByMarketCode } from '@betslip/constants/bet-slip.constant';
import { ComplexLegService } from '../complexLeg/complex-leg.service';
import { SportsLegService } from '../sportsLeg/sports-leg.service';
import { ForecastSportsLegService } from '../forecastSportsLeg/forecast-sports-leg.service';
import { ScorecastSportsLegService } from '../scorecastSportsLeg/scorecast-sports-leg.service';
import { HandicapSportsLegService } from '../handicapSportsLeg/handicap-sports-leg.service';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { Leg } from '@betslip/services/leg/leg';
import { IDocRef, ILeg } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { SportsLeg } from '@betslip/services/sportsLeg/sports-leg';

@Injectable({ providedIn: BetslipApiModule })
export class LegFactoryService {


  constructor(
    private complexLegService: ComplexLegService,
    /* eslint-disable */
    private sportsLegService: SportsLegService,
    private forecastSportsLegService: ForecastSportsLegService,
    private scorecastSportsLegService: ScorecastSportsLegService,
    private handicapSportsLegService: HandicapSportsLegService
    /* eslint-enable */
  ) {
  }

  constructLegs(selections: IBetSelection[] | any): SportsLeg[] {
    if(selections.length && selections[0].isLotto) {
      return selections;
    }
    return selections.reduce((legsEntity, sel: IBetSelection) => {
      if (sel.isFCTC) {
        return _.union(
          legsEntity, this.complexLegService.getTricastForecastLegs(sel, legsEntity)
        );
      }

      const straightLeg = [this.constructStrategy(sel, legsEntity.length + 1)],
        eachWayLeg = sel.hasEachWay ? [this.constructStrategy(sel.eachWayOn, legsEntity.length + 2)] : [];
      return _.union(legsEntity, straightLeg, eachWayLeg);
    }, []);
  }

  parseLegs(docs: ILeg[]): ILeg[] {
    return _.map(docs, this.parseStrategy.bind(this));
  }

  private parseStrategy(doc: IDocRef): Leg {
    const type = this.parseCombiType(doc) ||
      this.parseHandicapRangeType(doc) || 'SGL',
      modelClass = this.getModelClass(type);
    return modelClass.parseAndConstruct(doc);
  }

  private constructStrategy(selection: IBetSelection, index: number): SportsLeg | {} {
    const type = this.selectHandicapRangeType(selection) || selection.type,
      model = this.getModelClass(type);
    return model ? model.construct(selection, index) : {};
  }

  private getModelClass(type: string | number): SportsLegService | ForecastSportsLegService |
    ScorecastSportsLegService | HandicapSportsLegService {
    const className = type && modelByType[type];
    return this[className];
  }

  private selectHandicapRangeType(selection: IBetSelection): string {
    return selection.handicap && handicapByMarketCode[(<IHandicapOutcome>selection.handicap).type];
  }

  private parseHandicapRangeType(doc: IDocRef): number | string {
    return (doc.sportsLeg && doc.sportsLeg.legPart && doc.sportsLeg.legPart[0].range) ? doc.sportsLeg.legPart[0].range.rangeTypeRef.id : '';
  }

  private parseCombiType(doc: IDocRef): string {
    return (doc.sportsLeg && doc.sportsLeg.outcomeCombiRef) ? <string>doc.sportsLeg.outcomeCombiRef.id : '';
  }
}
