import {
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@app/core/models/outcome.model';


@Component({
  selector: 'sb-single-drop-double-odd-item',
  templateUrl: './sb-single-drop-double-odd-item.component.html',
  styleUrls: ['./sb-single-drop-double-odd-item.component.scss']
})
export class SbSingleDropDoubleOddItemComponent {
  @Input() eventEntity: ISportEvent;
  @Input() market: IMarket;
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();
  
  outcomeEntity: IOutcome
  marketNames: string[] = [];
  mktNameToOutcome = {};
  currOutcomes = [];
  btnTexts = ['Over', 'Under'];

constructor(
  ){
}
  ngOnInit(): void {
    this.market.outcomes.forEach(outcome => {
      const [teamName, outcomeType] = outcome.name.split('and');
      if(!this.marketNames.includes(teamName))
        this.marketNames.push(teamName);

      if(outcomeType.includes('Over'))
        this.mktNameToOutcome[teamName] = !this.mktNameToOutcome[teamName] ? [outcome] : [outcome, ...this.mktNameToOutcome[teamName]];
      else
        this.mktNameToOutcome[teamName] = !this.mktNameToOutcome[teamName] ? [outcome] : [...this.mktNameToOutcome[teamName], outcome];
    });

    this.currOutcomes = this.mktNameToOutcome[this.marketNames[0]];
  }

  onValueChange(outcomeId) {
    if (outcomeId) {
      this.currOutcomes = this.mktNameToOutcome[outcomeId];
    }
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market);
  }
}
