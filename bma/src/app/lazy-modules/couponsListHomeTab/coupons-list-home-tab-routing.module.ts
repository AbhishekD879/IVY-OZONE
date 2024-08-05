import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CouponsListSportTabComponent } from '@sbModule/components/couponsListSportTab/coupons-list-sport-tab.component';

const routes: Routes = [
  {
    path: ':sport',
    component: CouponsListSportTabComponent,
    data: {
      segment: 'coupons'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyCouponsListHomeTabRoutingModule { }
