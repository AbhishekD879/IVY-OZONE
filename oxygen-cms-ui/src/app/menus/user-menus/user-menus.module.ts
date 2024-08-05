import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';

import { UserMenusRoutingModule } from './user-menus-routing.module';
import { UserMenusListComponent } from './user-menus-list/user-menus-list.component';
import { UserMenusCreateComponent } from './user-menus-create/user-menus-create.component';
import { UserMenusEditComponent } from './user-menus-edit/user-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    UserMenusRoutingModule
  ],
  declarations: [
    UserMenusListComponent,
    UserMenusCreateComponent,
    UserMenusEditComponent
  ]
})
export class UserMenusModule { }
