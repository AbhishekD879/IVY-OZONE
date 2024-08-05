import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { GamesPageComponent } from './games-list/games.page.component';
import { GamePageComponent } from './game-edit/pageComponent/game.page.component';

const gamesRoutes: Routes = [
  {
    path: '',
    component: GamesPageComponent,
    children: []
  },
  { path: ':id',
    component: GamePageComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(gamesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class GamesRoutingModule { }
