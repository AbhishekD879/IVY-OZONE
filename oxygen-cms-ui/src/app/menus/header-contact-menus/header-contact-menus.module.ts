import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { HeaderContactMenusRoutingModule } from './header-contact-menus-routing.module';
import { HeaderContactMenusCreateComponent } from './header-contact-menus-create/header-contact-menus-create.component';
import { HeaderContactMenusEditComponent } from './header-contact-menus-edit/header-contact-menus-edit.component';
import { HeaderContactMenusListComponent } from './header-contact-menus-list/header-contact-menus-list.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    HeaderContactMenusRoutingModule
  ],
  declarations: [
    HeaderContactMenusCreateComponent,
    HeaderContactMenusEditComponent,
    HeaderContactMenusListComponent],
  providers: [
    DialogService
  ]
})
export class HeaderContactMenusModule { }
