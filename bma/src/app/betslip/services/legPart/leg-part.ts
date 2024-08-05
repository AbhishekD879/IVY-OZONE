import { IOutcome } from '@core/models/outcome.model';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { JsonElement } from '@betslip/services/json-element';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

export class LegPart {

  places: number | string;
  outcome: IOutcome | IBetSelection;
  constructor(
    public betSelectionsService: BetSelectionsService,
    outcomeParam: IOutcome | IBetSelection
  ) {
    this.outcome = this.betSelectionsService.getOutcome(outcomeParam.id) || outcomeParam;
  }

  doc(): { legPart: ILegPart[] } {
    return JsonElement.element('legPart',
      [JsonElement.element('outcomeRef', { id: this.outcome.id })]
    );
  }
}
