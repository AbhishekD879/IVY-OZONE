import { Component, Input, OnInit } from '@angular/core';
import { CompetitionKnockoutsService } from '@app/bigCompetitions/services/competitionKnockouts/competition-knockouts.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IBCModule } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import {
  IEventsByRoundMap,
  IKnockoutRounds
} from '@app/bigCompetitions/services/competitionKnockouts/competition-knockouts.model';

@Component({
  selector: 'competition-knockouts',
  templateUrl: 'competition-knockouts.component.html'
})
export class CompetitionKnockoutsComponent implements OnInit {
  @Input() moduleConfig: IBCModule;
  eventsByRound: IEventsByRoundMap;

  constructor(private competitionKnockoutsService: CompetitionKnockoutsService,
              private windowRef: WindowRefService) {}

  ngOnInit(): void {
    this.eventsByRound = this.competitionKnockoutsService.parseData(this.moduleConfig);
    this.scrollToActiveRound();
  }

  trackByStatus(index: number, round: IKnockoutRounds): string {
    return `${index}${round.active}`;
  }

  scrollToActiveRound(): void {
    const document: HTMLDocument = this.windowRef.document;
    setTimeout(() => {
      const element: HTMLElement = document.querySelector('.active-round');
      if (element) {
        const top: number = element.offsetTop;
        window.scrollTo(0, top);
      }
    }, 100);
  }
}
