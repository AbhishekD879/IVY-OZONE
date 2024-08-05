import { Component, Input, OnInit } from '@angular/core';
import { IPoolBet } from './../../models/pool-bet.model';

@Component({
  selector: 'bet-item',
  templateUrl: './bet-item.component.html'
})

export class BetItemComponent implements OnInit {
  @Input() bet: IPoolBet;
  @Input() poolCurrencySymbol: string;
  expanded: boolean;

  ngOnInit(): void {
    this.expanded = false;
  }
}
