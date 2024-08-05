import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import {
  CompetitionsPageComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';

const routes: Routes = [
  {
    path: '',
    component: CompetitionsPageComponent
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
