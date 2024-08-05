import * as _ from 'underscore';

import { LegPart } from '../legPart/leg-part';
import { IOutcome } from '@core/models/outcome.model';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { JsonElement } from '@betslip/services/json-element';
import { IRangeBase } from '../../../bpp/services/bppProviders/bpp-providers.model';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';

export class RangeLegPart extends LegPart {

  range: IRangeBase;
  outcome: IOutcome | IBetSelection;

  constructor(
    public betSelections: BetSelectionsService,
    outcome: IOutcome | IBetSelection,
    range: IRangeBase
  ) {
    super(betSelections, outcome);
    this.outcome = this.betSelectionsService.getOutcome(outcome.id) || outcome;
    this.range = range;
  }


  doc(): { legPart: ILegPart[] } {
    return (
      JsonElement.element('legPart', [
        _.extend(JsonElement.element('range',
          _.extend(
            _.pick(this.range, ['low', 'high']),
            JsonElement.element('rangeTypeRef', { id: this.range.type })
          )
          ),
          JsonElement.element('outcomeRef', { id: this.outcome.id }))])
    );
  }
}
