import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { ISurfaceBetEvent } from '@shared/models/surface-bet-event.model';

@Component({
  selector: 'odds-card-surface-bet',
  templateUrl: './odds-card-surface-bet.component.html',
  styleUrls: ['./odds-card-surface-bet.component.scss']
})
export class OddsCardSurfaceBetComponent implements OnInit, OnChanges {
  @Input() surfaceBet: ISurfaceBetEvent;
  @Input() surfaceBetIndex?: number;
  public oldPrice: string;
  public isButton: boolean;
  constructor(protected fracToDecService: FracToDecService) {
  }

  ngOnInit(): void {
    this.setOldPrice();
  }

  ngOnChanges(): void {
    this.isButton = Boolean(this.surfaceBet && this.surfaceBet.markets && this.surfaceBet.markets[0] &&
      this.surfaceBet.markets[0].outcomes && this.surfaceBet.markets[0].outcomes[0]);
    this.setOldPrice();
  }

  private setOldPrice(): void {
    const wasPrice = this.surfaceBet.markets[0]?.outcomes[0]?.name?.toLowerCase().split('(was ');
    if(wasPrice && wasPrice.length > 1) {
      const wasPriceSplit = wasPrice[1].replace(/[)]/ig,'').trim().split('/');
      this.oldPrice = <string>this.fracToDecService.getFormattedValue(
        Number(wasPriceSplit[0]),
        Number(wasPriceSplit[1])
      );
    } else {
      this.oldPrice = undefined;
    }
  }
}
