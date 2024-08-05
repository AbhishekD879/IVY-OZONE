import { finalize } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import * as _ from 'underscore';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { LeagueService } from '@app/stats/services/league.service';
import { IStatsCompetitions, IStatsAreasAndCompetitions } from '@app/stats/models';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'leagues-area',
  templateUrl: 'area.component.html'
})
export class LeaguesAreaComponent extends AbstractOutletComponent implements OnInit {
  area: string;
  competitions: IStatsCompetitions[];
  competition: IStatsCompetitions;
  index: number;

  constructor(
    private leagueService: LeagueService,
    private router: Router,
    private route: ActivatedRoute,
    private routingState: RoutingState) {
    super();
  }

  ngOnInit(): void {
    const areaId: string = this.routingState.getRouteParam('areaId', this.route.snapshot);
    const competitionId: string = this.routingState.getRouteParam('competitionId', this.route.snapshot);

    this.leagueService.getAreaAndCompetitions(areaId).pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((data: { value: IStatsAreasAndCompetitions }) => {
        this.area = data.value.area;
        this.competitions = data.value.competitions;

        const competitionIndex = _.findIndex(this.competitions, { id: competitionId });
        this.index = competitionIndex !== -1 ? competitionIndex : 0;

        if (competitionId) {
          this.competition = this.competitions[this.index];
        } else {
          this.loadCompetition();
        }
      }, () => {
        this.showError();
      });
  }

  goToNext(): void {
    if (this.index !== this.competitions.length - 1) {
      ++this.index;
      this.loadCompetition();
    }
  }

  goToPrev(): void {
    if (this.index !== 0) {
      --this.index;
      this.loadCompetition();
    }
  }

  /**
   * Reload last segment with selected competition
   */
  private loadCompetition(competitionId?: string): void {
    this.competition = this.competitions[this.index];

    if (this.competition) {
      this.router.navigate(['/leagues', this.competition.sportId, this.competition.areaId,
        competitionId || this.competition.id]);
    }
  }
}

