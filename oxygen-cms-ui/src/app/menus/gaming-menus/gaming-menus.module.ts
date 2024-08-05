import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { GamingMenusRoutingModule } from './gaming-menus-routing.module';
import { GamingMenusListComponent } from './gaming-menus-list/gaming-menus-list.component';
import { GamingMenusEditComponent } from './gaming-menus-edit/gaming-menus-edit.component';
import { GamingMenusCreateComponent } from './gaming-menus-create/gaming-menus-create.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    GamingMenusRoutingModule
  ],
  declarations: [
    GamingMenusListComponent,
    GamingMenusEditComponent,
    GamingMenusCreateComponent
  ],
  providers: [
    DialogService
  ]
})
export class GamingMenusModule { }
