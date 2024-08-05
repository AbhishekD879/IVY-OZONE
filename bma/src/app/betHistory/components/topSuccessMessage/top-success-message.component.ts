import { Component, Input, OnInit } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';

@Component({
  selector: 'top-success-message',
  templateUrl: './top-success-message.component.html',
  styleUrls: ['./top-success-message.component.scss']
})
export class TopSuccessMessageComponent implements OnInit {
  @Input() messageTranslateValue: string;
  @Input() value: string;
  @Input() currencySymbol: string;
  @Input() stake: string;
  @Input() betEventSource: RegularBet | CashoutBet;
  @Input() displayProfitIndicator: boolean;

  valueWithCurrency: string;

  constructor(private currencyPipe: CurrencyPipe) {}

  ngOnInit(): void {
    this.valueWithCurrency =  this.currencyPipe.transform(this.value, this.currencySymbol, 'code');
  }

}
