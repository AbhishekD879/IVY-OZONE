import { BetLegItemComponent as CoralBetLegItemComponent } from '@app/betHistory/components/betLegItem/bet-leg-item.component';
import { Component } from '@angular/core';
import { UNNAMED_FAVOURITES } from '@core/services/raceOutcomeDetails/race-outcome.constant';

@Component({
  selector: 'bet-leg-item',
  templateUrl: './bet-leg-item.component.html',
  styleUrls: [
    '../../../../../app/betHistory/components/betLegItem/bet-leg-item.component.scss',
    './bet-leg-item.component.scss'
  ]
})
export class BetLegItemComponent extends CoralBetLegItemComponent {
  getExcludedDrilldownTagNames(): string {
    const excludedTags = [];

    if (this.bet.eventSource && this.bet.eventSource.betType === 'SGL') {
      excludedTags.push('EVFLAG_MB', 'MKTFLAG_MB');
    }

    if (this.outcomeNames[0] && UNNAMED_FAVOURITES.indexOf(this.outcomeNames[0].toLowerCase()) >= 0) {
      excludedTags.push('MKTFLAG_EPR', 'EVFLAG_EPR');
    }

    return excludedTags.join(',');
  }
}
