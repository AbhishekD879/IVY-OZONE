import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FootballBannersRoutingModule } from './football-banners-routing.module';
import { SharedModule } from '../../shared/shared.module';

import { BannersListComponent } from './banners-list/banners-list.component';
import { BannersEditComponent } from './banners-edit/banners-edit.component';
import { BannersCreateComponent } from './banners-create/banners-create.component';
@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    FootballBannersRoutingModule
  ],
  declarations: [
    BannersListComponent,
    BannersEditComponent,
    BannersCreateComponent
  ],
  entryComponents: [
    BannersCreateComponent
  ]
})
export class FootballBannersModule { }
