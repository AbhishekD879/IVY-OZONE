import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { IBetslipData } from '@betslip/models/betslip-bet-data.model';

import { el } from '../json-element';
import { ILegList } from '../models/bet.model';
import { BetFactoryService } from '../betFactory/bet-factory.service';
import { Bet } from '../bet/bet';
import { BetErrorService } from '../betError/bet-error.service';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import {
  IBuildBetResponse,
  ILeg
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { LegFactoryService } from '@betslip/services/legFactory/leg-factory.service';

@Injectable({ providedIn: BetslipApiModule })
export class BsDocService {

  action: string;
  docId: string = null;

  constructor(
    public betFactoryService: BetFactoryService,
    private legFactoryService: LegFactoryService,
    private betErrorService: BetErrorService
  ) {}

  el(...args) {
    // @ts-ignore
    return el(...args);
  }

  buildRequest(data) {
    return el(this.action, this.content(data));
  }

  setResponse(response: IBuildBetResponse | any): IBetslipData {
    if(Array.isArray(response) && response[0].isLotto) {
      const lottoBets: Bet[] = this.betFactoryService.constructBets(response, [], []);
      return {bets: lottoBets};
    }
    const legs: ILegList = this.legFactoryService.parseLegs(<ILeg[]>response.legs);
    const errs: IBetError[] = this.betErrorService.parseErrors(response.betErrors || []);
    const bets: Bet[] = this.betFactoryService.constructBets(response.bets || response.bet || [], legs, errs);
    const betOffers = response.betOfferRef || [];

    return { legs, bets, errs, betOffers };
  }

  content(data: any): any {
    // abstract function
    return {};
  }
}
