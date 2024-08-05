import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { BankingMenusRoutingModule } from './banking-menus-routing.module';
import { BankingMenusListComponent } from './banking-menus-list/banking-menus-list.component';
import { BankingMenusCreateComponent } from './banking-menus-create/banking-menus-create.component';
import { BankingMenusEditComponent } from './banking-menus-edit/banking-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BankingMenusRoutingModule
  ],
  declarations: [
    BankingMenusListComponent,
    BankingMenusCreateComponent,
    BankingMenusEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class BankingMenusModule { }
