import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SharedModule} from '../shared/shared.module';
import {DialogService} from '../shared/dialog/dialog.service';

import {MenuConfigurationRoutingModule} from './menu-configuration-routing.module';
import {MenuItemManageComponent} from './menu-management/menu-item-manage/menu-item-manage.component';
import {ApiClientService} from '../client/private/services/http';
import {BrandService} from '../client/private/services/brand.service';
import {MenuAddComponent} from './menu-management/menu-add/menu-add.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    MenuConfigurationRoutingModule
  ],
  declarations: [
    MenuItemManageComponent,
    MenuAddComponent
  ],
   providers: [
    DialogService,
    ApiClientService,
    BrandService
  ],
  entryComponents: [
    MenuAddComponent
  ]
})
export class MenuConfigurationModule { }
