import {
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';


@Component({
  selector: 'sb-over-under-market-item',
  templateUrl: './sb-over-under-market-item.component.html',
  styleUrls: ['./sb-over-under-market-item.component.scss']
})
export class SbOverUnderMarketItemComponent {
  @Input() markets: IMarket[];
  @Input() eventEntity: ISportEvent;
  @Input() allMarkets: IMarket[];
  @Output() selectionClickEmit?: EventEmitter<any> = new EventEmitter();
  
  teamName = 'Total Goals';
  teamHPoints: number[] = [];
  pointsToOutcome = {};
  pointsToMarket = {};
  currOutcomes = [];
  currPoints = 0;
  btnTexts = ['Over', 'Under'];

constructor(
  ){
}
  ngOnInit(): void {
    this.markets.forEach((market) => {
      if(market.rawHandicapValue) {
        this.teamHPoints.push(Number(market.rawHandicapValue));
        this.pointsToOutcome[market.rawHandicapValue] = market.outcomes;
        this.pointsToMarket[market.rawHandicapValue] = market;
      }
    });
    this.teamHPoints.length && this.teamHPoints.sort((a,b) => a-b);
  }

  handleCounterValueChange(value) {
    this.currOutcomes = this.pointsToOutcome[value];
    this.currPoints = value;
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market);
  }
}
