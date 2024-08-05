import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { LegService } from '../leg/leg.service';
import { IBetSelection } from '../betSelection/bet-selection.model';
import { SportsLeg } from './sports-leg';
import { SportsLegPriceService } from '../sportsLegPrice/sports-leg-price.service';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { IDocRef } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IParseResponse } from '@betslip/services/betSelection/bet-selection.model';

@Injectable({ providedIn: BetslipApiModule })
export class SportsLegService extends LegService {
  static ngInjectableDef = undefined;

  constructor(
    public sportsLegPriceService: SportsLegPriceService,
    public betSelectionService: BetSelectionsService,
  ) {
    super(betSelectionService);
  }

  construct(selection: IBetSelection, docId: number, partsType?: any): SportsLeg {
    return new SportsLeg(this.sportsLegPriceService, this.betSelectionService, selection, docId, partsType);
  }

  parse(root: IDocRef): IParseResponse {
    const docId = root.documentId,
      sportsLeg = root.sportsLeg,
      legParts = sportsLeg.legPart,
      winPlace = <string>sportsLeg.winPlaceRef.id,
      price = sportsLeg.price,
      priceObj = price && this.sportsLegPriceService.parse(price),
      combi = <string>(sportsLeg.outcomeCombiRef && sportsLeg.outcomeCombiRef.id) || undefined,
      outcomes = legParts.map(part => {
        const outcomeId = part.outcomeRef.id;
        return {
          id: outcomeId,
          price: priceObj
        };
      });
    return {
      docId,
      legParts,
      winPlace,
      price: priceObj,
      combi,
      outcomes
    };
  }
}
