import * as _ from 'underscore';

import { LegPart } from '../legPart/leg-part';
import { IOutcome } from '@core/models/outcome.model';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { IBetSelection, IParams } from '@betslip/services/betSelection/bet-selection.model';
import { JsonElement } from '@betslip/services/json-element';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';

export class PlaceLegPart extends LegPart {

  places: number | string;
  outcome: IOutcome | IBetSelection;

  constructor(
    public betSelections: BetSelectionsService,
    outcome: IOutcome | IBetSelection,
    params: IParams
  ) {
    super(betSelections, outcome);
    this.outcome = outcome;
    this.places = this.getPlaces(params);
  }

  get data(): number | string {
    return this.places;
  }

  set data(place: number | string) {
    this.places = place;
  }

  getPlaces(params: IParams): string {
    return _.isObject(params.places)
       ? (params.places[this.outcome.id] || '*')
       : params.places;
  }

  doc(): { legPart: ILegPart[]; } {
    const places = this.places ? { places: this.places } : {};
    return (
      JsonElement.element('legPart', [_.extend(places,
        JsonElement.element('outcomeRef', { id: this.outcome.id }))])
    );
  }
}
