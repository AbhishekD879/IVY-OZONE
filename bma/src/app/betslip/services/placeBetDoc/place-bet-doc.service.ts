import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BsDocService } from '../bsDoc/bs-doc.service';
import { BetFactoryService } from '../betFactory/bet-factory.service';
import { BetErrorService } from '../betError/bet-error.service';
import { ILeg } from '@betslip/services/models/bet.model';
import { IBet } from '@betslip/services/bet/bet.model';
import { LegFactoryService } from '@betslip/services/legFactory/leg-factory.service';

@Injectable({ providedIn: BetslipApiModule })
export class PlaceBetDocService extends BsDocService {
  static ngInjectableDef = undefined;

  private static render(instance: { doc: Function; }): any { // realy don't know
    return instance.doc(true);
  }

  constructor(
    betFactoryService: BetFactoryService,
    legFactoryService: LegFactoryService,
    betErrorService: BetErrorService,
  ) {
    super(betFactoryService, legFactoryService, betErrorService);
  }

  content(data: { doc: Function, [key: string]: any; }): { leg: ILeg[]; bet: IBet[] } {
    // let request: IConstant = {};
    const request = data.doc();
    request.leg = _.map(data.legs, PlaceBetDocService.render);
    request.bet = _.map(data.bets, PlaceBetDocService.render);

    return request;
  }
}
