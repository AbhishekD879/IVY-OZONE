import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';

import { ConnectMenusRoutingModule } from './connect-menus-routing.module';
import { ConnectMenusListComponent } from './connect-menus-list/connect-menus-list.component';
import { ConnectMenusCreateComponent } from './connect-menus-create/connect-menus-create.component';
import { ConnectMenusEditComponent } from './connect-menus-edit/connect-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ConnectMenusRoutingModule
  ],
  declarations: [
    ConnectMenusListComponent,
    ConnectMenusCreateComponent,
    ConnectMenusEditComponent
  ]
})
export class ConnectMenusModule { }
