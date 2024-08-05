import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { BannersSectionComponent } from '@ladbrokesDesktop/lazy-modules/banners/bannersSection/banners-section.component';
import { FormsModule } from '@angular/forms';
import { SharedModule } from '@sharedModule/shared.module';
import { NgOptimizedImage } from '@angular/common';

@NgModule({
  imports: [
    FormsModule,
    SharedModule,
    NgOptimizedImage
  ],
  declarations: [BannersSectionComponent],
  exports: [BannersSectionComponent],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class BannersModule {
  static entry = BannersSectionComponent;
 }
