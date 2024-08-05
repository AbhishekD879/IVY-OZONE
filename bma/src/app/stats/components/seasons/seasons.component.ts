import { concatMap } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import * as _ from 'underscore';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { LeagueService } from '@app/stats/services/league.service';
import { IStatsSeasons } from '../../models/seasons.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'leagues-seasons',
  templateUrl: 'seasons.component.html'
})
export class LeaguesSeasonsComponent extends AbstractOutletComponent implements OnInit {
  seasons: IStatsSeasons[];
  selectedSeason: IStatsSeasons;
  seasonId: string;

  constructor(
    private leagueService: LeagueService,
    private router: Router,
    private route: ActivatedRoute,
    private routingState: RoutingState) {
    super();
  }

  ngOnInit(): void {
    this.route.params.pipe(
      concatMap((params: Params) => {
        this.showSpinner();
        return this.leagueService.getSeasons(params);
      }))
      .subscribe((seasons: IStatsSeasons[]) => {
        const seasonId: string = this.routingState.getRouteParam('seasonId', this.route.snapshot);

        this.seasons = seasons || [];
        this.seasonId = seasonId;
        this.selectedSeason = _.findWhere(this.seasons, { id: this.seasonId }) || this.seasons[0];
        this.hideSpinner();

        if (this.selectedSeason && !seasonId) {
          this.goToStanding(this.selectedSeason);
        }
      }, () => {
        this.showError();
      });
  }

  /**
   * Reload last segment with selected competition
   */
  goToStanding(season: IStatsSeasons): void {
    this.router.navigate(['/leagues', season.sportId, season.areaId, season.competitionId, season.id]);
  }
}
