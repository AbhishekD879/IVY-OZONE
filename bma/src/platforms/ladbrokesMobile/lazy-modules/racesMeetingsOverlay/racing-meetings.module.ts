import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';

import { LadbrokesRacingOverlayContentComponent } from '@ladbrokesMobile/lazy-modules/racesMeetingsOverlay/components/racingOverlayContent/racing-overlay-content.component';
import { RacingFeaturedModule } from '@lazy-modules-module/racingFeatured/racing-featured.module';
import { RacingModule } from '@racingModule/racing.module';
import { LadbrokesRacingAntepostContentComponent } from '@ladbrokesMobile/lazy-modules/racesMeetingsOverlay/components/racingAntepostOverlay/racing-antepost-content.component';

@NgModule({
  imports: [
    RacingFeaturedModule,
    SharedModule,
    RacingModule
  ],
  providers: [],
  exports: [
    LadbrokesRacingAntepostContentComponent
  ],
  declarations: [
    LadbrokesRacingOverlayContentComponent,
    LadbrokesRacingAntepostContentComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingOverlayModule {
  static entry = { LadbrokesRacingOverlayContentComponent, LadbrokesRacingAntepostContentComponent };
}
