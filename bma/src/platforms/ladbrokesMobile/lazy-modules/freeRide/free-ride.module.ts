import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LadsLaunchBannerComponent } from '@lazy-modules-module/freeRide/components/launch-banner/launch-banner.component';
import { LadsSecondarySplashPageComponent } from '@lazy-modules-module/freeRide/components/secondary-splash-page/secondary-splash-page.component';

@NgModule({
  declarations: [LadsLaunchBannerComponent, LadsSecondarySplashPageComponent],
  imports: [
    CommonModule
  ],
  exports: [
    LadsLaunchBannerComponent,
    LadsSecondarySplashPageComponent
  ]
})

export class FreeRideModule {
  static entry = {
    LadsLaunchBannerComponent,
    LadsSecondarySplashPageComponent
  };
}
