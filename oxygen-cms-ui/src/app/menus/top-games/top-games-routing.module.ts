import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {TopGamesListComponent} from './top-games-list/top-games-list.component';
import {TopGamesEditComponent} from './top-games-edit/top-games-edit.component';

const routes: Routes = [
  {
    path: 'top-games',
    component: TopGamesListComponent,
    children: []
  },
  {
    path: 'top-games/:id', component: TopGamesEditComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class TopGamesRoutingModule { }
