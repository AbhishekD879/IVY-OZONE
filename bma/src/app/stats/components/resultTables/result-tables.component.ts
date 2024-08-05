import { concatMap } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import * as _ from 'underscore';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { LeagueService } from '@app/stats/services/league.service';
import { IStatsResults } from '../../models/results.model';

@Component({
  selector: 'result-tables',
  templateUrl: 'result-tables.component.html'
})

export class ResultTablesComponent extends AbstractOutletComponent implements OnInit {
  results: IStatsResults[];

  constructor(
    private leagueService: LeagueService,
    private route: ActivatedRoute) {
    super();
  }

  ngOnInit(): void {
    this.route.params.pipe(
      concatMap((params: Params) => {
        this.showSpinner();
        return this.leagueService.getStandings(params.competitionId, params.seasonId);
      }))
      .subscribe((data: IStatsResults[]) => {
        this.results = data;
        this.hideSpinner();
      }, () => {
        this.showError();
      });
  }

  getTableValue(values: { key: string, value: string }[], tableKey: string): string {
    const obj = _.findWhere(values, { key: tableKey });
    return obj && obj.value;
  }
}
