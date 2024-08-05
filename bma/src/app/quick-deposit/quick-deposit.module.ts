import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '@sharedModule/shared.module';

import { QuickDepositIframeComponent } from '@quickDepositModule/components/quickDepositIframe/quick-deposit-iframe.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule
  ],
  declarations: [
    QuickDepositIframeComponent
  ],
  exports: [
    QuickDepositIframeComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class QuickDepositModule {
  static entry = { QuickDepositIframeComponent };
}
