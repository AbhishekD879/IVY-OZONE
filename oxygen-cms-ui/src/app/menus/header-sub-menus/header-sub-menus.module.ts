import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { HeaderSubMenusRoutingModule } from './header-sub-menus-routing.module';
import { HeaderSubMenusListComponent } from './header-sub-menus-list/header-sub-menus-list.component';
import { HeaderSubMenusCreateComponent } from './header-sub-menus-create/header-sub-menus-create.component';
import { HeaderSubMenusEditComponent } from './header-sub-menus-edit/header-sub-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    HeaderSubMenusRoutingModule
  ],
  declarations: [
    HeaderSubMenusListComponent,
    HeaderSubMenusCreateComponent,
    HeaderSubMenusEditComponent
  ],
  entryComponents: [
    HeaderSubMenusListComponent,
    HeaderSubMenusCreateComponent,
    HeaderSubMenusEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class HeaderSubMenusModule { }
