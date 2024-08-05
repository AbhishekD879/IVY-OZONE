import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';

@Component({
  selector: 'sb-racing-market-item',
  templateUrl: './sb-racing-market-item.component.html',
  styleUrls: ['./sb-racing-market-item.component.scss']
})

export class SbRacingMarketItemComponent {
  @Input() market: IMarket;
  @Input() event: ISportEvent;
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();
  isNumberNeeded: Function;

  constructor(
    private raceOutcomeData: RaceOutcomeDetailsService
  ) {
    this.isNumberNeeded = this.raceOutcomeData.isNumberNeeded;
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market); 
  }

  getTrackById(index: number, entity: any) {
    return `${entity.id}_${index}`;
  }

}
