import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import {
  NextRacesHomeTabComponent
} from '@lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';

const routes: Routes = [
  {
    path: '',
    component: NextRacesHomeTabComponent
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
export class LazyNextRacesTabRoutingModule {}
