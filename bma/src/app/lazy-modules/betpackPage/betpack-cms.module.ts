import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BetpackCmsService } from '@lazy-modules/betpackPage/services/betpack-cms.service';
import { BetpackEmptyPageComponent } from '@lazy-modules/betpackPage/components/betpackEmptyPage/betpack-empty-page.component';
import { BetpackInfoPageComponent } from '@lazy-modules/betpackPage/components/betpackInfoPage/betpack-info-page.component';
import { SharedModule } from '@sharedModule/shared.module';

import { ReceiptHeaderModule } from '@lazy-modules/receiptHeader/receipt-header.module';
import { BetpackExpiresinTimerComponent } from '@lazy-modules/betpackPage/components/betpack-expiresin-timer/betpack-expiresin-timer.component';

@NgModule({
  imports: [
    SharedModule,

    ReceiptHeaderModule    
  ],
  declarations: [BetpackEmptyPageComponent, BetpackInfoPageComponent,BetpackExpiresinTimerComponent],
  exports: [BetpackEmptyPageComponent, BetpackInfoPageComponent,BetpackExpiresinTimerComponent],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BetpackCmsModule {
  constructor(betpackCmsService: BetpackCmsService) { }
}
