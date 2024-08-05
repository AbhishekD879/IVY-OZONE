import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { CouponsModule } from '@lazy-modules/couponsModule/coupons.module';
import { LazyCouponsListHomeTabRoutingModule } from './coupons-list-home-tab-routing.module';

@NgModule({
  imports: [
    CouponsModule,

    LazyCouponsListHomeTabRoutingModule
  ],
  declarations: [],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyCouponsListHomeTabModule { }
