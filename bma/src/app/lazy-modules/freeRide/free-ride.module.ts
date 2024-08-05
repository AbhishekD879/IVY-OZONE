import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '@sharedModule/shared.module';
import { LaunchBannerComponent } from '@lazy-modules/freeRide/components/launch-banner/launch-banner.component';
import { SplashPopupComponent } from '@lazy-modules/freeRide/components/splash-popup/splash-popup.component';
import { FreeRideOverlayComponent } from '@lazy-modules/freeRide/components/free-ride-overlay/free-ride-overlay.component';
import { SecondarySplashPageComponent } from '@lazy-modules/freeRide/components/secondary-splash-page/secondary-splash-page.component';

@NgModule({
  declarations: [LaunchBannerComponent, SplashPopupComponent, FreeRideOverlayComponent, SecondarySplashPageComponent],
  imports: [
    CommonModule,

    SharedModule
  ]
})

export class FreeRideModule {
  static entry = {
    LaunchBannerComponent,
    SecondarySplashPageComponent
  };
}

