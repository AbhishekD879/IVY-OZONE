import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { RightMenusRoutingModule } from './right-menus-routing.module';
import { RightMenusListComponent } from './right-menus-list/right-menus-list.component';
import { RightMenusCreateComponent } from './right-menus-create/right-menus-create.component';
import { RightMenusEditComponent } from './right-menus-edit/right-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    RightMenusRoutingModule
  ],
  declarations: [
    RightMenusListComponent,
    RightMenusCreateComponent,
    RightMenusEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class RightMenusModule { }
