import * as _ from 'underscore';

import { el } from '../json-element';
import { UserService } from '@core/services/user/user.service';
import { IStake } from '@betslip/services/betStake/bet-stake.model';

export class BetStake {

  min: number;
  lines: number;
  placement: number;
  isTraderOffered: boolean = false;
  private stakeMax: number;
  private _amount: number;
  private stakePerLine: string|number;
  private _freeBetAmount: number;

  static formatNumber(arg): number {
    return arg && Number(Number(arg).toFixed(2));
  }

  constructor(private params: IStake, private userService: UserService) {
    this.max = BetStake.formatNumber(params.max);
    this.min = BetStake.formatNumber(params.min) || 0.01;
    this.amount = BetStake.formatNumber(params.amount);
    this.lines = params.lines;
    this.perLine = BetStake.formatNumber(params.perLine);
    this.freeBetAmount = BetStake.formatNumber(params.freeBetAmount);
  }

  get max(): number {
    return this.stakeMax;
  }

  set max(max: number) {
    this.stakeMax = BetStake.formatNumber(max);
  }

  get currency(): string {
    return this.userService.currency;
  }

  set currency(value: string){}

  get amount(): number {
    const value: number = this.placement || <number>this.perLine;
    return BetStake.formatNumber(value * (this.lines || 1)) || this._amount;
  }

  set amount(amount: number) {
    this._amount = amount;
  }

  get perLine(): string|number {
    if (typeof this.stakePerLine === 'string' && this.stakePerLine.charAt(0) === '.') {
      this.stakePerLine = `0${this.stakePerLine}`;
    }
    return _.isNumber(this.stakePerLine) ||
    (this.stakePerLine && this.stakePerLine.match('^\\d{0,12}((\\.|,)\\d{0,2}){0,1}$')) ? this.stakePerLine : '';
  }

  set perLine(value: string|number) {
    this.stakePerLine = value;
  }

  get freeBetAmount(): number {
    return BetStake.formatNumber(this._freeBetAmount);
  }

  set freeBetAmount(amount: number) {
    this._freeBetAmount = amount;
  }

  clone(): BetStake {
    return new BetStake(this.params, this.userService);
  }

  doc(): IStake {
    const stakeElement: Partial<IStake> = {
      amount: this.amount,
      stakePerLine: this.placement || this.amount
    };
    if (this.freeBetAmount) {
      stakeElement.freebet = this.freeBetAmount;
    }

    return <IStake>el('stake', stakeElement,
        [el('currencyRef', { id: this.currency })]
      );
  }
}
