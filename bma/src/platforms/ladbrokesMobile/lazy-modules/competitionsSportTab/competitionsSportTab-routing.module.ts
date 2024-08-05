import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import {
  LadbrokesCompetitionsPageComponent
} from '@ladbrokesMobile/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';

const routes: Routes = [
  {
    path: '',
    component: LadbrokesCompetitionsPageComponent
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
export class LadbrokesCompetitionsTabRoutingModule {}
