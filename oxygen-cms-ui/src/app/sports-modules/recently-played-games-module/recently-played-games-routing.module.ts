import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {
  RecentlyPlayedGamesModulePageComponent
} from '@app/sports-modules/recently-played-games-module/recently-played-games-module-page/recently-played-games-module-page.component';


const routes: Routes = [
  {
    path: ':moduleId',
    component: RecentlyPlayedGamesModulePageComponent,
    children: []
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
export class RecentlyPlayedGamesRoutingModule { }
