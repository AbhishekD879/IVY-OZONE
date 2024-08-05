import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { BetError } from './bet-error';
import * as _ from 'underscore';
import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetErrorService {

  parse(doc: IBetErrorDoc): BetError {
    return new BetError(doc);
  }

  parseErrors(docs: IBetErrorDoc[]): BetError[] {
    return _.map(docs, this.parse);
  }
}
