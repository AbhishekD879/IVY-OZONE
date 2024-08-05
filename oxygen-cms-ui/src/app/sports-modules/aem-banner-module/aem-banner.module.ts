import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {AemBannerComponent} from '@app/sports-modules/aem-banner-module/editor/aem-banner.component';
import {AemBannerRoutingModule} from '@app/sports-modules/aem-banner-module/aem-banner-routing-module';


@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    AemBannerRoutingModule,
  ],

  declarations: [
    AemBannerComponent,

  ]
})
export class AemBannerModule {}
