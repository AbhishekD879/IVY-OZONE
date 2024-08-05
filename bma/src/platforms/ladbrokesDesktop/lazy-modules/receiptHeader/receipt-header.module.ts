import { ReceiptHeaderComponent } from '@ladbrokesMobile/lazy-modules/receiptHeader/components/receiptHeader/receipt-header.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    ReceiptHeaderComponent
  ],
  providers: [],
  exports: [
    ReceiptHeaderComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class ReceiptHeaderModule {
  static entry = ReceiptHeaderComponent;
}
