import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { SearchLeaguesComponent } from './components/searchLeagues/search-leagues.component';
import { LeaguesAreaComponent } from './components/area/area.component';
import { LeaguesSeasonsComponent } from './components/seasons/seasons.component';
import { ResultTablesComponent } from './components/resultTables/result-tables.component';

const routes: Routes = [{
  matcher: equalPathMatcher,
  component: SearchLeaguesComponent,
  data: {
    segment: 'searchLeagues',
    path: 'search-leagues'
  }
}, {
  path: ':sportId/:areaId',
  component: LeaguesAreaComponent,
  data: {
    segment: 'leaguesArea'
  },
  children: [{
    path: ':competitionId',
    component: LeaguesSeasonsComponent,
    data: {
      segment: 'leaguesSeason'
    },
    children: [{
      path: ':seasonId',
      component: ResultTablesComponent,
      data: {
        segment: 'leaguesResultsTables'
      }
    }]
  }]
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class StatsRoutingModule { }
