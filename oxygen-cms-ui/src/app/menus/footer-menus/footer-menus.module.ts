import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { FooterMenusRoutingModule } from './footer-menus-routing.module';
import { FooterMenusListComponent } from './footer-menus-list/footer-menus-list.component';
import { FooterMenusCreateComponent } from './footer-menus-create/footer-menus-create.component';
import { FooterMenusEditComponent } from './footer-menus-edit/footer-menus-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FooterMenusRoutingModule
  ],
  declarations: [
    FooterMenusListComponent,
    FooterMenusCreateComponent,
    FooterMenusEditComponent
  ]
})
export class FooterMenusModule { }
