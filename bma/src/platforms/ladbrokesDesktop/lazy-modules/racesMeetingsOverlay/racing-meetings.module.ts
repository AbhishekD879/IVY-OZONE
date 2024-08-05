import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';

import { LadbrokesDesktopRacingOverlayContentComponent } from '@ladbrokesDesktop/lazy-modules/racesMeetingsOverlay/components/racingOverlayContent/racing-overlay-content.component';
import { RacingFeaturedModule } from '@ladbrokesDesktop/lazy-modules/racingFeatured/racing-featured.module';
import { RacingModule } from '@racingModule/racing.module';
import { LadbrokesDesktopRacingAntepostContentComponent } from '@ladbrokesDesktop/lazy-modules/racesMeetingsOverlay/components/racingAntepostOverlay/racing-antepost-content.component';

@NgModule({
  imports: [
    RacingFeaturedModule,
    SharedModule,
    RacingModule
  ],
  providers: [],
  exports: [
    LadbrokesDesktopRacingOverlayContentComponent,
    LadbrokesDesktopRacingAntepostContentComponent
  ],
  declarations: [
    LadbrokesDesktopRacingOverlayContentComponent,
    LadbrokesDesktopRacingAntepostContentComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingOverlayModule {
  static entry = { LadbrokesDesktopRacingOverlayContentComponent, LadbrokesDesktopRacingAntepostContentComponent };
}
