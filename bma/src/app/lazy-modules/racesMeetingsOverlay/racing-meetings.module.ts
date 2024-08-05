import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { RacingFeaturedModule } from '@lazy-modules-module/racingFeatured/racing-featured.module';
import { RacingOverlayContentComponent } from '@app/lazy-modules/racesMeetingsOverlay/components/racingOverlayContent/racing-overlay-content.component';
import { RacingAntepostContentComponent } from '@app/lazy-modules/racesMeetingsOverlay/components/racingAntepostOverlay/racing-antepost-content.component';
import { RacingModule } from '@racingModule/racing.module';

@NgModule({
  imports: [
    RacingFeaturedModule,
    SharedModule,
    RacingModule
  ],
  providers: [],
  exports: [RacingOverlayContentComponent, RacingAntepostContentComponent],
  declarations: [
    RacingOverlayContentComponent,
    RacingAntepostContentComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RacingOverlayModule {
  static entry = { RacingOverlayContentComponent, RacingAntepostContentComponent };
}
