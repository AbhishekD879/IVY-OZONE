import { CUSTOM_ELEMENTS_SCHEMA, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';


import { SharedModule } from '@sharedModule/shared.module';
import { LuckyDipEntryPageComponent } from '@lazy-modules/luckyDip/components/luckyDip-entry-page/luckyDip-entry-page.component';
import { LuckyDipOddsButtonComponent } from '@lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component';
import { SplashModalComponent } from '@lazy-modules/luckyDip/components/splash-modal/splash-modal.component';
import { MarketDescriptionPopupComponent } from '@lazy-modules/luckyDip/components/market-description-popup/market-description-popup.component';
import { LuckyDipBetSelectionComponent } from '@lazy-modules/luckyDip/components/luckyDip-quick-bet/luckyDip-quick-bet.component';
import { AnimationModalComponent } from '@lazy-modules/luckyDip/components/animation-modal/animation-modal.component';

@NgModule({
  declarations: [
    LuckyDipBetSelectionComponent,
    LuckyDipEntryPageComponent,
    LuckyDipOddsButtonComponent,
    SplashModalComponent,
    MarketDescriptionPopupComponent,
    AnimationModalComponent
  ],
  imports: [
    CommonModule,

    SharedModule
  ],
  schemas: [NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA]
})

export class LuckyDipModule {
  static entry = {
    LuckyDipEntryPageComponent,
  };
}

