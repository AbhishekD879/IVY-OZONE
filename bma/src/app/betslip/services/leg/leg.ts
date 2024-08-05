import * as _ from 'underscore';

import { IOutcome } from '@core/models/outcome.model';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { LegPartService } from '../legPart/leg-part.service';
import { LegPart } from '../legPart/leg-part';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';

export class Leg {

  selection: IBetSelection;
  docId: number;
  parts: LegPart[];
  partsType: LegPartService;

  constructor(
    public betSelections: BetSelectionsService,
    selection: IBetSelection,
    docId: number,
    partsType?: any
  ) {
    this.selection = selection;
    this.docId = docId;
    this.partsType =  partsType || new LegPartService(this.betSelections);
    this.parts = this.constructParts(selection);
  }

  get firstOutcomeId(): string | number {
    return _.first(this.parts).outcome.id;
  }
  set firstOutcomeId(value:string | number){}
  constructParts(selection: IBetSelection): LegPart[] {
    return _.map(selection.outcomes, (outcome: IOutcome) => {
      return this.partsType.construct(outcome, selection);
    });
  }
}
