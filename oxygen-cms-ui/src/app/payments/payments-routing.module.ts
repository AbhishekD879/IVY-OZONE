import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EditPaymentComponent } from './edit-payment/edit-payment.component';
import { ListPaymentsComponent } from './list-payments/list-payments.component';

const routes: Routes = [
  {
    path: '',
    component: ListPaymentsComponent,
    children: []
  },
  {
    path: ':id', component: EditPaymentComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class PaymentsRoutingModule { }
