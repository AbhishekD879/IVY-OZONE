import * as _ from 'underscore';

import { IBetSelection } from '../betSelection/bet-selection.model';
import { SportsLegPriceService } from '../sportsLegPrice/sports-leg-price.service';
import { Leg } from '../leg/leg';
import { SportsLegPriceModel } from '../sportsLegPrice/sports-leg-price';
import { JsonElement } from '@betslip/services/json-element';
import { IDocRef } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { LegPart } from '@betslip/services/legPart/leg-part';
import { BetSelectionsService } from '@betslip/services/betSelections/bet-selections.service';

export class SportsLeg extends Leg {

  winPlace: boolean | string;
  combi: string;
  price: SportsLegPriceModel;
  selection: IBetSelection;
  docId: number;

  constructor(
    public sportsLegPriceService: SportsLegPriceService,
    public betSelectionsService: BetSelectionsService,
    selection: IBetSelection,
    docId: number,
    partsType?: any
  ) {
    super(betSelectionsService, selection, docId, partsType);

    this.winPlace = selection.winPlace || 'WIN';
    this.combi = selection.combi;
    this.price = selection.price && this.newPrice(selection.price);
    this.selection = selection;
    this.docId = docId;

    this.normalizeCombiName();
  }

  newPrice(priceParams: any) {
    return priceParams.doc
      ? priceParams
      : this.sportsLegPriceService.construct(priceParams);
  }

  doc(isPlacingBet: boolean): IDocRef {
    const parts = _.reduce(this.parts, (legPart, part) => {
        const partTmp = this.renderPart(part).legPart;

        this.setPlaces(this.selection, partTmp);

        return legPart.concat(partTmp);
      }, []),
      combiRef = this.combi ? JsonElement.element('outcomeCombiRef', { id: this.combi }) : {},
      winPlaceRef = JsonElement.element('winPlaceRef', { id: this.winPlace }),
      hasBPG: boolean = _.every(this.parts, part => {
        return part.outcome.details && part.outcome.details.isGpAvailable;
      });

    return _.extend({
        documentId: this.docId
      },
      JsonElement.element('sportsLeg',
        _.extend(this.price.doc(isPlacingBet, hasBPG),
          { legPart: parts },
          combiRef,
          winPlaceRef))
    );
  }

  renderPart(part: LegPart) {
    return part.doc();
  }

  setPlaces(selection: IBetSelection, part) {
    if (selection.combi && selection.combi !== 'SCORECAST') {
      const defaultPlace = { places: part[0].places ? part[0].places : '*' };
      part[0] = _.extend(part[0], defaultPlace);
    }

    return part;
  }

  normalizeCombiName(): void {
    if (/^(FORE|TRI)CAST_COM$/.test(this.combi)) {
      this.combi = this.combi.replace('_COM', '');
    }
  }

}
