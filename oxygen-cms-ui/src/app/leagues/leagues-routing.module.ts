import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LeaguesListComponent } from './leagues-list/leagues-list.component';
import { EditLeagueComponent } from './edit-league/edit-league.component';

const leaguesConfigurationRoutes: Routes = [
  {
    path: '',
    component: LeaguesListComponent,
  },
  { path: ':id',  component: EditLeagueComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(leaguesConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class LeaguesConfigurationRoutingModule { }
