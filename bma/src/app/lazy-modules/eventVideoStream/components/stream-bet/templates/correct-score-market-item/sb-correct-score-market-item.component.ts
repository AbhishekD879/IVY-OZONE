import {
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { CorrectScoreComponent } from '@edp/components/markets/correctScore/correct-score.component';
import { CorrectScoreService } from '@edp/components/markets/correctScore/correct-score.service';


@Component({
  selector: 'sb-correct-score-market-item',
  templateUrl: './sb-correct-score-market-item.component.html',
  styleUrls: ['./sb-correct-score-market-item.component.scss']
})
export class SbCorrectScoreMarketItemComponent extends CorrectScoreComponent {
  @Input() market: IMarket;
  @Input() eventEntity: ISportEvent;
  @Input() marketGroup: IMarket[];
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();
  
  teamHPoints: number[] = [];
  teamAPoints: number[] = [];
  teamHCounterValue: number;
  teamACounterValue: number;

constructor(correctScoreService: CorrectScoreService, filterService: FiltersService){
  super(correctScoreService, filterService);
}
  ngOnInit(): void {
    super.ngOnInit();
    this.groupedOutcomes.forEach(group =>{
      group.forEach(outcome => {
        const points = outcome.outcomeMeaningScores.split(',');
        this.teamHPoints.push(+points[0]);
        this.teamAPoints.push(+points[1])
      });
    });

    this.teamHPoints = [...new Set(this.teamHPoints)].sort((a,b) => a - b);
    this.teamAPoints = [...new Set(this.teamAPoints)].sort((a,b) => a - b);
  }

  handleCounterValueChange(value, homeOrAway) {
    if(homeOrAway === 'H')
      this.teamHCounterValue = value;
    else
      this.teamACounterValue = value;

    this.onScoreChange(value.toString(), homeOrAway);
  }

  handleSelectionClick(market: IMarket) {
      this.selectionClickEmit.emit(market); 
  }
}
