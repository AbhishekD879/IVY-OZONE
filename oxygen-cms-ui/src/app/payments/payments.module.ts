import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreatePaymentComponent } from './create-payment/create-payment.component';
import { EditPaymentComponent } from './edit-payment/edit-payment.component';
import { ListPaymentsComponent } from './list-payments/list-payments.component';
import { DialogService } from '../shared/dialog/dialog.service';
import { SharedModule } from '../shared/shared.module';
import { PaymentsRoutingModule } from './payments-routing.module';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    PaymentsRoutingModule
  ],
  declarations: [
    CreatePaymentComponent,
    EditPaymentComponent,
    ListPaymentsComponent
  ],
  providers: [
    DialogService
  ],
  entryComponents: [
    CreatePaymentComponent
  ]
})
export class PaymentsModule { }
