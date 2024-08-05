import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { Leg } from './leg';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { JsonElement } from '@betslip/services/json-element';
import { IDocRef } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Injectable()
export class LegService {

  constructor(
    public betSelectionService: BetSelectionsService
  ) {
  }

  construct(selection: IBetSelection, docId?: number): Leg {
    return new Leg(this.betSelectionService, selection, docId);
  }

  parseAndConstruct(_doc: IDocRef): Leg {
    const parseParams = this.parse(_doc);
    const selection = this.betSelectionService.mapParsed(parseParams);
    const params = _.extend({}, selection, parseParams);
    return this.construct(params, params.docId);
  }

  parse(_doc: IDocRef): any {
    return { abstract: 'leg', _doc };
  }

  doc(): { leg: { abstract: 'leg'} } {
    return JsonElement.element('leg', { abstract: 'leg' });
  }
}
