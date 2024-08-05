import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { LadsDeskLuckyDipEntryPageComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/luckyDip-entry-page/luckyDip-entry-page.component';
import { LadsDeskLuckyDipOddsButtonComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component';
import { LadsDeskSplashModalComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/splash-modal/splash-modal.component';
import { LadsDeskLuckyDipBetSelectionComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/luckyDip-quick-bet/luckyDip-quick-bet.component';
import { LadsDeskAnimationModalComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/animation-modal/animation-modal.component';
import { LadsDeskLuckyDipBetReceiptComponent } from '@ladbrokesDesktop/lazy-modules/luckyDip/components/luckyDip-bet-receipt/luckyDip-bet-receipt.component';

@NgModule({
    declarations: [
      LadsDeskLuckyDipEntryPageComponent,
      LadsDeskLuckyDipOddsButtonComponent,
      LadsDeskSplashModalComponent,
      LadsDeskLuckyDipBetSelectionComponent,
      LadsDeskAnimationModalComponent,
      LadsDeskLuckyDipBetReceiptComponent
    ],
    imports: [
      CommonModule,
      SharedModule
    ],
    exports: [
        LadsDeskLuckyDipEntryPageComponent,
    ],
    schemas: [NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA]
  })

export class LuckyDipModule {
    static entry = {
      LadsDeskLuckyDipEntryPageComponent,
      LadsDeskLuckyDipBetReceiptComponent
    };
}

