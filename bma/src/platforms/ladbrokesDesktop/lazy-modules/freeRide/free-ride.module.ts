import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '@sharedModule/shared.module';
import { LadsDeskLaunchBannerComponent } from '@lazy-modules-module/freeRide/components/launch-banner/launch-banner.component';
import { LadsDeskSecondarySplashPageComponent } from '@lazy-modules-module/freeRide/components/secondary-splash-page/secondary-splash-page.component';

@NgModule({
  declarations: [LadsDeskLaunchBannerComponent, LadsDeskSecondarySplashPageComponent],
  imports: [
    CommonModule,

    SharedModule
  ],
  exports: [
    LadsDeskLaunchBannerComponent,
    LadsDeskSecondarySplashPageComponent
  ]
})
export class FreeRideModule {
  static entry = {
    LadsDeskLaunchBannerComponent,
    LadsDeskSecondarySplashPageComponent
  };
}
