import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { FreeBet } from '@betslip/services/freeBet/free-bet';

@Injectable({ providedIn: BetslipApiModule })
export class FreeBetService {

  constructor() {}

  construct(params: IFreeBet): FreeBet {
    return new FreeBet({
      id:  params && params.id ? params.id : null,
      name: params && params.name ? params.name : null,
      value:  params && params.value ? params.value : null,
      expireAt: params && params.expireAt ? params.expireAt : null,
      type: params && params.type ? params.type : null,
      possibleBets: params && params.possibleBets ? params.possibleBets : null,
      freeBetTokenDisplayText: params && params.freeBetTokenDisplayText ? params.freeBetTokenDisplayText : null,
      freeBetOfferCategories: params && params.freeBetOfferCategories ? params.freeBetOfferCategories : null
    });
  }

  parse(elements: IFreeBet[]): FreeBet[] {
    const freeBets: FreeBet[] = [];
    _.each(elements, element => {
      freeBets.push(this.construct(this.parseOne(element)));
    });
    return freeBets;
  }

  parseOne(element: IFreeBet): IFreeBet {
    return {
      id: element.id,
      name: element.offerName,
      value: element.value,
      expireAt: new Date(element.expiry),
      type: element.type,
      possibleBets: element.tokenPossibleBets,
      freeBetOfferCategories: element.freebetOfferCategories,
      freeBetTokenDisplayText: element.freebetTokenDisplayText
    };
  }
}
