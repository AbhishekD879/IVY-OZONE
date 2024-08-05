import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LeagueLinksListComponent } from './league-links-list/league-links-list.component';
import { LeagueLinksEditComponent } from './league-links-edit/league-links-edit.component';

const LeagueLinksRoutes: Routes = [
  {
    path: '',
    component: LeagueLinksListComponent,
    children: []
  },
  { path: ':id',  component: LeagueLinksEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(LeagueLinksRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class LeagueLinksRoutingModule { }
