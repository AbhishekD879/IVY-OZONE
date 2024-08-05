import { finalize } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { LeagueService } from '@app/stats/services/league.service';
import { IStatsAreas } from '@app/stats/models/areas.model';

@Component({
  selector: 'search-leagues',
  templateUrl: 'search-leagues.component.html'
})
export class SearchLeaguesComponent extends AbstractOutletComponent implements OnInit {
  areas: IStatsAreas[];

  constructor(
    private leagueService: LeagueService
  ) {
    super();
  }

  ngOnInit(): void {
    this.leagueService.getAreas().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((areas: IStatsAreas[]) => {
        this.areas = areas;
      }, () => {
        this.showError();
      });
  }
}
