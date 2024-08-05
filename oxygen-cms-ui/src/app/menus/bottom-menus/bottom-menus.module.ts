import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { BottomMenusRoutingModule } from './bottom-menus-routing.module';
import { BottomMenusListComponent } from './bottom-menus-list/bottom-menus-list.component';
import { BottomMenusCreateComponent } from './bottom-menus-create/bottom-menus-create.component';
import { BottomMenusEditComponent } from './bottom-menus-edit/bottom-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BottomMenusRoutingModule
  ],
  declarations: [
    BottomMenusListComponent,
    BottomMenusCreateComponent,
    BottomMenusEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class BottomMenusModule { }
