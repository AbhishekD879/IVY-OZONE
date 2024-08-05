import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { JackpotRoutingModule } from '@lazy-modules/jackpot/jackpot-routing.module';

import { JackpotSportTabService } from '@lazy-modules/jackpot/services/jackpot-sport-tab.service';
import { JackpotReceiptPageService } from '@lazy-modules/jackpot/services/jackpot-receipt-page.service';

import { LuckyDipDialogComponent } from '@lazy-modules/jackpot/components/luckyDipDialog/lucky-dip-dialog.component';
import { HowToPlayDialogComponent } from '@lazy-modules/jackpot/components/howToPlayDialog/how-to-play-dialog.component';
import { JackpotReceiptPageComponent } from '@lazy-modules/jackpot/components/jackpotReceiptPage/jackpot-receipt-page.component';
import { JackpotSportTabComponent } from '@lazy-modules/jackpot/components/jackpotSportTab/jackpot-sport-tab.component';

@NgModule({
  imports: [
    SharedModule,
    JackpotRoutingModule
  ],
  providers: [
    JackpotSportTabService,
    JackpotReceiptPageService
  ],
  declarations: [
    JackpotReceiptPageComponent,
    JackpotSportTabComponent,
    LuckyDipDialogComponent,
    HowToPlayDialogComponent,
  ],
  exports: [
    JackpotReceiptPageComponent,
    JackpotSportTabComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class JackpotModule {
  static entry = JackpotSportTabComponent;
}
