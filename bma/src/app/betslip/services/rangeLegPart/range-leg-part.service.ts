import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { LegPartService } from '../legPart/leg-part.service';
import { IOutcome } from '@core/models/outcome.model';
import { IConstant } from '@core/services/models/constant.model';
import { handicapByMarketCode } from '@betslip/constants/bet-slip.constant';
import { IRangeBase } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { RangeLegPart } from '@betslip/services/rangeLegPart/range-leg-part';

export class RangeLegPartService extends LegPartService {

  range: IRangeBase;
  constructor(
    public betSelections: BetSelectionsService
  ) {
    super(betSelections);
  }

  construct(outcome: IOutcome, params?: any): RangeLegPart {
    if (params.handicap) {
      this.range = {
        type: handicapByMarketCode[params.handicap.type],
        low: params.handicap.raw,
        high: params.handicap.raw
      };
    } else {
      const handicap: IConstant = params.legParts ? params.legParts[0].range : {};
      if (Object.keys(handicap).length) {
        this.range = {
          type: handicap.rangeTypeRef ? handicap.rangeTypeRef.id : '',
          low: handicap.low,
          high: handicap.high
        };
      }
    }
    return new RangeLegPart(this.betSelections, outcome, this.range);
  }
}
