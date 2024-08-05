import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesLottoBetReceiptComponent } from './components/lotto-bet-recept/lotto-bet-receipt.component';
import { LadbrokesLottoBetslipComponent } from './components/lotto-betslip.component';
@NgModule({
  declarations: [
    LadbrokesLottoBetslipComponent,
    LadbrokesLottoBetReceiptComponent
  ],
  imports: [
    SharedModule,
    CommonModule
  ],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LottoBetslipModule {
  static entry = {LadbrokesLottoBetslipComponent,LadbrokesLottoBetReceiptComponent};
}