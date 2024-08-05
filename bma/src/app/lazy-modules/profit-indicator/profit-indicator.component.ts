import { Component, Input, OnInit } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { CashoutSectionService } from '@app/betHistory/services/cashOutSection/cash-out-section.service';

@Component({
  selector: 'profit-indicator',
  templateUrl: './profit-indicator.component.html',
  styleUrls: ['./profit-indicator.component.scss']
})
export class ProfitIndicatorComponent implements OnInit {
  @Input() stake: string;
  @Input() betEventSource: RegularBet | CashoutBet;
  @Input() returns: string;
  @Input() currencySymbol: string;

  isProfit: boolean;
  profitValueWithCurency: string;

  constructor(private currencyPipe: CurrencyPipe,
    private cashOutSectionService: CashoutSectionService) { }

  ngOnInit() {
    const stakeValue = Number(this.stake) || Number(this.cashOutSectionService.getInitialStake(this.betEventSource));
    const returnValue = Number(this.returns);
    this.isProfit = returnValue > stakeValue;
    if (this.isProfit) {
      const profitValue = returnValue - stakeValue;
      this.profitValueWithCurency = this.currencyPipe.transform(profitValue, this.currencySymbol, 'code');
    }
  }
}
