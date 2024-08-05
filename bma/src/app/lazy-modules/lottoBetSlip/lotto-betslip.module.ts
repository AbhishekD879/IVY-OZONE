import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LottoBetslipComponent } from './components/lotto-betslip.component';
import { LottoBetReceiptComponent } from './components/lotto-bet-recept/lotto-bet-receipt.component';
@NgModule({
  declarations: [
    LottoBetslipComponent,
    LottoBetReceiptComponent
  ],
  imports: [
    SharedModule
  ],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LottoBetslipModule {
  static entry ={ LottoBetslipComponent, LottoBetReceiptComponent};
}