import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { CouponsModule } from '@lazy-modules/couponsModule/coupons.module';
import { LazySportRoutingModule } from '@sb/sport/sport-routing.module';
import { SportMainModule } from '@ladbrokesMobile/sb/components/sportMain/sport-main.module';

@NgModule({
  imports: [
    SharedModule,
    SportMainModule,
    CouponsModule,

    LazySportRoutingModule
  ],
  declarations: [
  ],
  providers: [],
  exports: [
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazySportModule { }
