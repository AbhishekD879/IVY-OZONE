import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { UserService } from '@core/services/user/user.service';
import { BetStake } from './bet-stake';
import { IStake } from '@betslip/services/betStake/bet-stake.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetStakeService {

  constructor(
    private userService: UserService
  ) { }

  construct(params: IStake): BetStake {
    return new BetStake(params, this.userService);
  }

  parse(doc: IStake, lines: number): BetStake {
    return this.construct({
      amount: doc.amount,
      perLine: doc.stakePerLine,
      max: doc.maxAllowed,
      min: doc.minAllowed,
      currency: this.userService.currency,
      lines
    });
  }
}
