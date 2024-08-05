import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingFeaturedComponent } from '@ladbrokesMobile/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';
import { InspiredVirtualComponent } from '@app/lazy-modules/racingFeatured/components/inspiredVirtual/inspired-virtual.component';
import {
  LadbrokesHorseRaceGridComponent as HorseRaceGridComponent
} from '@ladbrokesMobile/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';

import { LadbrokesRacingPoolIndicatorComponent } from '@ladbrokesMobile/lazy-modules/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component';

import { RacingEventsComponent } from '@ladbrokesMobile/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';
import { DailyRacingModuleComponent } from '@app/racing/components/dailyRacing/daily-racing.component';
/* eslint-disable max-len */
import { LadbrokesOffersAndFeaturedRacesComponent } from '@ladbrokesMobile/racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';

import { SharedModule } from '@sharedModule/shared.module';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service';
import { VirtualEntryPointBannerModule } from '../virtualEntryPointBanner/virtual-entry-point-banner.module';

@NgModule({
  imports: [
    SharedModule,
    VirtualEntryPointBannerModule
  ],
  providers: [
    HorseracingService,
    GreyhoundService
  ],
  exports: [
    HorseRaceGridComponent,
    LadbrokesRacingPoolIndicatorComponent,
    RacingEventsComponent,
    LadbrokesOffersAndFeaturedRacesComponent,
    InspiredVirtualComponent
  ],
  declarations: [
    RacingFeaturedComponent,
    InspiredVirtualComponent,
    HorseRaceGridComponent,
    LadbrokesRacingPoolIndicatorComponent,
    RacingEventsComponent,
    DailyRacingModuleComponent,
    LadbrokesOffersAndFeaturedRacesComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingFeaturedModule {
  static entry = RacingFeaturedComponent;
}
