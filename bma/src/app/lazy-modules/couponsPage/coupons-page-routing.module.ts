import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CouponsDetailsComponent } from '@sbModule/components/couponsDetails/coupons-details.component';

const routes: Routes = [
  {
    path: '',
    children: [{
      path: ':sport',
      pathMatch: 'full',
      redirectTo: '/sport/:sport/coupons'
    }, {
      path: ':sport/:couponName',
      pathMatch: 'full',
      redirectTo: '/sport/:sport/coupons'
    }, {
      path: ':sport/:couponName/:couponId',
      component: CouponsDetailsComponent,
      data: {
        segment: 'couponsDetails'
      }
    }]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyCouponsPageRoutingModule { }
