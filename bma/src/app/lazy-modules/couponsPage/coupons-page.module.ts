import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { CouponsModule } from '@lazy-modules/couponsModule/coupons.module';
import { LazyCouponsPageRoutingModule } from './coupons-page-routing.module';

@NgModule({
  imports: [
    CouponsModule,

    LazyCouponsPageRoutingModule
  ],
  declarations: [],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyCouponsPageModule { }
