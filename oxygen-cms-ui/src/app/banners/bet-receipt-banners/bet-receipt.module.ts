import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';
import { BetReceiptRoutingModule } from './bet-receipt-routing.module';
import { ReceiptCreateComponent } from './receipt-create/receipt-create.component';
import { ReceiptListComponent } from './receipt-list/receipt-list.component';
import { ReceiptEditComponent } from './receipt-edit/receipt-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BetReceiptRoutingModule
  ],
  declarations: [
    ReceiptCreateComponent,
    ReceiptListComponent,
    ReceiptEditComponent
  ],
  providers: [
    DialogService
  ],
  entryComponents: [
    ReceiptCreateComponent
  ]
})
export class BetReceiptModule { }
