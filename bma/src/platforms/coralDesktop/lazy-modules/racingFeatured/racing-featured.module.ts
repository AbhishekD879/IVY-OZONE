import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingFeaturedComponent } from './components/racingFeatured/racing-featured.component';
import { DesktopInspiredVirtualComponent as InspiredVirtualComponent } from './components/inspiredVirtual/inspired-virtual.component';
import { DesktopHorseRaceGridComponent as HorseRaceGridComponent } from './components/raceGrid/horse-race-grid.component';
import {
  RacingPoolIndicatorComponent
} from '@app/lazy-modules/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component';
import { RacingEventsComponent } from './components/racingEvents/racing-events.component';

import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktopModule/desktop.module';
import { VirtualEntryPointBannerModule } from '../virtualEntryPointBanner/virtual-entry-point-banner.module';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule,
    VirtualEntryPointBannerModule
  ],
  providers: [],
  exports: [
    HorseRaceGridComponent,
    RacingEventsComponent,
    RacingPoolIndicatorComponent,
    InspiredVirtualComponent],
  declarations: [
    RacingFeaturedComponent,
    InspiredVirtualComponent,
    HorseRaceGridComponent,
    RacingPoolIndicatorComponent,
    RacingEventsComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingFeaturedModule {
  static entry = RacingFeaturedComponent;
}
