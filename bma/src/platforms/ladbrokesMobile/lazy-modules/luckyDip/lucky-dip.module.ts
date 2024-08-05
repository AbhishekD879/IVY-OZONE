import { NgModule , CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { LadsLuckyDipOddsButtonComponent } from '@ladbrokesMobile/lazy-modules/luckyDip/components/luckyDip-odds-button/luckyDip-odds-button.component';
import { LadsLuckyDipEntryPageComponent } from '@ladbrokesMobile/lazy-modules/luckyDip/components/luckyDip-entry-page/luckyDip-entry-page.component';

@NgModule({
  declarations: [LadsLuckyDipEntryPageComponent, LadsLuckyDipOddsButtonComponent],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports: [
    LadsLuckyDipEntryPageComponent,
    LadsLuckyDipOddsButtonComponent
  ],
  schemas: [NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA]
})

export class LuckyDipModule {
  static entry = {
    LadsLuckyDipEntryPageComponent,
  };
}
