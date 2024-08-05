import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { HeaderMenusRoutingModule } from './header-menus-routing.module';
import { HeaderMenusListComponent } from './header-menus-list/header-menus-list.component';
import { HeaderMenusCreateComponent } from './header-menus-create/header-menus-create.component';
import { HeaderMenusEditComponent } from './header-menus-edit/header-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    HeaderMenusRoutingModule
  ],
  declarations: [
    HeaderMenusListComponent,
    HeaderMenusCreateComponent,
    HeaderMenusEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class HeaderMenusModule { }
