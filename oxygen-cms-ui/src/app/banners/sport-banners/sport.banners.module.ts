import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SportBannersRoutingModule } from './sport.banners-routing.module';
import {SportBannersListComponent} from './sport-banners-list/banners.list.component';
import { BannerPageComponent } from './sport-banner-edit/banner.page.component';
import { BannerCreateComponent } from './sport-banner-create/banner.create.component';
import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';
import { BannersApiService } from './service/banners.api.service';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    SportBannersRoutingModule
  ],
  declarations: [
    SportBannersListComponent,
    BannerPageComponent,
    BannerCreateComponent
  ],
  providers: [
    DialogService,
    BannersApiService
  ],
  entryComponents: [
    BannerCreateComponent
  ]
})
export class SportBannersModule { }
