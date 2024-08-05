import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { PreplayPopularbetsComponent } from './pre-play-popular-bets.component';
const prePlaypopularBetsModuleRoutes: Routes = [
  {
      path: ':moduleId', component: PreplayPopularbetsComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(prePlaypopularBetsModuleRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class PrePlayPopularBetsRoutingModule { }