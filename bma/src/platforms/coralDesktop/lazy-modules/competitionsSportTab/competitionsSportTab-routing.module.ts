import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import {
  DesktopCompetitionsPageComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';

const routes: Routes = [
  {
    path: '',
    component: DesktopCompetitionsPageComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class CompetitionsTabRoutingModule {}
