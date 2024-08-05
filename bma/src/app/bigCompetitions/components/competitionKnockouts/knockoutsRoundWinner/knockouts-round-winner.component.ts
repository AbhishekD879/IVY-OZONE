import { Component, Input } from '@angular/core';
import {
  IEventsByRoundMap,
  IKnockoutRounds
} from '@app/bigCompetitions/services/competitionKnockouts/competition-knockouts.model';

@Component({
  selector: 'knockouts-round-winner',
  templateUrl: 'knockouts-round-winner.component.html'
})
export class KnockoutsRoundWinnerComponent {
  @Input() abbr: string;
  @Input() eventsByRound: IEventsByRoundMap;
  @Input() round: IKnockoutRounds;
}
