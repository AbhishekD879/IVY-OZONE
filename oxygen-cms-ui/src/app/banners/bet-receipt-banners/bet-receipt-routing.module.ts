import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ReceiptListComponent } from './receipt-list/receipt-list.component';
import { ReceiptEditComponent } from './receipt-edit/receipt-edit.component';

const ReceiptBannersRoutes: Routes = [
  {
    path: '',
    component: ReceiptListComponent,
    children: []
  },
  { path: ':id',  component: ReceiptEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(ReceiptBannersRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class BetReceiptRoutingModule { }
