import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingFeaturedComponent } from './components/racingFeatured/racing-featured.component';
import { InspiredVirtualComponent } from './components/inspiredVirtual/inspired-virtual.component';
import { HorseRaceGridComponent } from '@lazy-modules-module/racingFeatured/components/horseRaceGrid/horse-race-grid.component';
import { RacingPoolIndicatorComponent } from '@lazy-modules-module/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component';
import { RacingEventsComponent } from '@lazy-modules-module/racingFeatured/components/racingEvents/racing-events.component';
import { OffersAndFeaturedRacesComponent } from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import { DailyRacingModuleComponent } from '@racing/components/dailyRacing/daily-racing.component';

import { SharedModule } from '@sharedModule/shared.module';
import { VirtualEntryPointBannerModule } from '@lazy-modules-module/virtualEntryPointBanner/virtual-entry-point-banner.module';

@NgModule({
  imports: [
    SharedModule,
    VirtualEntryPointBannerModule
  ],
  providers: [],
  exports: [
    HorseRaceGridComponent,
    RacingPoolIndicatorComponent,
    RacingEventsComponent,
    OffersAndFeaturedRacesComponent,
    InspiredVirtualComponent
  ],
  declarations: [
    RacingFeaturedComponent,
    InspiredVirtualComponent,
    HorseRaceGridComponent,
    RacingPoolIndicatorComponent,
    RacingEventsComponent,
    OffersAndFeaturedRacesComponent,
    DailyRacingModuleComponent,
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingFeaturedModule {
  static entry = RacingFeaturedComponent;
}
