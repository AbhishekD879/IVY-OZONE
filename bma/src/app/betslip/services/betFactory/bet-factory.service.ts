import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BetService } from '../bet/bet.service';
import { ILegList, ILeg } from '../models/bet.model';
import { Bet } from '../bet/bet';
import { IBet, IBetDoc } from '@betslip/services/bet/bet.model';
import { IBetError } from '@betslip/services/betError/bet-error.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetFactoryService {

  private static getErrsByLeg(errs: IBetError[], leg: any): IBetError[] {
    return _.union(
      _.where(errs, { outcomeId: leg.parts[0].outcome.id }),
      _.where(errs, { legDocId: leg.docId })
    );
  }

  constructor(
    public betService: BetService
  ) {}

  constructBets(betDocs: IBetDoc[] | any, legs: ILegList, errs: IBetError[]): Bet[] {
    return betDocs.length
      ? this.parseBets(betDocs, legs)
      : this.constructTempBets(legs, errs);
  }

  private parseBets(betDocs, legs): Bet[] {
    return betDocs.map(bet => {
      return this.betService.parse(bet, legs);
    });
  }

  private constructTempBets(legs: ILegList, errors: IBetError[]): Bet[] {
    const winLegs = _.reject(legs, leg =>  leg.winPlace === 'EACH_WAY' ); // avoid duplicating bets
    return winLegs.map((leg: ILeg) => {
      return this.betService.construct(<IBet>{
        isMocked: true,
        type: 'SGL', // temporary bet
        betOffer: {},
        allLegs: legs,
        legIds: [leg.docId],
        errs: BetFactoryService.getErrsByLeg(errors, leg),
        lines: this.getTempBetLines(leg),
        docId: leg.docId
      });
    });
  }

  private getTempBetLines(leg: ILeg): number {
    if (leg.combi === 'FORECAST' && leg.selection.places === '*') {
      const len = leg.parts.length;
      return len * (len - 1);
    }

    if (leg.combi === 'TRICAST' && leg.selection.places === '*') {
      const len = leg.parts.length;
      return len * (len - 1) * (len - 2);
    }

    return 1;
  }
}
