import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';
import { LeagueService } from './services/league.service';
import { MatchResultsService } from './services/match-results.service';
import { StatsPointsProvider } from './services/stats-points.provider';
import { SearchLeaguesComponent } from './components/searchLeagues/search-leagues.component';
import { ResultTablesComponent } from './components/resultTables/result-tables.component';
import { LeaguesAreaComponent } from './components/area/area.component';
import { LeaguesSeasonsComponent } from './components/seasons/seasons.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
  ],
  providers: [
    LeagueService,
    MatchResultsService,
    StatsPointsProvider
  ],
  exports: [],
  declarations: [
    SearchLeaguesComponent,
    LeaguesAreaComponent,
    ResultTablesComponent,
    LeaguesSeasonsComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})

export class StatsModule {
  constructor(
    private leagueService: LeagueService,
    private matchResultsService: MatchResultsService,
    private asls: AsyncScriptLoaderService
  ) {
    this.leagueService.registerCommand();
    this.matchResultsService.registerCommand();
    this.asls.loadCssFile('assets-stats.css', true, true).subscribe();
    }
}
